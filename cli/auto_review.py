# cli/auto_review.py

import logging
import argparse
from app.git_operations import get_changed_files
from app.review_manager import process_file

logging.basicConfig(level=logging.INFO)

def run_auto_review():
    parser = argparse.ArgumentParser(description="Automatic PR review using OpenAI.")
    parser.add_argument('--files', nargs='*', help='List of files to review')
    args = parser.parse_args()

    logging.info("Starting the automatic review process.")
    files = args.files if args.files else get_changed_files()
    if not files:
        logging.info("No changed files to review.")
        return

    for file in files:
        process_file(file)

    logging.info("Automatic review process completed.")
