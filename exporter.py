import pandas as pd

def export_to_excel(jobs):
    if not jobs:
        print("No jobs ❌")
        return

    df = pd.DataFrame([{
        "Job/Internship Name": j["title"],
        "Company": j["company"],
        "Description": j["description"][:300],
        "Last Date": j["last_date"],
        "Match Score": round(j.get("match_score", 0), 3),
        "Salary": j.get("salary", 0)
    } for j in jobs])

    df.to_excel("matched_jobs.xlsx", index=False)

    print("Excel ready ✅")