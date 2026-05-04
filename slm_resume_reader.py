from sentence_transformers import SentenceTransformer
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

ROLE_LABELS = [
    "data scientist",
    "machine learning engineer",
    "data analyst",
    "software engineer",
    "backend developer",
    "frontend developer"
]

def extract_location(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text

    return None


def extract_skills(text):
    doc = nlp(text)

    skills = set()

    for chunk in doc.noun_chunks:
        txt = chunk.text.lower()

        if 2 < len(txt) < 30:
            if not any(x in txt for x in ["project", "experience", "objective"]):
                skills.add(txt)

    return list(skills)


def detect_role(text):
    embeddings = model.encode([text] + ROLE_LABELS)

    resume_vec = embeddings[0]
    role_vecs = embeddings[1:]

    scores = np.dot(role_vecs, resume_vec)

    best_index = int(np.argmax(scores))

    return ROLE_LABELS[best_index]


def parse_resume_smart(text):
    skills = extract_skills(text)
    location = extract_location(text)
    role = detect_role(text)

    return {
        "skills": skills,
        "location": location,
        "role": role
    }