import os
import toml
import logging
import json

def load_config():
    config_path = os.path.join(os.getcwd(), "config.toml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as config_file:
                return toml.load(config_file)
        except Exception as e:
            logging.error(f"Ошибка при загрузке конфигурационного файла: {e}")
            return {}
    else:
        logging.warning("Конфигурационный файл не найден, будут использованы значения по умолчанию.")
        return {}

def get_user_choice():
    while True:
        choice = input("Выберите действие: (r) повторить ревью, (o) получить отчёт, (q) выйти: ").lower()
        if choice in ['r', 'o', 'q']:
            return choice
        else:
            logging.warning("Некорректный ввод. Пожалуйста, введите 'r', 'o', или 'q'.")

def generate_final_report(assessment):
    report = []
    report.append("Финальный отчёт о ревью:")
    report.append(json.dumps(assessment, indent=4, ensure_ascii=False))
    return "\n".join(report)
