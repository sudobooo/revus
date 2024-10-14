# app/review_manager.py

import logging
import json
from app.code_review import review_code, review_code_with_hints, read_file_content
from app.judge_review import judge_review
from app.assess_review_quality import assess_review_quality
from app.utils import get_user_choice, generate_final_report

def process_file(file):
    logging.info(f"\nReviewing file: {file}")
    file_content = read_file_content(file)
    print(file_content)
    if not file_content:
        return

    assessment_data = handle_review(file_content, file)
    if assessment_data is None:
        return

    if assess_review_quality(assessment_data) == 'low':
        logging.info(f"\nReview for file {file} failed the assessment.")
        user_choice = get_user_choice()

        if user_choice == 'r':
            assessment_data = handle_repeated_review(file_content, assessment_data, file)
            if assessment_data is None:
                return
            if assess_review_quality(assessment_data) != 'low':
                logging.info(f"\nReview for file {file} passed the assessment.")
            else:
                logging.info(f"\nReview for file {file} still failed the assessment. Providing final report.")
                final_report = generate_final_report(assessment_data)
                logging.info(final_report)
        elif user_choice == 'o':
            logging.info(f"\nProviding final report for file {file}.")
            final_report = generate_final_report(assessment_data)
            logging.info(final_report)
        elif user_choice == 'q':
            logging.info("Review process was interrupted by the user.")
    else:
        logging.info(f"\nReview for file {file} passed the assessment successfully.")

def handle_review(file_content, file):
    review = review_code(file_content)
    logging.info(f"\nReview results for file {file}:")
    logging.info(review)
    assessment = judge_review(review)
    try:
        assessment_data = json.loads(assessment)
    except json.JSONDecodeError:
        logging.error(f"\nError processing assessment for file {file}: {assessment}")
        return None
    logging.info(f"\nQuality assessment of the review for file {file}:")
    logging.info(json.dumps(assessment_data, indent=4, ensure_ascii=False))
    return assessment_data

def handle_repeated_review(file_content, assessment_data, file):
    logging.info(f"\nStarting repeated review for file {file} considering previous comments.")
    review = review_code_with_hints(file_content, assessment_data['comments'])
    logging.info(f"\nRepeated review results for file {file}:")
    logging.info(review)
    assessment = judge_review(review)
    try:
        assessment_data = json.loads(assessment)
    except json.JSONDecodeError:
        logging.error(f"\nError processing assessment for file {file}: {assessment}")
        return None
    logging.info(f"\nQuality assessment of the repeated review for file {file}:")
    logging.info(json.dumps(assessment_data, indent=4, ensure_ascii=False))
    return assessment_data
