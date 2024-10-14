# app/config.py

import os
import toml
import logging

class Config:
    _instance = None

    def __init__(self):
        self.config = self.load_config()

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

    def load_config(self):
        config_path = os.path.join(os.getcwd(), "config.toml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as config_file:
                    return toml.load(config_file)
            except Exception as e:
                logging.error(f"Error loading configuration file: {e}")
                return {}
        else:
            logging.warning("Configuration file not found, default values will be used.")
            return {}

    def get(self, key, default=None):
        return self.config.get(key, default)
