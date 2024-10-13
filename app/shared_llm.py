import sys
from langchain_openai import ChatOpenAI
from app.utils import load_config
import logging

config = load_config()

def get_llm():
    api_key = config.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("Необходимо создать файл config.toml и добавить туда свой OPENAI_API_KEY")
        sys.exit(1)
    return ChatOpenAI(model_name=config.get("model_name", 'gpt-4'), openai_api_key=api_key)
