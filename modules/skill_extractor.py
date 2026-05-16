import re


def extract_skills_and_location(text):
    text_lower = text.lower()

    skills = set()
    location = None

    # Extract multi-word skill-like phrases
    words = re.findall(r'\b[a-zA-Z][a-zA-Z\+\#\.\/\-]{2,25}\b', text_lower)
    for word in words:
        if word not in ["project", "experience", "achievement", "education", "university"]:
            skills.add(word)

    # Extract location
    location_keywords = [
        "bangalore", "bengaluru", "mumbai", "delhi", "hyderabad",
        "chennai", "pune", "kolkata", "noida", "gurgaon",
        "india", "remote"
    ]
    for loc in location_keywords:
        if loc in text_lower:
            location = loc.title()
            break

    return list(skills), location