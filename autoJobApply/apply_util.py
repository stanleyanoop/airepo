import json
import requests
import time
from ai_agent import JobSearchAgent

global job_search_agent
job_search_agent = JobSearchAgent()

class JobApplyUtil:
    def __init__(self, file_path="cnfg/job_search_config.json"):
        self.file_path = file_path
        self.job_criteria = self.load_job_criteria()

    def load_job_criteria(self):
        """
        This method loads job criteria from a JSON file.
        It reads the file and returns a list of job criteria.
        If the file does not exist or cannot be read, it returns an empty list."""
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading job criteria: {e}")
            return []
    # check the endpoint params and headers for future tuning @ 
    # https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/playground/endpoint_73845d59-2a15-4a88-92c5-e9b1bc90956d
    
    def search_jobs(self, headers, params):
        """
        This method searches for jobs based on the provided criteria.
        It uses the JSearch API to find jobs that match the criteria.
            :param headers: Headers for the API request, including API keys.
            :param params: Parameters for the job search, including query, country, date posted, employment types, etc.
        """
        JSEARCH_ENDPOINT = "https://jsearch.p.rapidapi.com/search"
        # Placeholder for job search logic
        print(f"Searching for jobs with params: {params}")
        # This method would typically call an API or search engine to find jobs based on the criteria
        response = requests.get(JSEARCH_ENDPOINT, headers=headers, params=params)
        data = response.json()
        # print(f"Response data: {data}")
        return data
    
    def rate_job(self, job_criteria, job_listing):
        """
        This method rates a job based on the provided criteria.
        It uses the JobSearchAgent - intelligent AI agent - 
        to get a rating score for the job.
            :param job_criteria: Criteria for the job search, including job title, type, and keywords.
            :param job_listing: Job listing to be rated, including job title, type, keywords, etc."""
        time.sleep(5)
        print ("Delaying 5 seconds before rating the job...")
        return job_search_agent.rate_job(job_criteria, job_listing)
        
if __name__ == "__main__":
    job_apply_util = JobApplyUtil("cnfg/job_search_config.json")
    job_criteria = job_apply_util.load_job_criteria()
    print("Loaded job criteria:")
    for job in job_criteria:
        print(job)