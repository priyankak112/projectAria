# llm_config.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables once
load_dotenv()

# Your Google API key from .env
google_api_key = os.getenv("GOOGLE_API_KEY")

# Define the LLM instance
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=google_api_key
)
print("LLM initialized in llm_config.py:", llm.model)