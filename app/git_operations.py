# app/git_operations.py

import logging
import os
from git import Repo, InvalidGitRepositoryError, GitCommandError
from app.config import Config

class GitOperations:

    @staticmethod
    def get_changed_files():
        try:
            repo = Repo('.')
            staged_files = {item.a_path for item in repo.index.diff("HEAD", staged=True)}
            staged_files = [file for file in staged_files if os.path.exists(file)]
        except (InvalidGitRepositoryError, GitCommandError) as e:
            logging.error(f"Error working with Git repository: {e}")
            return []

        config = Config.get_instance()
        file_types = config.get("file_types", [".py"])
        exclude_paths = config.get("exclude_paths", [])

        filtered_files = [file for file in staged_files if any(file.endswith(ext) for ext in file_types)]
        filtered_files = [file for file in filtered_files if not any(file.startswith(path) for path in exclude_paths)]

        return filtered_files
