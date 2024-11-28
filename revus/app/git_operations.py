# app/git_operations.py

import os
import sys
from typing import Dict, List, Union
from git import Repo, InvalidGitRepositoryError, GitCommandError
from .config import get_config
from .logger import log_error
from .cli import parse_cli_args


def _get_changed_files(repo: Repo) -> Dict[str, List[str]]:
    """Retrieve the lists of changed files in the Git repository."""
    try:
        staged_files = [item.a_path for item in repo.index.diff("HEAD", staged=True)]
        unstaged_files = repo.git.diff(name_only=True).splitlines()
        new_files = repo.untracked_files
        return {
            "staged": staged_files,
            "unstaged": unstaged_files,
            "new": new_files,
        }
    except (InvalidGitRepositoryError, GitCommandError) as e:
        log_error(f"Error working with Git repository: {e}")


def _filter_changed_files(
    files: Dict[str, List[str]],
    requested_path: str,
    file_types: List[str],
    exclude_paths: List[str],
) -> Dict[str, List[str]]:
    """Filter changed files based on the requested path, file types, and excluded paths."""
    filtered_files = {}

    for change_type, file_paths in files.items():
        filtered_paths = []
        for path in file_paths:
            if not os.path.exists(path):
                continue
            if requested_path and not path.startswith(requested_path):
                continue
            if not any(path.endswith(ext) for ext in file_types):
                continue
            if any(path.startswith(exclude_path) for exclude_path in exclude_paths):
                continue

            filtered_paths.append(path)

        filtered_files[change_type] = filtered_paths

    return filtered_files


def _get_changes(
    repo: Repo, changed_files: Dict[str, List[str]]
) -> Dict[str, Dict[str, Union[str, None]]]:
    """Retrieve changes for files (staged, unstaged, new) in the repository."""
    changes = {}
    for status, files in changed_files.items():
        for path in files:
            try:
                with open(path, "r") as f:
                    file_content = f.read()
            except Exception as e:
                log_error(f"Error reading file {path}: {e}")
                sys.exit(1)

            file_diff: Union[str, None] = None
            if status == "staged":
                file_diff = repo.git.diff("HEAD", path, staged=True)
            elif status == "unstaged":
                file_diff = repo.git.diff(path)
            elif status == "new":
                file_diff = file_content
            changes[path] = {
                "changes_in_file": file_diff,
                "file_content": file_content,
            }

    return changes


def get_file_changes() -> Dict[str, Dict[str, Union[str, None]]]:
    """Retrieve changes for files in the repository."""
    try:
        repo = Repo(".")
    except (InvalidGitRepositoryError, GitCommandError) as e:
        log_error(f"Error working with Git repository: {e}")
        return {}

    changed_files = _get_changed_files(repo)

    args = parse_cli_args()
    requested_path = args.path

    file_types = get_config("file_types", [".py"])
    exclude_paths = get_config("exclude_paths", [])

    filtered_files = _filter_changed_files(
        changed_files, requested_path, file_types, exclude_paths
    )

    return _get_changes(repo, filtered_files)
