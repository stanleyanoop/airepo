
import unittest
from unittest.mock import MagicMock
from apply_util import JobApplyUtil
from ai_agent import JobSearchAgent

class TestUtils(unittest.TestCase):
    def setUp(self):
        util = JobApplyUtil(file_path="cnfg/job_search_config.json")
        self.job_criteria = util.load_job_criteria()
        self.job_criteria = [
            {
                "job_title": "Software Engineer",
                "job_employment_type": "Full-time",
                "job_keywords": ["Python", "Django", "REST"],
                "exclude_keywords": ["Remote"]
            }
        ]
        self.job_listing = {
            "job_title": "Senior Software Engineer",
            "job_description": "Looking for a skilled Python developer with experience in Django and REST APIs.",
            "job_employment_type": "Full-time",
            "job_keywords": ["Python", "Django", "REST"]
        }
        self.mock_llm = MagicMock()
        self.mock_llm.invoke.return_value = "8"
    
    def test_load_job_criteria(self):
        for job in self.job_criteria:
            self.assertIn("job_title", job, "Job title should be present")
            self.assertIn("job_employment_type", job, "Job type should be present")
            self.assertIn("job_keywords", job, "Job keywords should be present")
    
    def test_rate_job(self):
        agent = JobSearchAgent()
        agent.llm = self.mock_llm
            
if __name__ == "__main__":
    unittest.main()