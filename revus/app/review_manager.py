# app/review_manager.py

import json
from .code_reviewer import CodeReviewer
from .review_assessor import ReviewAssessor
from .file_reader import read_file_content
from .utils import get_user_choice
from .logger import log_info, log_error, log_success

class ReviewManager:

    def __init__(self):
        self.code_reviewer = CodeReviewer()
        self.review_assessor = ReviewAssessor()

    def process_file(self, file_path):
        file_content = read_file_content(file_path)
        if not file_content:
            return

        review = self.code_reviewer.review_code(file_content)
        log_info(f"\n[bold]Review results for file {file_path}:[/bold]\n{review}")

        while True:
            assessment = self.review_assessor.judge_review(review)
            try:
                assessment_data = json.loads(assessment)
            except json.JSONDecodeError:
                log_error(f"Error processing assessment for file {file_path}: {assessment}")
                return

            log_info(f"\n[bold]Quality assessment of the review for file {file_path}:[/bold]\n{json.dumps(assessment_data, indent=4, ensure_ascii=False)}")

            user_choice = get_user_choice()

            if user_choice == 'r':
                review = self.code_reviewer.review_code(file_content, assessment_data.get('comments'))
                log_info(f"\n[bold]Re-review results for file {file_path}:[/bold]\n{review}")
            elif user_choice == 'c':
                log_success("Continuing with the next steps.")
                break
            elif user_choice == 'q':
                log_info("Review process was interrupted by the user.")
                exit()
