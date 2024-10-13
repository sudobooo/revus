import logging
import json
from app.code_review import review_code, review_code_with_hints, read_file_content
from app.judge_review import judge_review
from app.assess_review_quality import assess_review_quality
from app.utils import get_user_choice, generate_final_report

def process_file(file):
    logging.info(f"\nРевью файла: {file}")
    file_content = read_file_content(file)
    print(file_content)
    if not file_content:
        return

    assessment_data = handle_review(file_content, file)
    if assessment_data is None:
        return

    if assess_review_quality(assessment_data) == 'low':
        logging.info(f"\nРевью файла {file} не прошло по оценке.")
        user_choice = get_user_choice()

        if user_choice == 'r':
            assessment_data = handle_repeated_review(file_content, assessment_data, file)
            if assessment_data is None:
                return
            if assess_review_quality(assessment_data) != 'low':
                logging.info(f"\nРевью файла {file} успешно пройдено по оценке.")
            else:
                logging.info(f"\nРевью файла {file} всё ещё не прошло по оценке. Предоставляем финальный отчёт.")
                final_report = generate_final_report(assessment_data)
                logging.info(final_report)
        elif user_choice == 'o':
            logging.info(f"\nПредоставляем финальный отчёт для файла {file}.")
            final_report = generate_final_report(assessment_data)
            logging.info(final_report)
        elif user_choice == 'q':
            logging.info("Процесс ревью был прерван пользователем.")
    else:
        logging.info(f"\nРевью файла {file} прошло успешно по оценке.")

def handle_review(file_content, file):
    review = review_code(file_content)
    logging.info(f"\nРезультаты ревью файла {file}:")
    logging.info(review)
    assessment = judge_review(review)
    try:
        assessment_data = json.loads(assessment)
    except json.JSONDecodeError:
        logging.error(f"\nОшибка при обработке оценки для файла {file}: {assessment}")
        return None
    logging.info(f"\nОценка качества ревью файла {file}:")
    logging.info(json.dumps(assessment_data, indent=4, ensure_ascii=False))
    return assessment_data

def handle_repeated_review(file_content, assessment_data, file):
    logging.info(f"\nЗапускаем повторное ревью файла {file} с учётом предыдущих комментариев.")
    review = review_code_with_hints(file_content, assessment_data['comments'])
    logging.info(f"\nРезультаты повторного ревью файла {file}:")
    logging.info(review)
    assessment = judge_review(review)
    try:
        assessment_data = json.loads(assessment)
    except json.JSONDecodeError:
        logging.error(f"\nОшибка при обработке оценки для файла {file}: {assessment}")
        return None
    logging.info(f"\nОценка качества повторного ревью файла {file}:")
    logging.info(json.dumps(assessment_data, indent=4, ensure_ascii=False))
    return assessment_data
