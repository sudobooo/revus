# app/review_executor.py

from .review_manager import ReviewManager
from .git_operations import get_file_changes
from .logger import log_info, log_success


def review_files():
    files_to_review = get_file_changes()

    if not files_to_review:
        log_info("No files to review.")
        return

    log_info(f"Found {len(files_to_review)} files to review.")
    review_manager = ReviewManager()

    for file, changes in files_to_review.items():
        review_manager.process_file(file, changes)

    log_success("All files have been reviewed.")
