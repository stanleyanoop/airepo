import sys
import os

import json
import warnings
from datetime import datetime
from dotenv import load_dotenv
from apply_util import JobApplyUtil
warnings.filterwarnings("ignore")

# Step 1: Load your .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
JSEARCH_API_KEY = os.getenv("x-rapidapi-key")
JSEARCH_API_HOST = os.getenv("x-rapidapi-host") 

if not GOOGLE_API_KEY or not JSEARCH_API_KEY:
    print("Error: GOOGLE_API_KEY or x-rapidapi-key not set in .env file.")
    raise ValueError("Missing API keys in .env file. The agent needs both google and rapid api keys to function properly.")

job_apply_util = JobApplyUtil(file_path="cnfg/job_search_config.json")
job_criteria = job_apply_util.load_job_criteria()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for job in job_criteria:
    if "job_title" not in job or "job_employment_type" not in job:
        print("Error: Job criteria is missing required fields.")
        raise ValueError("Job criteria must contain 'jobTitle', 'jobType', and 'keyWords'.")
    print("Loaded job criteria:" + job["job_title"]) 
    headers = {
        "x-rapidapi-key": JSEARCH_API_KEY, 
        "x-rapidapi-host": JSEARCH_API_HOST
    }
    weekday = datetime.today().weekday()
    print(f"Today is {weekday} (0=Monday, 6=Sunday)")
    date_posted = "3days" if weekday == 0 else "today"  # Default to 3 days, can be changed based on job criteria
    query = f"{job['job_title']} {' '.join(job['job_keywords'])}"
    params = {
        "query": query,
        "country": "us",
        "date_posted": date_posted,
        "employment_types": job["job_employment_type"],
        "sort_by": "relevance",
        "exclude_job_publishers": "BeeBe",
        "page": 1,
        "num_pages": 2
    }

    data = job_apply_util.search_jobs(headers=headers, params =params)
    if "data" not in data or len(data["data"]) == 0:
        print(f"Warning : No data found in the response for the params: {params}")
        continue
    
    print(f"✅ Found {len(data['data'])} result(s):\n")
    output_file = os.path.join(output_dir, f"output_{job['job_title'].replace(' ', '_')}.txt")  # Use os.path.join for cross-platform compatibility
    with open(output_file, "w") as f:
        for idx, job_entry in enumerate(data["data"], 1):
            print(f"🧩 Job #{idx}")
            job_entry = job_apply_util.rate_job(job, job_entry)
            job_details = (
                f"Title       : {job_entry.get('job_title')}\n"
                f"Company     : {job_entry.get('employer_name')}\n"
                f"Location    : {job_entry.get('job_city')}, {job_entry.get('job_country')}\n"
                f"Job Type    : {job_entry.get('job_employment_type')}\n"
                f"Apply Link  : {job_entry.get('job_apply_link')}\n"
                f"Rating      : {job_entry.get('rating', 'N/A')}\n"
                f"{'-' * 80}\n"
            )
            print(job_details)  # Print to console
            f.write(job_details)
    print(f"Results saved to {output_file}\n")