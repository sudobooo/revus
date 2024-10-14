# main.py

import logging
from app.cli import AutoReviewCLI


def main():
    logging.basicConfig(level=logging.INFO)
    auto_review_cli = AutoReviewCLI()
    auto_review_cli.run()

if __name__ == "__main__":
    main()
