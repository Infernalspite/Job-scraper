import re

ROLE_LABELS = [
    "data scientist",
    "machine learning engineer",
    "data analyst",
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "ai engineer",
]

# Common technical skills to look for
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi",
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "ci/cd",
    "git", "linux", "rest api", "graphql", "microservices",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
    "html", "css", "sass", "tailwind", "bootstrap",
    "agile", "scrum", "jira", "devops", "testing", "unit testing",
    "data analysis", "data visualization", "tableau", "power bi", "excel",
    "spark", "hadoop", "kafka", "airflow", "etl",
    "figma", "photoshop", "ui/ux", "responsive design",
]

# Common location indicators
LOCATION_KEYWORDS = [
    "india", "bangalore", "bengaluru", "mumbai", "delhi", "hyderabad", "chennai",
    "pune", "kolkata", "ahmedabad", "noida", "gurgaon", "gurugram", "jaipur",
    "new york", "san francisco", "london", "singapore", "dubai", "toronto",
    "remote", "hybrid", "on-site", "work from home",
]


def extract_location(text):
    """Extract location from resume text using keyword matching."""
    text_lower = text.lower()
    for loc in LOCATION_KEYWORDS:
        if loc in text_lower:
            return loc.title()
    return None


def extract_skills(text):
    """Extract skills from resume text using keyword matching."""
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        # Use word boundary matching for short skills to avoid false positives
        if len(skill) <= 3:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        else:
            if skill in text_lower:
                found_skills.append(skill)

    return found_skills


def detect_role(text):
    """Detect the most likely role from resume text using keyword matching."""
    text_lower = text.lower()
    best_role = "software engineer"
    best_count = 0

    for role in ROLE_LABELS:
        role_words = role.split()
        count = sum(1 for word in role_words if word in text_lower)

        if count > best_count:
            best_count = count
            best_role = role

    # Also check for exact role matches
    for role in ROLE_LABELS:
        if role in text_lower:
            return role

    return best_role


def parse_resume_smart(text):
    skills = extract_skills(text)
    location = extract_location(text)
    role = detect_role(text)

    return {
        "skills": skills,
        "location": location,
        "role": role
    }