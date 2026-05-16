from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(jobs, resume_data):
    role = resume_data.get("role", "")
    skills = resume_data.get("skills", [])
    location = resume_data.get("location", "")

    resume_text = role + " " + " ".join(skills)

    job_texts = [job["title"] + " " + job["description"] for job in jobs]

    if not job_texts:
        return []

    # Build TF-IDF vectors and compute cosine similarity
    corpus = [resume_text] + job_texts
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    results = []

    for i, job in enumerate(jobs):
        score = float(scores[i])
        job["match_score"] = score

        # Role filter
        if role.lower() not in job["title"].lower():
            if score < 0.2:
                continue

        # Location filter
        if location:
            if location.lower() not in job["description"].lower():
                if score < 0.15:
                    continue

        results.append(job)

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
