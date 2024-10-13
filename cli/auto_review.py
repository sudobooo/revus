import logging
import argparse
from app.git_operations import get_changed_files
from app.review_manager import process_file

logging.basicConfig(level=logging.INFO)

def run_auto_review():
    parser = argparse.ArgumentParser(description="Автоматическое ревью PR с использованием OpenAI.")
    parser.add_argument('--files', nargs='*', help='Список файлов для ревью')
    args = parser.parse_args()

    logging.info("Начало процесса автоматического ревью.")
    files = args.files if args.files else get_changed_files()
    if not files:
        logging.info("Нет изменённых файлов для ревью.")
        return

    for file in files:
        process_file(file)

    logging.info("Завершение процесса автоматического ревью.")
