# app/file_reader.py

from .logger import log_error


def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        log_error(f"Error reading file {file_path}: {e}")
        return ""
