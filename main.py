# main.py

import logging
from cli.auto_review import run_auto_review

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    run_auto_review()
