# app/review_manager.py

import logging
import json
from .code_reviewer import CodeReviewer
from .review_assessor import ReviewAssessor
from .file_reader import read_file_content
from .utils import get_user_choice

class ReviewManager:

    def __init__(self):
        self.code_reviewer = CodeReviewer()
        self.review_assessor = ReviewAssessor()

    def process_file(self, file_path):
        file_content = read_file_content(file_path)
        if not file_content:
            return

        review = self.code_reviewer.review_code(file_content)
        logging.info(f"\nReview results for file {file_path}:\n{review}")

        while True:
            assessment = self.review_assessor.judge_review(review)
            try:
                assessment_data = json.loads(assessment)
            except json.JSONDecodeError:
                logging.error(f"Error processing assessment for file {file_path}: {assessment}")
                return

            logging.info(f"\nQuality assessment of the review for file {file_path}:\n{json.dumps(assessment_data, indent=4, ensure_ascii=False)}")

            user_choice = get_user_choice()

            if user_choice == 'r':
                review = self.code_reviewer.review_code(file_content, assessment_data.get('comments'))
                logging.info(f"\nRe-review results for file {file_path}:\n{review}")
            elif user_choice == 'c':
                break
            elif user_choice == 'q':
                logging.info("Review process was interrupted by the user.")
                exit()
