import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def get_llm():
    """
    Initializes and returns the primary LLM.
    """
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    return llm