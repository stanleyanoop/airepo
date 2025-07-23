import os
import json
import unittest
from applyUtil import JobApplyUtil

class TestUtils(unittest.TestCase):
    def setUp(self):
        util = JobApplyUtil(file_path="cnfg/job_search_config.json")
        self.job_criteria = util.load_job_criteria()
    
    def test_load_job_criteria(self):
        for job in self.job_criteria:
            self.assertIn("jobTitle", job, "Job title should be present")
            self.assertIn("jobType", job, "Job type should be present")
            self.assertIn("keyWords", job, "Job keywords should be present")
            
if __name__ == "__main__":
    unittest.main()