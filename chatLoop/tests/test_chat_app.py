import os
import json
import unittest
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
'''
This class is for testing the ChatGoogleGenerativeAI model.
Steps to run the tests:
1. Ensure you have a .env file with your GOOGLE_API_KEY.
2. Navigate to the parent directory containing this app script (chatLoop in this case).
3. Run the tests using the command:
    python -m unittest discover -s tests -v
'''
load_dotenv()

class TestChatApp(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=self.api_key)

    def test_llm_response(self):
        prompt = "Say hello!"
        response = self.model.invoke(prompt)
        self.assertIsInstance(response, AIMessage)
        self.assertIn("hello", response.content.lower())

    def test_memory_file_creation(self):
        test_file = "test_memory.json"
        test_data = [{"user": "Hi", "ai": "Hello there!"}]
        with open(test_file, "w") as f:
            json.dump(test_data, f)

        self.assertTrue(os.path.exists(test_file))

        with open(test_file, "r") as f:
            loaded = json.load(f)
            self.assertEqual(loaded[0]["user"], "Hi")
            self.assertEqual(loaded[0]["ai"], "Hello there!")

        os.remove(test_file)

    def test_dynamic_response(self):
        prompt = "Give me 3 interesting facts about space."
        response = self.model.invoke(prompt)
        self.assertIsInstance(response, AIMessage)
        
        # Check that response has at least 3 numbered items or bullet points
        lines = response.content.strip().split("\n")
        self.assertGreaterEqual(len(lines), 3)
        
        # Optionally check for presence of space-related words
        keywords = ["galaxy", "planet", "star", "vacuum", "universe"]
        content_lower = response.content.lower()
        self.assertTrue(any(kw in content_lower for kw in keywords))

if __name__ == "__main__":
    unittest.main()