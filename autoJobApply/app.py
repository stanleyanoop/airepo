import sys
import os

import json
import warnings
from dotenv import load_dotenv
from applyUtil import JobApplyUtil
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

for job in job_criteria:
    if "jobTitle" not in job or "jobType" not in job:
        print("Error: Job criteria is missing required fields.")
        raise ValueError("Job criteria must contain 'jobTitle', 'jobType', and 'keyWords'.")
    print("Loaded job criteria:" + job["jobTitle"]) 
    headers = {
        "x-rapidapi-key": JSEARCH_API_KEY, 
        "x-rapidapi-host": JSEARCH_API_HOST
    }
    query = f"{job['jobTitle']} {' '.join(job['keyWords'])}"
    params = {
        "query": query,
        "country": "us",
        "date_posted": "3days",
        "employment_types": job["jobType"],
        "sort_by": "relevance",
        "page": 1,
        "num_pages": 1
    }

    data = job_apply_util.search_jobs(headers=headers, params =params)
    if "data" not in data or len(data["data"]) == 0:
        print(f"Warning : No data found in the response for the params: {params}")
        continue
    
    print(f"✅ Found {len(data['data'])} result(s):\n")
    for idx, job_entry in enumerate(data["data"], 1):
        print(f"🧩 Job #{idx}")
        print(f"Title       : {job_entry.get('job_title')}")
        print(f"Company     : {job_entry.get('employer_name')}")
        print(f"Location    : {job_entry.get('job_city')}, {job_entry.get('job_country')}")
        print(f"Job Type    : {job_entry.get('job_employment_type')}")
        print(f"Apply Link  : {job_entry.get('job_apply_link')}")
        print(f"Description :\n{job_entry.get('job_description')[:500]}...")  # Trimmed for readability
        print("-" * 80)

