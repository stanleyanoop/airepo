import sys
import os
import json
import warnings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

warnings.filterwarnings("ignore")
# Function to load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

# Function to save memory to file
def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f)
        
TOKEN_PROMPT = sys.argv[1] if len(sys.argv) > 1 else None

# Step 1: Load your .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
MEMORY_FILE = "chat_memory.json"

# Initialize memory and load previous conversation
history = load_memory()
memory = ConversationBufferMemory()
for message in history:
    memory.chat_memory.add_user_message(message["user"])
    memory.chat_memory.add_ai_message(message["ai"])


# Step 2: Set up the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)
# Initialize memory and load previous conversation
history = load_memory()
memory = ConversationBufferMemory()
for message in history:
    memory.chat_memory.add_user_message(message["user"])
    memory.chat_memory.add_ai_message(message["ai"])

# Build chain
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

print("🤖 Gemini Terminal Chat (type 'exit' to quit)\n")

# Chat loop
while True:
    user_input = input("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n🧑 You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = conversation.run(user_input)
    print(f"\n\n🤖 AI: {response}")

    # Save chat to file
    history.append({"user": user_input, "ai": response})
    save_memory(history)

print("👋 Session ended. Chat history saved.")
# # Step 3: Run a simple prompt
# if TOKEN_PROMPT:
# 	response = llm.invoke(TOKEN_PROMPT)
# else:
# 	response = llm.invoke("What are three interesting facts about space?")
# print(response.content)
