from datetime import datetime
from urllib.request import Request, urlopen

import psycopg2

from bs4 import BeautifulSoup


# DB connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_db_user",
        password="your_db_password",
        host="your_db_host",
        port="your_db_port"
    )
    return conn


def fetch_jobs():
    req = Request('https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm')

    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Referer', 'https://www.google.com/')  # Example referrer

    r = urlopen(req).read().decode('utf-8')

    soup = BeautifulSoup(r, 'html.parser')
    jobs_list = []

    for job_card in soup.find_all('li', class_='JobsList_jobListItem__wjTHv'):
        employer_name = job_card.find('span', class_='EmployerProfile_compactEmployerName__LE242')
        job_title = job_card.find('a', class_='JobCard_jobTitle___7I6y')
        location = job_card.find('div', class_='JobCard_location__rCz3x')
        description = job_card.find('div', class_='JobCard_jobDescriptionSnippet__yWW8q')
        salary = job_card.find('div', class_='JobCard_salaryEstimate__arV5J')
        skills = job_card.find('b', string='Skills:')
        date_posted = job_card.find('div', class_='JobCard_listingAge__Ny_nG')

        # Extract text and handle missing data
        employer_name = employer_name.text.strip() if employer_name else None
        job_title = job_title.text.strip() if job_title else "No Title"
        description = description.text.strip() if description else None
        location = location.text.strip() if location else None
        salary = salary.text.strip() if salary else None
        skills = skills.find_next_sibling(text=True).strip() if skills else None
        date_posted = date_posted.text.strip() if date_posted else None
        created_at = datetime.now()
        updated_at = datetime.now()

        jobs_list.append((job_title, employer_name, location, description, skills, None, None, salary, date_posted,
                     created_at, updated_at))

    return jobs_list


# Store job data in PostgreSQL
def store_jobs(jobs):
    conn = get_db_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO jobs_job (title, company_name, location, description, skills_required, 
    experience_required, education_required, salary_range, date_posted, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cur.executemany(insert_query, jobs)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    jobs = fetch_jobs()
    store_jobs(jobs)
    print("Data Saved to DB")
