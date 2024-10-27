# app/git_operations.py

import os
import sys
from git import Repo, InvalidGitRepositoryError, GitCommandError
from .config import get_config
from .logger import log_error


def get_file_changes():
    try:
        repo = Repo(".")
        staged_files = {item.a_path for item in repo.index.diff("HEAD", staged=True)}
        staged_files = [file for file in staged_files if os.path.exists(file)]
    except (InvalidGitRepositoryError, GitCommandError) as e:
        log_error(f"Error working with Git repository: {e}")
        return {}

    file_types = get_config("file_types", [".py"])
    exclude_paths = get_config("exclude_paths", [])

    filtered_files = [
        file for file in staged_files if any(file.endswith(ext) for ext in file_types)
    ]
    filtered_files = [
        file
        for file in filtered_files
        if not any(file.startswith(path) for path in exclude_paths)
    ]

    changes = {}
    for file in filtered_files:
        try:
            with open(file, "r") as f:
                file_content = f.read()
        except Exception as e:
            log_error(f"Error reading file {file}: {e}")
            sys.exit(1)

        file_diff = repo.git.diff("HEAD", file, staged=True)

        changes[file] = {"changes_in_file": file_diff, "file_content": file_content}

    return changes
