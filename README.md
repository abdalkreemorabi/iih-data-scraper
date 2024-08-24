# Glassdoor Job Scraper

This Python project scrapes job listings from Glassdoor 
for the "Software Engineer" role and stores the data in a PostgresSQL database.

## Features

- Scrapes job listings from Glassdoor.
- Extracts job title, employer name, location, description, skills, salary, and date posted.
- Stores the extracted data in a PostgresSQL database.
- Uses `pypoetry` for dependency management.

## Requirements

- Python 3.11+
- PostgresSQL database
- Dependencies (managed by `pypoetry`):

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/abdalkreemorabi/django-job-portal.git
   cd django-job-portal
   ```

2. **Set Up the Virtual Environment**
   ```bash
      poetry install
   ```

3. **Activate the Virtual Environment**
   ```bash
      poetry shell
   ```
4. **Run the Script**
   ```bash
     python glassdoor_scraper.py
   ```
