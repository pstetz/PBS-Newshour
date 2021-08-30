import re
import time
import json
from pathlib import Path
import multiprocessing as mlt
import urllib
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


def download_url(url):
    page = urllib.request.urlopen(url)
    return BeautifulSoup(page, features="lxml")


def find_max(url_dir):
    """
    Going on PBS Newshour, there is a bar that only goes up to 500, however
    don't trust it! If you put in higher page numbers in the URL, you can
    go back further in time. It'll still give you a URL if you've exceeded
    and it will say "There are no videos that match the filter criteria."
    """
    regex = "There are no videos that match the filter criteria."
    # HACK: assume around 2,000 pages currently. In the future max 20,000
    # pages. An excellent example of using binary search to save time!
    start, end = 2000, 20000
    while start < end:
        guess = start + ((end - start) // 2)
        if str(download_url(f"{url_dir}/{guess}")).find(regex) == -1:
            start = guess + 1
        else:
            end = guess
    print("Guessed max page number:", start - 1)
    return start - 1


def get_story(url):
    page = download_url(f"{url}#story")

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
    return page.find("time").text


def get_speeches(transcript):
    speeches, speakers = list(), set()
    for speech in transcript:
        paragraphs = speech.find_all("p")

        if paragraphs[0].find("strong") is not None:
            speaker = (paragraphs[0].find("strong").text.replace(":", "")
                       .split(",")[0])

            # This allows for some mistakes, see edge case (1) below
#             if not speaker.isupper():
#                 continue

            speakers.add(speaker)
            paragraphs = paragraphs[1:]

        text = [paragraph.text for paragraph in paragraphs]
        speeches.append([speaker, text])

    return speeches, list(speakers)


def get_transcript(page):
    transcript = page.find("div", {"id": "transcript"})

    if transcript is None:
        return None, None

    transcript = transcript.find_all("li")
    return get_speeches(transcript)


# Gets all the information from a video clip
def get_single_info(url):
    page = download_url(f"{url}#transcript")

    story = get_story(url)
    date = get_date(page)
    transcript, speakers = get_transcript(page)

    return story, date, transcript, speakers


def is_bad_url(url):
    root = "https://www.pbs.org/newshour"
    if url == f"{root}/show/0":
        return True
    ignore = ["politics", "nation", "world"]
    if url.replace(f"{root}/", "").split("/")[0] in ignore:
        return True
    return False


# Loops through each video on a page and stores each information
def get_multi_info(videos, page, dst_dir):
    dst_dir = dst_dir / str(page)
    for video in videos:
        is_full = video.find_all(text=re.compile('Full Episode'))
        if len(is_full) == 1:
            continue
        video = video.find("a", {"class": "card-sm__title"})

        url = video["href"]
        title = video.span.text

        if is_bad_url(url):
            continue
        try:
            story, date, transcript, speakers = get_single_info(url)

            news_story = {
                "url": url,
                "story": story,
                "date": date,
                "title": title,
                "transcript": transcript,
                "speakers": speakers
            }
            fp = dst_dir / (url.split("/")[-1] + ".json")
            fp.parent.mkdir(exist_ok=True,  parents=True)
            with open(fp, "w") as f:
                json.dump(news_story, f)
        except Exception as e:
            print(e)
            print(url)


def scrape_page(url_dir, page, dst_dir):
    data = download_url(f"{url_dir}/{page}")

    # Display pulled video titles
    videos = data.find("div", {"id": "all-videos"})
    videos = videos.findAll("article", {"class": "card-sm"})

    get_multi_info(videos, page, dst_dir)


def scrape_threading(url_dir, dst_dir, THREADS, START, DURATION):
    """
    A multiprocessing threading
    """
    procs = []
    pbar = tqdm(total=DURATION)  # progress bar

    pages = list(range(START, START+DURATION + 1))
    while len(pages):
        procs = [p for p in procs if p.is_alive()]
        if len(procs) > THREADS:
            time.sleep(2)
            continue
        page = pages.pop()
        pbar.update(1)
        p = mlt.Process(target=scrape_page, args=(url_dir, page, dst_dir))
        procs.append(p)
        p.start()

    [p.join() for p in procs]  # Join all threads
    pbar.close()  # End progress bar


def main(url_dir, dst_dir, START=1, DURATION=None, THREADS=20):
    if DURATION is None:
        DURATION = find_max(url_dir)  # How many pages to scrape

    scrape_threading(url_dir, dst_dir, THREADS, START, DURATION)


if __name__ == "__main__":
    url_dir = "https://www.pbs.org/newshour/video/page"
    dst_dir = Path("/Users/pbezuhov/Desktop/pbs")
    main(url_dir, dst_dir)


"""
FIXME: Selenium the comments are loaded with JS so beautiful soup won't work
something interactive like Selenium needs to be used
def get_comments(page):
    comments = page.find("button", {"class": "comments__btn"})
    if comments is None:
        return None

    comments = comments.find("span")
    if comments is None:
        return None
    return comments.text
"""
