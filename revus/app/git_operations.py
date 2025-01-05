# app/git_operations.py

import os
from typing import Dict, List, Union
from git import Repo, InvalidGitRepositoryError, GitCommandError
from .config import get_config
from .logger import log_error
from .cli import parse_cli_args


def _get_changed_files(repo: Repo) -> Dict[str, List[str]]:
    """Retrieve the lists of changed files in the Git repository."""
    changed_files = {
        "staged": [],
        "unstaged": [],
        "new": [],
    }
    try:
        staged_diff = repo.index.diff("HEAD", staged=True)
        changed_files["staged"] = [item.a_path for item in staged_diff]

        unstaged_diff = repo.git.diff(name_only=True).splitlines()
        changed_files["unstaged"] = unstaged_diff

        changed_files["new"] = repo.untracked_files
    except (InvalidGitRepositoryError, GitCommandError) as e:
        log_error(f"Error working with Git repository: {e}")

    return changed_files


def _filter_files(
    files: Dict[str, List[str]],
    requested_path: str,
    file_types: List[str],
    exclude_paths: List[str],
) -> Dict[str, List[str]]:
    """Filter files based on criteria."""
    filtered_files = {}

    for change_type, paths in files.items():
        filtered_paths = []
        for path in paths:
            path_exists = os.path.exists(path)
            is_in_requested_path = not requested_path or path.startswith(requested_path)
            matches_file_types = any(path.endswith(ext) for ext in file_types)
            not_excluded = not any(
                path.startswith(exclude_path) for exclude_path in exclude_paths
            )
            if all(
                [path_exists, is_in_requested_path, matches_file_types, not_excluded]
            ):
                filtered_paths.append(path)

        filtered_files[change_type] = filtered_paths

    return filtered_files


def _read_file_content(path: str) -> str:
    """Read the content of a file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        log_error(f"Error reading file {path}: {e}")
        return ""


def _get_file_diff(repo: Repo, path: str, status: str) -> Union[str, None]:
    """Get the diff for a file based on its status."""

    try:
        match status:
            case "staged":
                return repo.git.diff("HEAD", path, staged=True)
            case "unstaged":
                return repo.git.diff(path)
            case "new":
                return None
            case _:
                log_error(f"Unknown file status '{status}' for file {path}.")
                return None
    except GitCommandError as e:
        log_error(f"Error getting diff for file {path}: {e}")
        return None


def _get_changes(
    repo: Repo, changed_files: Dict[str, List[str]]
) -> Dict[str, Dict[str, Union[str, None]]]:
    """Retrieve changes for files (staged, unstaged, new) in the repository."""
    changes = {}
    for status, files in changed_files.items():
        for path in files:
            file_content = _read_file_content(path)
            file_diff = _get_file_diff(repo, path, status)

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
    if not changed_files:
        return {}

    args = parse_cli_args()
    requested_path = args.path

    file_types = get_config("file_types", [".py"])
    exclude_paths = get_config("exclude_paths", [])

    filtered_files = _filter_files(
        changed_files, requested_path, file_types, exclude_paths
    )

    return _get_changes(repo, filtered_files)
