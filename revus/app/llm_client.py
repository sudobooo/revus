# app/llm_client.py

import sys
import logging
from langchain_openai import ChatOpenAI
from .config import get

_llm_instance = None

def _initialize_llm():
    api_key = get("OPENAI_API_KEY")
    if not api_key:
        logging.error("You need to create a config.toml file and add your OPENAI_API_KEY there.")
        sys.exit(1)
    model_name = get("model_name", 'gpt-4')
    try:
        return ChatOpenAI(model_name=model_name, openai_api_key=api_key)
    except Exception as e:
        logging.error(f"Error initializing LLM: {e}")
        sys.exit(1)

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = _initialize_llm()
    return _llm_instance

__all__ = ['get_llm']
