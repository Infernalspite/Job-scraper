import requests
from bs4 import BeautifulSoup
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from serpapi import GoogleSearch
from config import SERPAPI_KEY, SEARCH_KEYWORDS
import time

# ---------------- DRIVER notwrk :( ---------------- #
def get_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def fetch_google_jobs():
    params = {
        "engine": "google_jobs",
        "q": SEARCH_KEYWORDS,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = []

    for job in results.get("jobs_results", []):
        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "description": job.get("description", ""),
            "link": job.get("related_links", [{}])[0].get("link", ""),
            "source": "GoogleJobs",
            "last_date": job.get("detected_extensions", {}).get("posted_at", "N/A"),
            "salary": 0
        })

    return jobs

# -------------ADZUNA wrkss ---------------- #
def fetch_adzuna():
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}&what={SEARCH_KEYWORDS}&results_per_page=20"

    try:
        response = requests.get(url)
        data = response.json()
    except:
        print("Adzuna fetch failed")
        return []

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "description": job.get("description", ""),
            "link": job.get("redirect_url", ""),
            "source": "Adzuna",
            "last_date": job.get("created", "N/A"),
            "salary": job.get("salary_max") or job.get("salary_min") or 0
        })

    return jobs


# --------------JOOBLEwrks ---------------- #
def fetch_jooble():
    url = f"https://jooble.org/api/{JOOBLE_API_KEY}"

    payload = {
        "keywords": SEARCH_KEYWORDS,
        "location": "India"
    }

    try:
        response = requests.post(url, json=payload)
    except:
        print("Jooble request failed")
        return []

    jobs = []

    if response.status_code == 200:
        data = response.json()

        for job in data.get("jobs", []):
            jobs.append({
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "description": job.get("snippet", ""),
                "link": job.get("link", ""),
                "source": "Jooble",
                "last_date": job.get("updated", "N/A"),
                "salary": 0
            })
    else:
        print("Jooble error:", response.status_code)

    return jobs


# --------------internshala doesnt work-------------- #
def fetch_internshala():
    try:
        response = requests.get("https://internshala.com/jobs/")
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("Internshala failed")
        return []

    jobs = []

    listings = soup.find_all("div", class_="individual_internship")

    for job in listings:
        title = job.find("h3")
        company = job.find("h4")

        jobs.append({
            "title": title.text.strip() if title else "",
            "company": company.text.strip() if company else "",
            "description": job.text.strip(),
            "link": "https://internshala.com",
            "source": "Internshala",
            "last_date": "N/A",
            "salary": 0
        })

    return jobs


# -------------that remoteok wrks ---------------- #
def fetch_remoteok():
    url = "https://remoteok.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("RemoteOK failed")
        return []

    jobs = []

    rows = soup.find_all("tr", class_="job")

    for job in rows:
        title = job.find("h2")
        company = job.find("h3")

        jobs.append({
            "title": title.text.strip() if title else "",
            "company": company.text.strip() if company else "",
            "description": job.text.strip(),
            "link": url,
            "source": "RemoteOK",
            "last_date": "N/A",
            "salary": 0
        })

    return jobs


# ----------------worked once?? ---------------- #
def fetch_weworkremotely():
    url = "https://weworkremotely.com/remote-jobs"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("WeWorkRemotely failed")
        return []

    jobs = []

    listings = soup.find_all("li", class_="feature")

    for job in listings:
        jobs.append({
            "title": job.text.strip(),
            "company": "",
            "description": job.text.strip(),
            "link": url,
            "source": "WeWorkRemotely",
            "last_date": "N/A",
            "salary": 0
        })

    return jobs


def fetch_all_jobs():
    sources = [
        fetch_google_jobs,
        fetch_adzuna,
        fetch_jooble,
        fetch_internshala,
        fetch_remoteok,
        fetch_weworkremotely
    ]

    all_jobs = []
    source_counts = {}

    for source in sources:
        try:
            jobs = source()
            all_jobs.extend(jobs)

            source_counts[source.__name__] = len(jobs)
            print(f"{source.__name__}: {len(jobs)} jobs")

        except Exception as e:
            print(f"Error in {source.__name__}: {e}")

    return all_jobs, source_counts