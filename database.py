import sqlite3

# 🔹 Create database and table
def create_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            link TEXT,
            match_score REAL,
            date_scraped TEXT
        )
    """)

    conn.commit()
    conn.close()


# 🔹 Save jobs into database
def save_jobs(jobs):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute("""
            INSERT INTO jobs (title, company, link, match_score, date_scraped)
            VALUES (?, ?, ?, ?, ?)
        """, (
            job.get("title"),
            job.get("company"),
            job.get("link"),
            job.get("match_score"),
            job.get("date_scraped")
        ))

    conn.commit()
    conn.close()


# 🔹 (Optional but VERY useful) View stored jobs
def view_jobs():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


# 🔹 (Optional) Clear all data 
def clear_jobs():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

    conn.commit()
    conn.close()