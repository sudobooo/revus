import logging
import os
from git import Repo, InvalidGitRepositoryError, GitCommandError
from app.utils import load_config

config = load_config()

def get_changed_files(file_types=None):
    try:
        repo = Repo('.')
        staged_files = list({item.a_path for item in repo.index.diff("HEAD", staged=True)})
        staged_files = [file for file in staged_files if os.path.exists(file)]
    except (InvalidGitRepositoryError, GitCommandError) as e:
        logging.error(f"Ошибка работы с репозиторием Git: {e}")
        return []

    file_types = file_types or config.get("file_types", [".py"])
    exclude_paths = config.get("exclude_paths", [])

    filtered_files = [file for file in staged_files if any(file.endswith(ext) for ext in file_types)]

    if exclude_paths:
        filtered_files = [file for file in filtered_files if not any(file.startswith(path) for path in exclude_paths)]

    return filtered_files
