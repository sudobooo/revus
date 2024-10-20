# cli/cli.py

from .review_manager import ReviewManager
from .git_operations import get_changed_files
from .logger import log_info, log_success

def review_changed_files():
    files_to_review = get_changed_files()

    if not files_to_review:
        log_info("No files to review.")
        return

    log_info(f"Found {len(files_to_review)} files to review.")
    review_manager = ReviewManager()

    for file in files_to_review:
        review_manager.process_file(file)

    log_success("All files have been reviewed.")
