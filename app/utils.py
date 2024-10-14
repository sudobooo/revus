# app/utils.py

import os
import toml
import logging
import json

def load_config():
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

def get_user_choice():
    while True:
        choice = input("Choose an action: (r) repeat review, (o) get report, (q) quit: ").lower()
        if choice in ['r', 'o', 'q']:
            return choice
        else:
            logging.warning("Invalid input. Please enter 'r', 'o', or 'q'.")

def generate_final_report(assessment):
    report = []
    report.append("Final review report:")
    report.append(json.dumps(assessment, indent=4, ensure_ascii=False))
    return "\n".join(report)
