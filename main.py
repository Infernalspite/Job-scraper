from modules.pdf_reader import extract_text_from_pdf
from modules.slm_resume_reader import parse_resume_smart
from modules.job_fetcher import fetch_all_jobs
from modules.deduplicator import remove_duplicates
from modules.matcher import match_jobs
from modules.exporter import export_to_excel
from config import LOCATION_PREFERENCE


def main():
    print("\n[1/6] Reading Resume...")
    text = extract_text_from_pdf("data/resume.pdf")

    print("\n[2/6] Understanding Resume (SLM)...")
    resume_data = parse_resume_smart(text)

    # Fix missing location
    if not resume_data["location"]:
        resume_data["location"] = LOCATION_PREFERENCE

    print("\n[3/6] Resume Insights:")
    print("Role:", resume_data["role"])
    print("Location:", resume_data["location"])
    print("Skills (sample):", resume_data["skills"][:10])

    print("\n[4/6] Fetching Jobs...")
    jobs, counts = fetch_all_jobs()

    print("\nJobs per source:")
    for src, count in counts.items():
        print(f"  {src}: {count}")

    print("\n[5/6] Removing duplicates...")
    jobs = remove_duplicates(jobs)
    print("After deduplication:", len(jobs))

    print("\n[5/6] Matching jobs using AI...")
    matched_jobs = match_jobs(jobs, resume_data)

    print("\nMatched jobs:", len(matched_jobs))

    if len(matched_jobs) == 0:
        print("\nNo jobs matched. Try:")
        print("- Lower MIN_MATCH_SCORE in config.py")
        print("- Change SEARCH_KEYWORDS")
        print("- Check resume content")
        return

    print("\n[6/6] Exporting to Excel...")
    export_to_excel(matched_jobs)

    print("\nDone! Open 'matched_jobs.xlsx'")


if __name__ == "__main__":
    main()