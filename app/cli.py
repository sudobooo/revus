# cli/cli.py

import logging
from app.review_manager import ReviewManager
from app.git_operations import GitOperations

class AutoReviewCLI:

    def __init__(self):
        self.review_manager = ReviewManager()

    def run(self):
        files_to_review = GitOperations.get_changed_files()
        if not files_to_review:
            logging.info("No files to review.")
            return

        for file in files_to_review:
            self.review_manager.process_file(file)
