# app/shared_llm.py

import sys
from langchain_openai import ChatOpenAI
from app.utils import load_config
import logging

config = load_config()

def get_llm():
    api_key = config.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("You need to create a config.toml file and add your OPENAI_API_KEY there.")
        sys.exit(1)
    return ChatOpenAI(model_name=config.get("model_name", 'gpt-4o-mini'), openai_api_key=api_key)
