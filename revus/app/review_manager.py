# app/review_manager.py

from .code_reviewer import CodeReviewer
from .logger import log_info, log_success
from .cli import get_user_choice, format_review_output


class ReviewManager:
    def __init__(self):
        self.code_reviewer = CodeReviewer()

    def process_file(self, file_path, changes):
        review = self.code_reviewer.review_code(changes)
        formatted_review = format_review_output(review)
        log_info(
            f"\n[bold]Review results for file {file_path}:[/bold]\n{formatted_review}"
        )

        while True:
            user_choice = get_user_choice()

            if user_choice == "r":
                review = self.code_reviewer.review_code(changes)
                formatted_review = format_review_output(review)
                log_info(
                    f"\n[bold]Re-review results for file {file_path}:[/bold]\n{formatted_review}"
                )
            elif user_choice == "c":
                log_success("Continuing with the next steps.")
                break
            elif user_choice == "q":
                log_info("Review process was interrupted by the user.")
                exit()
