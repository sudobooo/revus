# app/utils.py

import json
import logging

class Utils:

    @staticmethod
    def get_user_choice():
        choices = {'r': 're-review file', 'c': 'continue', 'q': 'quit'}
        while True:
            choice = input("Choose an action: (r) re-review file, (c) continue, (q) quit: ").lower()
            if choice in choices:
                return choice
            else:
                logging.warning("Invalid input. Please enter 'r', 'c', or 'q'.")

    @staticmethod
    def generate_final_report(assessment):
        report = ["Final review report:", json.dumps(assessment, indent=4, ensure_ascii=False)]
        return "\n".join(report)
