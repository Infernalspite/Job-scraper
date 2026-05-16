import math
from collections import Counter
import re

def get_words(text):
    # Basic tokenization
    words = re.findall(r'\b[a-z]{2,}\b', text.lower())
    # Extremely basic stop words
    stop_words = {"the", "and", "a", "an", "in", "on", "at", "to", "for", "of", "with", "is", "are", "this"}
    return [w for w in words if w not in stop_words]

def compute_tf(word_counts, total_words):
    tf = {}
    for word, count in word_counts.items():
        tf[word] = count / float(total_words)
    return tf

def compute_idf(doc_list):
    idf = {}
    N = len(doc_list)
    # count how many docs contain each word
    doc_counts = Counter()
    for doc in doc_list:
        unique_words = set(doc)
        for word in unique_words:
            doc_counts[word] += 1
            
    for word, count in doc_counts.items():
        idf[word] = math.log10(N / float(count))
    return idf

def compute_tfidf(tf, idf):
    tfidf = {}
    for word, val in tf.items():
        tfidf[word] = val * idf.get(word, 0)
    return tfidf

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def match_jobs(jobs, resume_data):
    role = resume_data.get("role", "")
    skills = resume_data.get("skills", [])
    location = resume_data.get("location", "")

    resume_text = role + " " + " ".join(skills)
    job_texts = [job["title"] + " " + job["description"] for job in jobs]

    if not job_texts:
        return []

    # Prepare corpus for pure Python TF-IDF
    corpus = [resume_text] + job_texts
    tokenized_corpus = [get_words(doc) for doc in corpus]
    
    # Calculate TF for each doc
    tf_docs = []
    for tokens in tokenized_corpus:
        counts = Counter(tokens)
        total = len(tokens) if len(tokens) > 0 else 1
        tf_docs.append(compute_tf(counts, total))
        
    # Calculate global IDF
    idf = compute_idf(tokenized_corpus)
    
    # Calculate TF-IDF
    tfidf_docs = [compute_tfidf(tf, idf) for tf in tf_docs]
    
    resume_vector = tfidf_docs[0]
    job_vectors = tfidf_docs[1:]

    results = []

    for i, job in enumerate(jobs):
        score = cosine_similarity(resume_vector, job_vectors[i])
        job["match_score"] = score

        # Role filter
        if role.lower() not in job["title"].lower():
            if score < 0.05: # lowered threshold slightly for pure python method
                continue

        # Location filter
        if location:
            if location.lower() not in job["description"].lower():
                if score < 0.02:
                    continue

        results.append(job)

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
