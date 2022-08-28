import re

def remove_party(name):
    dem_regex = r"\(D[^)]*\)"
    rep_regex = r"\(R[^)]*\)"
    name = re.sub(dem_regex, "", name)
    name = re.sub(rep_regex, "", name)
    name = name.replace("ICONN.", "")
    name = name.strip()
    return name

def clean_name_edge_cases(name):
    if name in {"UDY WOODRUFF"}:
        return "JUDY WOODRUFF"
    elif name in {"OBAMA"}:
        return "BARACK OBAMA"
    elif name in {"JOE BIDEN", "JOSE BIDEN", "BIDEN"}:
        return "JOSEPH BIDEN"
    elif name in {"VICE MIKE  PENCE"}:
        return "MIKE PENCE"
    elif name in {"S RICHARD NIXON"}:
        return "RICHARD NIXON"
    elif name in {"HILLARY RODHAM CLINTON", "HILLARY RODHAM CLINTON IC"}:
        return "HILLARY CLINTON"
    elif name in {'TRUMP ( OF THE UNION)', "TRUMP", "TRUMP (STATE OF THE UNION)"}:
        return "DONALD TRUMP"
    elif name in {"SREENIVASAN", "SREENIVASN", "HARI"}:
        return "HARI SREENIVASAN"
    elif name in {"SPICER"}:
        return "SEAN SPICER"
    elif name in {"PUTIN"}:
        return "VLADIMIR PUTIN"
    # Sorry to any hispanics, but accents are hard to type!
    elif name in {"CARMEN YULÍN CRUZ"}:
        return "CARMEN YULIN CRUZ"
    elif name in {"SPEAKER JOHN BOEHNER"}:
        return "JOHN BOEHNER"
    elif name in {"PAUL PAUL RYAN"}:
        return "PAUL RYAN"
    elif name in {"MIKE MULLEN"}:
        return "MICHAEL MULLEN"
    elif name in {"JUSTICE ANTHONY KENNEDY"}:
        return "ANTHONY KENNEDY"
    elif name in {"THE  AL SHARPTON"}:
        return "AL SHARPTON"
    return name

def clean_names(name):
    name = name.upper()
    
    name = name.replace("READ THE FULL TRANSCRIPT BELOW.", "")
    name = name.replace("\xa0", " ")
    name = name.replace("\ufeff", "")
    
    for specific_title in specific_titles:
        name = name.replace(specific_title, "")
    
    for vice in ("VIE PRESIDENT", "VICE PRESIDENT"):
        name = name.replace(vice, "")
        
    for title in titles:
        name = name.replace(title, "")
    
    for qualifier in ("(THROUGH INTERPRETER)", "(THROUGH INTEPRETER)", "(THROUGH TRANSLATOR)",
                      "(AT PODIUM)", "(TRANSLATED)", "(RECORDING)", "VOICE OF",
                      "(TRANSLATED FROM ITALIAN)", "(IN COURT)", "(THROUGH COMPUTER VOICE)",
                      "(SINGING)", "(TO GILBERT CANTRELL)", "(TRANSLATED )", "(VOICED OVER)",
                      "( INTERPRETER)", "(TELEVISION COMMERCIAL)", "THROUGH TRANSLATOR)",
                      "(SUBTITLES)", "(EXECUTIVE DIRECTOR", "(SPEECH)", "(THROUGH INTERPRETER",
                      "(THROUGH INTERPRETERR)", "(THROUGH INTERPRETOR)", "(ENGLISH)",
                      "(VOICE IN RECORD PLAYER)", "(SPANISH)", "(LAUGHTER)", "(THROUGH COMPUTER)",
                      "(ON VIDEO)", "(ON STAGE)", "(TO DOGS)", "(TRANSLATED FROM FRENCH)",
                      "(CURATOR", "(VOICEOVER)", "(THROUGH INTERPETER)", "(IN CHARACTER)",
                      "(THROUGH INETRPRETER)", "(ON CAMERA)", "(TO LEE)", "(NOBLE ENERGY)", "(VOICEOVER)",
                      "(FEBRUARY 19", "(IN CAR)", "(2012)", "(TO PATRICK)", "(TO LISETTE)", "(TO SCOZZARI0",
                      "(APRIL 18"): 
        if name != qualifier:
            name = name.replace(qualifier, "")
            
    for misc in ("(D)", "(R)", "RMINN",
                 "(I)", "ICONN", "(IVA.)",
                 "(D-N.C.)", "(RET.)", "-", "IAL CANDIDATE", "VICE  ", "(IMAINE)",
                 "(ICONNECTICUT)", "(VTI)", "(VTD)", "(IVT)", "(IVA.)", "(IVA)",
                 "(VOICEOVER)", "(TO ANDRE)", " R)", "[NARRATION]", "[MAY 2014]"):
        name = name.replace(misc, "")
    name = remove_party(name)
    name = name.replace("()", "")
    name = name.replace("[", "").replace("]", "")
    name = name.strip()
    name = clean_name_edge_cases(name)
    return name

def get_mistaken_names():
    return {clean_names(x) for x in mistakes}


