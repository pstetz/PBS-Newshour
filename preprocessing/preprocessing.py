import re

def remove_party(name):
    dem_regex = r"\(D-[^)]*\)"
    rep_regex = r"\(R-[^)]*\)"
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
    return name

def clean_names(name):
    name = name.upper()
    for specific_title in specific_titles:
        name = name.replace(specific_title, "")
        
    for title in titles:
        name = name.replace(title, "")
    
    name = name.replace("\xa0", " ")
    name = name.replace("\ufeff", "")
    name = name.replace("(D)", "").replace("(R)", "").replace("(D-N.C.)", "")
    name = name.replace("(RET.)", "")
    name = name.replace("—", "")
    
    
    for qualifier in ("(THROUGH INTERPRETER)", "(THROUGH TRANSLATOR)",
                      "(AT PODIUM)", "(TRANSLATED)", "(RECORDING)", "VOICE OF "):        
        if name != qualifier:
            name = name.replace(qualifier, "")
            
    name = clean_name_edge_cases(name)
    return name.strip()

titles = ("PRESIDENT", "PRIME MINISTER", "MAYOR",
          "U.S. ATTORNEY GENERAL", "U.S AMBASSADOR",
          "U.N. AMBASSADOR", "MEDAL OF HONOR RECIPIENT",
          "LT.", "COLONEL", "COL.", "SGT.", "CAPT.", "GEN.",
          "ADM.", "VICE ADM.", "COM.", "MAJ.", "BRIG.",
          "U.S. ARMY", "U.S.", "U. S.", "U.S",
          "R- WIS.", "NEW YORK CITY", "MASSACHUSETTS",
          "GOV.", "REP.", "SEN.",
          "CHAIRMAN", "OFFICER", "JUDGE",
          "REV.", "DR.", "PROF.", "FMR.", "FORMER",
          "FILM CRITIC", "OF PACIFICA RADIO")

specific_titles = ("FORMER U.S. PRESIDENT", "FMR. PRESIDENT",
                 "PRESIDENT-ELECT", "FORMER GOV.", "FMR. JUSTICE",
                 "1ST LT.", "2ND LT.", "UTAH REP.",
                 "FORMER U.S. AMBASSADOR TO VIETNAM", "FORMER U.S. CONGRESSWOMAN",
                 "AMBASSADOR TO THE UNITED NATIONS",
                 "U.S. AMBASSADOR TO THE U.N.", "U.S. ENERGY SECRETARY",
                 "U.S. TREASURY SECRETARY", "U.S. REPRESENTATIVE",
                 "SECRETARY OF HEALTH AND HUMAN SERVICES", "NEW YORK CITY POLICE COMMISSIONER",
                 "LOS ANGELES CLIPPERS POINT", "FBI SPECIAL AGENT IN CHARGE",
                 "CHIEF OF MILITARY INTELLIGENCE", "SENATE FOREIGN RELATIONS COMMITTEE",
                 "UNIVERSITY OF CENTRAL FLORIDA’S")

