import sys
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

TOKEN_PROMPT = sys.argv[1] if len(sys.argv) > 1 else None

# Step 1: Load your .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Step 2: Set up the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)

# Step 3: Run a simple prompt
if TOKEN_PROMPT:
	response = llm.invoke(TOKEN_PROMPT)
else:
	response = llm.invoke("What are three interesting facts about space?")
print(response.content)
