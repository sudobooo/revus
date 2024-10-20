# app/utils.py

import logging

def get_user_choice():
    choices = {'r': 're-review file', 'c': 'continue', 'q': 'quit'}
    while True:
        choice = input("Choose an action: (r) re-review file, (c) continue, (q) quit: ").lower()
        if choice in choices:
            return choice
        else:
            logging.warning("Invalid input. Please enter 'r', 'c', or 'q'.")
