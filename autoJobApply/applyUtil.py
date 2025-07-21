import json
import requests

class JobApplyUtil:
    def __init__(self, file_path="cnfg/job_search_config.json"):
        self.file_path = file_path
        self.job_criteria = self.load_job_criteria()

    def load_job_criteria(self):
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
        JSEARCH_ENDPOINT = "https://jsearch.p.rapidapi.com/search"

        # Placeholder for job search logic
        print(f"Searching for jobs with params: {params}")
        # This method would typically call an API or search engine to find jobs based on the criteria
        response = requests.get(JSEARCH_ENDPOINT, headers=headers, params=params)
        data = response.json()
        print(f"Response data: {data}")
        # conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
        # conn.request("GET", f"/search?query={job_title}&type={job_type}&keywords={keywords}", headers=headers)
        # res = conn.getresponse()
        # data = res.read()
        return data

if __name__ == "__main__":
    job_apply_util = JobApplyUtil("cnfg/job_search_config.json")
    job_criteria = job_apply_util.load_job_criteria()
    print("Loaded job criteria:")
    for job in job_criteria:
        print(job)