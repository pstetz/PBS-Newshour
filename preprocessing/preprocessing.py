import re

def remove_party(name):
    dem_regex = r"\(D[^)]*\)"
    rep_regex = r"\(R[^)]*\)"
    name = re.sub(dem_regex, "", name)
    name = re.sub(rep_regex, "", name)
    name = name.strip()
    return name

def clean_name_edge_cases(name):
    if name in {"UDY WOODRUFF"}:
        return "JUDY WOODRUFF"
    elif name in {"OBAMA"}:
        return "BARACK OBAMA"
    elif name in {"TRUMP"}:
        return "BARACK OBAMA"
    elif name in {"S RICHARD NIXON"}:
        return "RICHARD NIXON"
    elif name in {"HILLARY RODHAM CLINTON", "HILLARY RODHAM CLINTON"}:
        return "HILLARY CLINTON"
    return name

def clean_names(name):
    name = name.upper()
    
    name = name.replace("READ THE FULL TRANSCRIPT BELOW.", "")
    name = name.replace("\xa0", " ")
    name = name.replace("\ufeff", "")
    
    for specific_title in specific_titles:
        name = name.replace(specific_title, "")
        
    for title in titles:
        name = name.replace(title, "")
    
    for qualifier in ("(THROUGH INTERPRETER)", "(THROUGH INTEPRETER)", "(THROUGH TRANSLATOR)",
                      "(AT PODIUM)", "(TRANSLATED)", "(RECORDING)", "VOICE OF",
                      "(TRANSLATED FROM ITALIAN)", "(IN COURT)", "(THROUGH COMPUTER VOICE)",
                      "(SINGING)", "(TO GILBERT CANTRELL)", "(TRANSLATED )", "(VOICED OVER)",
                      "( INTERPRETER)", "(TELEVISION COMMERCIAL)", "THROUGH TRANSLATOR)"): 
        if name != qualifier:
            name = name.replace(qualifier, "")
            
    for misc in ("(D)", "(R)", "(I)", "(D-N.C.)", "(RET.)", "-"):
        name = name.replace(misc, "")
            
    name = clean_name_edge_cases(name)
    name = remove_party(name)
    name = name.replace("()", "")
    return name

titles = ("PRESIDENT", "PRIME MINISTER", "MAYOR",
          "U.S. ATTORNEY GENERAL", "U.S AMBASSADOR",
          "U.N. AMBASSADOR", "MEDAL OF HONOR RECIPIENT",
          "LT.", "COLONEL", "COL.", "SGT.", "CAPT.", "GEN.",
          "ADM.", "VICE ADM.", "COM.", "MAJ.", "BRIG.",
          "U.S. ARMY", "U.S.", "U. S.", "U.S",
          "R- WIS.", "NEW YORK CITY", "MASSACHUSETTS",
          "ARIZONA", "NEW YORK",
          "MINNESOTA", "1ST", "REPRESENTATIVE",
          "GOV.", "REP.", "SEN.", "REPUBLICAN", "DEMOCRAT",
          "DEMOCRATIC",
          "CHAIRMAN", "OFFICER", "JUDGE", "FATHER",
          "REV.", "DR.", "PROF.", "FMR.", "FORMER", "RETIRED",
          "SPC.",
          "RET.", "FILM CRITIC", "OF PACIFICA RADIO", "STAFF", "STATE",
          "ACTING")

specific_titles = ("FORMER U.S. PRESIDENT", "FMR. PRESIDENT", "PRESIDENT OF THE UNITED STATE",
                   "PRESIDENT OF THE UNITED STATES", "IAL CANDIDATE"
                 "PRESIDENT-ELECT", "FORMER GOV.", "FMR. JUSTICE",
                 "1ST LT.", "2ND LT.", "UTAH REP.", "1ST CLASS",
                 "FORMER U.S. AMBASSADOR TO VIETNAM", "FORMER U.S. CONGRESSWOMAN",
                   "INDEPENDENT SENATOR",
                   "OF VERMONT", "OF NEBRASKA", "OF PENNSYLVANIA", "OF OHIO",
                   "OF INDIANA", "OF ARIZONA", "OF TEXAS", "OF ALABAMA",
                   "OF WISCONSIN", "OF COLORADO", "OF OREGON",
                   "FORMER SUPREME COURT JUSTICE", "WHITE HOUSE PRESS SECRETARY",
                   "WHITE HOUSE BUDGET DIRECTOR",
                 "AMBASSADOR TO THE UNITED NATIONS",
                   "SECRETARY OF VETERANS AFFAIRS",
                   "NORTHWESTERN UNIVERSITY FINANCE PROFESSOR",
                   "RADIO IOWA REPORTER",  "SECRETARY OF STATE",
                   "SECURETARY OF STATE",
                 "U.S. AMBASSADOR TO THE U.N.", "U.S. ENERGY SECRETARY",
                 "U.S. TREASURY SECRETARY", "U.S. REPRESENTATIVE",
                 "SECRETARY OF HEALTH AND HUMAN SERVICES", "NEW YORK CITY POLICE COMMISSIONER",
                 "LOS ANGELES CLIPPERS POINT", "FBI SPECIAL AGENT IN CHARGE",
                 "CHIEF OF MILITARY INTELLIGENCE", "SENATE FOREIGN RELATIONS COMMITTEE",
                   "MINISTER OF AGRICULTURE", "FBI DIRECTOR",
                   "HOUSE MAJORITY LEADER",
                   "HOUSE MINORITY LEADER",
                   "HOUSE MINORITY WHIP",
                   "WHITE HOUSE SPOKESMAN",
                   "HOUSE SPEAKER",
                   "SEC. OF STATE",
                   "DEPARTMENT SPOKESWOMAN",
                   "DEPARTMENT SPOKESMAN",
                   "ASSISTANT ATTORNEY GENERAL",
                   "BISHOP",
                   "FIRST LADY",
                   "HIGHWAY PATROL CAPTAIN",
                   "MEXICAN FINANCE SECRETARY",
                   "NPR TV CRITIC",
                   "CITY COUNCILLOR",
                   "REPORTER AND AUTHOR",
                   "RUSSIAN FOREIGN MINISTER",
                   "SECRETARY OF TRANSPORTATION",
                   "SECRETARY OF TREASURY",
                   "TWOTIME OLYMPIC GOLD MEDALIST",
                   "SECRETARY OF HOMELAND SECURITY",
                   "SECURITY OF HOMELAND SECURITY",
                   "SOUTH CAROLINA CONGRESSMAN",
                   "SOUTH CAROLINA SENATOR",
                   "MIAMI HEAT FORWARD",
                   "CHIEF OPERATING",
                   "CHINESE FOREIGN MINISTER",
                   "– FOREIGN CORRESPONDENT",
                   "STANFORD BIOENGINEERING PROFESSOR",
                   "STANFORD UNIVERSITY PROFESSOR",
                   "SECRETARY OF DEFENSE",
                   "ACCUWEATHER METEOROLOGIST",
                   "UBER SPOKESPERSON",
                   "INTERIOR SECRETARY",
                   "FED CHAIR",
                   "ATTORNEY GENERAL",
                   "WYOMING SENATOR",
                   "PROJECT MANAGER",
                   "ILLINOIS DEMOCRAT",
                   "ILLINOIS DEMOCRAT",
                   "SECRETARY OF EDUCATION",
                   "NATO SECRETARYGENERAL",
                   "NINETEENYEAROLD",
                   "ACTING UKRAINIAN",
                 "UNIVERSITY OF CENTRAL FLORIDA’S PRESIDENT", "SECRETARY OF VETERANS AFFAIRS RETIRED",
                  "HOUSING AND URBAN DEVELOPMENT SECRETARY", "HEALTH AND HUMAN SERVICES SECRETARY",
                  "BRITISH FOREIGN SECRETARY", "BRITISH PRIME MINISTER",
                  "CHIEF MASTER", "DALLAS POLICE CHIEF", "COUNTY SCHOOL ADMINISTRATOR",
                  "E.U. COMPETITION COMMISSIONER", "FACEBOOK GENERAL COUNSEL", "EXECUTIVE VICE",
                  "OF AMNESTY INTERNATIONAL", "GM VICE", "GREEN PARTY CANDIDATE")

