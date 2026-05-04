def remove_duplicates(jobs):
    seen = set()
    unique = []

    for job in jobs:
        key = (job['title'].lower(), job['company'].lower())

        if key not in seen:
            seen.add(key)
            unique.append(job)

    return unique