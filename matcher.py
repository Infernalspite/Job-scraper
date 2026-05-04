from sentence_transformers import SentenceTransformer, util
from config import *

model = SentenceTransformer('all-MiniLM-L6-v2')
def match_jobs(jobs, resume_data):
    role = resume_data["role"]
    skills = resume_data["skills"]
    location = resume_data["location"]

    resume_text = role + " " + " ".join(skills)

    job_texts = [job["title"] + " " + job["description"] for job in jobs]

    job_emb = model.encode(job_texts, convert_to_tensor=True)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    scores = util.cos_sim(resume_emb, job_emb)[0]

    results = []

    for i, job in enumerate(jobs):
        score = float(scores[i])
        job["match_score"] = score

        # ROLE FILTER
        if role.lower() not in job["title"].lower():
            if score < 0.2:
                continue

        # LOCATION FILTER
        if location:
            if location.lower() not in job["description"].lower():
                if score < 0.15:
                    continue

        results.append(job)

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
