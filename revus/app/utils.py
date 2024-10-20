# app/utils.py

from .logger import log_warning, console


def get_user_choice():
    choices = {"r": "re-review file", "c": "continue", "q": "quit"}
    while True:
        choice = console.input(
            "[bold blue]Choose an action: (r) re-review file, (c) continue, (q) quit: [/bold blue]"
        ).lower()
        if choice in choices:
            return choice
        else:
            log_warning("Invalid input. Please enter 'r', 'c', or 'q'.")
