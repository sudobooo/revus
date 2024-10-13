import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Необходимо указать OPENAI_API_KEY")
    return ChatOpenAI(model_name='gpt-4', openai_api_key=api_key)
