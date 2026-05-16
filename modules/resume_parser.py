import spacy
from geotext import GeoText

nlp = spacy.load("en_core_web_sm")

# Common tech roles
ROLE_KEYWORDS = [
    "data scientist", "data analyst", "machine learning engineer",
    "ai engineer", "software engineer", "backend developer",
    "frontend developer", "full stack developer"
]

def parse_resume(text):
    doc = nlp(text.lower())

    skills = set()
    roles = set()

    # -------- SKILLS -------- #
    for chunk in doc.noun_chunks:
        txt = chunk.text.strip()

        if 2 < len(txt) < 30:
            if not any(x in txt for x in ["project", "experience", "objective"]):
                skills.add(txt)

    # -------- ROLES -------- #
    for role in ROLE_KEYWORDS:
        if role in text.lower():
            roles.add(role)

    # -------- LOCATION (SMART) -------- #
    places = GeoText(text)

    location = None
    if places.cities:
        location = places.cities[0]
    elif places.countries:
        location = places.countries[0]

    return {
        "skills": list(skills),
        "roles": list(roles),
        "location": location
    }