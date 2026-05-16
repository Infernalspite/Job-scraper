import re

# Common tech roles
ROLE_KEYWORDS = [
    "data scientist", "data analyst", "machine learning engineer",
    "ai engineer", "software engineer", "backend developer",
    "frontend developer", "full stack developer"
]


def parse_resume(text):
    text_lower = text.lower()

    skills = set()
    roles = set()

    # -------- SKILLS (keyword-based) -------- #
    words = re.findall(r'\b[a-zA-Z][a-zA-Z\+\#\.\/\-]{2,25}\b', text_lower)
    for word in words:
        if word not in ["project", "experience", "objective", "education", "university"]:
            skills.add(word)

    # -------- ROLES -------- #
    for role in ROLE_KEYWORDS:
        if role in text_lower:
            roles.add(role)

    # -------- LOCATION -------- #
    location = None
    location_keywords = [
        "bangalore", "bengaluru", "mumbai", "delhi", "hyderabad",
        "chennai", "pune", "kolkata", "noida", "gurgaon",
        "india", "remote"
    ]
    for loc in location_keywords:
        if loc in text_lower:
            location = loc.title()
            break

    return {
        "skills": list(skills),
        "roles": list(roles),
        "location": location
    }