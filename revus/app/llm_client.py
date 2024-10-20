# app/llm_client.py

import sys
import logging
from langchain_openai import ChatOpenAI
from .config import Config

class LLMClient:
    _instance = None

    def __init__(self):
        self.llm = self.initialize_llm()

    @staticmethod
    def get_instance():
        if LLMClient._instance is None:
            LLMClient._instance = LLMClient()
        return LLMClient._instance

    def initialize_llm(self):
        config = Config.get_instance()
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            logging.error("You need to create a config.toml file and add your OPENAI_API_KEY there.")
            sys.exit(1)
        model_name = config.get("model_name", 'gpt-4')
        try:
            return ChatOpenAI(model_name=model_name, openai_api_key=api_key)
        except Exception as e:
            logging.error(f"Error initializing LLM: {e}")
            sys.exit(1)

    def get_llm(self):
        return self.llm
