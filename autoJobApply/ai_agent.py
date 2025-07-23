import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class JobSearchAgent:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GOOGLE_API_KEY_SECOND = os.getenv("GOOGLE_API_KEY_SECOND")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=self.GOOGLE_API_KEY)


    def get_agent_rating(self, job_criteria, job_listing):

        job_title = job_listing.get('job_title', '')
        job_type = job_listing.get('job_employment_type', '')
        key_words = job_listing.get('job_keywords', [])

        title_criteria = job_criteria.get('job_title', '')
        type_criteria = job_criteria.get('job_employment_type', '')
        keywords_criteria = job_criteria.get('job_keywords', [])

        print(f"Rating score for job '{job_title}' being assessed by the JobSearchAgent.")
        prompt_str = """
            You are a Job matching AI. Rate the job based on the following criteria in a scale of 1 (Poor Match) to 10 ((Perfect Match)):
            
            Job Listing:
                Job Title: {job_title}
                Job Type: {job_type}
                Key Words: {key_words}
            
            User Criteria:
                Title Criteria: {title_criteria}
                Type Criteria: {type_criteria}
                Keywords Criteria: {keywords_criteria}
            And return only the rating score as an integer.
        """
        prompt = PromptTemplate.from_template(prompt_str)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        try:
            score = chain.run({
                'job_title': job_title,
                'job_type': job_type,
                'key_words': ', '.join(key_words),
                'title_criteria': title_criteria,
                'type_criteria': type_criteria,
                'keywords_criteria': ', '.join(keywords_criteria)
            })
        except Exception as e:
            print(f"Error while getting rating score: {e}")
            # retry once with a different api key
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=self.GOOGLE_API_KEY_SECOND)
            chain = LLMChain(llm=self.llm, prompt=prompt)
            score = chain.run({
                'job_title': job_title,
                'job_type': job_type,
                'key_words': ', '.join(key_words),
                'title_criteria': title_criteria,
                'type_criteria': type_criteria,
                'keywords_criteria': ', '.join(keywords_criteria)
            })
        print(f"Rating score for job '{job_title}': {score}")
        return score
    
    def rate_job(self, job_criteria, job_listing):
        """
        Rate the job based on the criteria.
        This is a placeholder for the actual rating logic.
        """
        print(f"Rating job: {job_listing.get('job_title')} based on criteria: {job_criteria}")
        # For now, just print the job title and criteria
        print(f"Job Title: {job_listing.get('job_title')}, Criteria: {job_criteria['job_title']}")
        rating_score = self.get_agent_rating(job_criteria, job_listing)  # Placeholder score, replace with actual logic
        job_listing['rating'] = rating_score
        
        return job_listing