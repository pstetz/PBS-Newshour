# Progress bar
from tqdm import tqdm

### Standard imports
import pandas as pd
import numpy as np

# Multiprocessing (saves a lot of time)
import multiprocessing as mlt

# Regular expressions
import re

### Libraries for website scraping
from bs4 import BeautifulSoup
import requests
import urllib

def get_story(url):
    # Open
    page = urllib.request.urlopen(f"{url}#story")
    page = BeautifulSoup(page)
    
    # Layout 1
    story = page.find("div", {"id": "story"})
    if story is not None:
        story = story.find("p")
        if story is not None:
            return story.text
    
    # Layout 2
    story = page.find("div", {"id": "transcript"})
    if story is not None:
        story = story.find("div", {"class": "vt__excerpt body-text"})
        if story is not None:
            story = story.find("p")
            if story is not None:
                return story.text
    
    # Some clips don't have a summary story        
    return None
    
def get_date(page):
    date = page.find("time").text
    return date

def get_comments(page):
    comments = page.find("button", {"class": "comments__btn"})
    if comments is None:
        return None
    
    comments = comments.find("span")
    if comments is None:
        return None
    return comments.text

def get_speeches(transcript):
    speeches, speakers = list(), set()

    for speech in transcript:
        paragraphs = speech.find_all("p")
        
        if paragraphs[0].find("strong") != None:
            speaker = paragraphs[0].find("strong").text.replace(":", "").split(",")[0]
            
            # This allows for some mistakes, see edge case (1) below
#             if not speaker.isupper():
#                 continue

            speakers.add(speaker)
            paragraphs = paragraphs[1:]
            
        text = [paragraph.text for paragraph in paragraphs]
        speeches.append([speaker, text])
        
    return speeches, speakers

def get_transcript(page):
    transcript = page.find("div", {"id": "transcript"})
    
    if transcript is None:
        return None, None
    
    transcript = transcript.find_all("li")
        
    return get_speeches(transcript)

# Gets all the information from a video clip
def get_single_info(url):
    page = urllib.request.urlopen(f"{url}#transcript")
    page = BeautifulSoup(page)
    
    story = get_story(url)
    date  = get_date(page)
    transcript, speakers = get_transcript(page)
    comments = get_comments(page)
    
    return story, date, transcript, speakers, comments

# Loops through each video on a page and stores each information
def get_multi_info(pbs_df, videos, pbar, THREADS):
    for video in videos:
        is_full = video.find_all(text=re.compile('Full Episode'))
        if len(is_full) == 1:
            continue
        video = video.find("a", {"class": "card-sm__title"})
        
        url   = video["href"]
        title = video.span.text
                
        if url == "https://www.pbs.org/newshour/show/0":
            continue
        
        if url.replace("https://www.pbs.org/newshour/", "").split("/")[0] in ["politics", "nation", "world"]:
            continue
        
        try:
            story, date, transcript, speakers, comments = get_single_info(url)

            # Store info in df
            row = [url, story, date, title, transcript, speakers, comments]
            pbs_df.loc[len(pbs_df)] = row
        except:
            print("FAILED")
            print(url)
    pbar.update(THREADS)
    return pbs_df
    
def scrap_all(url_dir, pages, df_dict, i, pbar, THREADS):
    cols   = ["URL", "Story", "Date", "Title", "Transcript",
              "Speakers", "Number of Comments"]
    pbs_df = pd.DataFrame(columns = cols)
    
    for i in pages:
    
        # Retrieving website data
        page = urllib.request.urlopen(f"{url_dir}{i}")
        page = BeautifulSoup(page)

        # Display pulled video titles
        videos = page.find("div", {"id": "all-videos"})
        videos = videos.findAll("article", {"class": "card-sm"})
        
        pbs_df = get_multi_info(pbs_df, videos, pbar, THREADS)
        
    df_dict[i] = pbs_df

### A multiprocessing threading
def scrap_threading(url_dir, THREADS, START, DURATION):
    manager = mlt.Manager() # multiprocessing manager
    df_dict = manager.dict() # Shared variable among threads
    jobs = []
    pbar = tqdm(total=DURATION) # progress bar
    
    # Splits all the pages needed into even lists.  Numpy's amazing!
    grouped_pages = np.arange(START, START+DURATION)
    grouped_pages = np.array_split(grouped_pages, THREADS)
    
    # Start each thread
    for i, pages in enumerate(grouped_pages):
        p = mlt.Process(target=scrap_all, args=(url_dir, pages, df_dict, i, pbar, THREADS))
        jobs.append(p)
        p.start()
    
    # Join all threads
    for proc in jobs:
        proc.join()
        
    pbar.close() # End progress bar
    return df_dict


def join_mlt_df(mlt_dict_df):
    df = pd.concat(mlt_dict_df.values())
    return df.reset_index(drop=True)