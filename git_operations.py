from git import Repo, InvalidGitRepositoryError, GitCommandError

def get_changed_files(file_types=None):
    try:
        repo = Repo('.')
        changed_files = [file for file in repo.git.diff('HEAD', name_only=True).split('\n') if file]
        new_files = [file.a_path for file in repo.index.diff(None) if file.change_type == 'A']
        all_files = list(set(changed_files + new_files))
    except (InvalidGitRepositoryError, GitCommandError) as e:
        print(f"Ошибка: {e}")
        return []

    if file_types:
        all_files = [file for file in all_files if any(file.endswith(ext) for ext in file_types)]

    return all_files
