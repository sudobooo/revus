import logging
import json
from git_operations import get_changed_files
from code_review import review_code, review_code_with_hints, read_file_content
from judge_review import judge_review
from assess_review_quality import assess_review_quality

logging.basicConfig(level=logging.INFO)

def get_user_choice():
    while True:
        choice = input("Выберите действие: (r) повторить ревью, (o) получить отчёт: ").lower()
        if choice in ['r', 'o']:
            return choice
        else:
            print("Некорректный ввод. Пожалуйста, введите 'r' или 'o'.")

def generate_final_report(assessment):
    report = []
    report.append("Финальный отчёт о ревью:")
    report.append(json.dumps(assessment, indent=4, ensure_ascii=False))
    return "\n".join(report)

def run_auto_review():
    print("Запуск функции run_auto_review...")  # Отладочное сообщение для проверки запуска
    logging.info("Начало процесса автоматического ревью.")
    files = get_changed_files(['.py'])
    if not files:
        print("Нет изменённых файлов для ревью.")
        return

    for file in files:
        print(f"\nРевью файла: {file}")
        file_content = read_file_content(file)
        if not file_content:
            continue

        review = review_code(file_content)
        print(f"\nРезультаты ревью файла {file}:\n{review}")

        assessment = judge_review(review)
        try:
            assessment_data = json.loads(assessment)
        except json.JSONDecodeError:
            print(f"\nОшибка при обработке оценки для файла {file}: {assessment}")
            continue

        print(f"\nОценка качества ревью файла {file}:\n{json.dumps(assessment_data, indent=4, ensure_ascii=False)}")

        if assess_review_quality(assessment_data) == 'low':
            print(f"\nРевью файла {file} не прошло по оценке.")
            user_choice = get_user_choice()

            if user_choice == 'r':
                print(f"\nЗапускаем повторное ревью файла {file} с учётом предыдущих комментариев.")
                review = review_code_with_hints(file_content, assessment_data['comments'])
                print(f"\nРезультаты повторного ревью файла {file}:\n{review}")
                assessment = judge_review(review)
                try:
                    assessment_data = json.loads(assessment)
                except json.JSONDecodeError:
                    print(f"\nОшибка при обработке оценки для файла {file}: {assessment}")
                    continue
                print(f"\nОценка качества повторного ревью файла {file}:\n{json.dumps(assessment_data, indent=4, ensure_ascii=False)}")

                if assess_review_quality(assessment_data) != 'low':
                    print(f"\nРевью файла {file} успешно пройдено по оценке.")
                else:
                    print(f"\nРевью файла {file} всё ещё не прошло по оценке. Предоставляем финальный отчёт.")
                    final_report = generate_final_report(assessment_data)
                    print(f"\n{final_report}")
            else:
                print(f"\nПредоставляем финальный отчёт для файла {file}.")
                final_report = generate_final_report(assessment_data)
                print(f"\n{final_report}")
        else:
            print(f"\nРевью файла {file} прошло успешно по оценке.")
    logging.info("Завершение процесса автоматического ревью.")

if __name__ == "__main__":
    run_auto_review()
