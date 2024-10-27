# app/llm_client.py

import sys
from langchain_openai import ChatOpenAI
from .config import get_config
from .logger import log_error

_llm_instance = None


def _initialize_llm(params=None):
    params = params or {}
    api_key = get_config("OPENAI_API_KEY")

    if not api_key:
        log_error(
            "You need to create a config.toml file and add your OPENAI_API_KEY there."
        )
        sys.exit(1)
    model_name = get_config("model_name", "gpt-4o-mini")
    try:
        return ChatOpenAI(model=model_name, api_key=api_key, **params)
    except Exception as e:
        log_error(f"Error initializing LLM: {e}")
        sys.exit(1)


def get_llm(params=None):
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = _initialize_llm(params)
    return _llm_instance


__all__ = ["get_llm"]
