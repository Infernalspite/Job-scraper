import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills_and_location(text):
    doc = nlp(text)

    skills = set()
    location = None

    for chunk in doc.noun_chunks:
        txt = chunk.text.lower()

        if len(txt) > 3 and len(txt.split()) <= 3:
            if not any(x in txt for x in ["project", "experience", "achievement"]):
                skills.add(txt)

    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = ent.text

    return list(skills), location