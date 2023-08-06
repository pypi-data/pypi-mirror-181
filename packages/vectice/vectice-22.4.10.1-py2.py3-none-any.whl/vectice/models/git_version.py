from __future__ import annotations

import logging

from typing import Optional, Any
from vectice.api.json.user_declared_version import UserDeclaredVersion
from vectice.api.json.code_version import GitVersion


_logger = logging.getLogger(__name__)


class CodeSource:
    """
    CodeSource captures the current commit present in the local .git folder.
    """

    def __init__(self, repository: Optional[Any] = None, user_declared_version: Optional[UserDeclaredVersion] = None):
        self._repository = repository
        self._git_version: GitVersion = self._extract_git_version(repository)
        self._user_declared_version = user_declared_version

    @property
    def repository(self) -> Any:
        return self._repository

    @property
    def user_declared_version(self) -> Optional[UserDeclaredVersion]:
        return self._user_declared_version

    @property
    def git_version(self) -> GitVersion:
        return self._git_version

    def _extract_git_version(self, repository: Any):
        try:
            from git import InvalidGitRepositoryError, NoSuchPathError
        except ModuleNotFoundError as e:
            _logger.warning("The GitPython module is not installed. It is required for code capture.")
            raise ModuleNotFoundError(e)
        try:
            repository_name = repository.remotes.origin.url.split(".git")[0].split("/")[-1]
            try:
                branch_name = repository.active_branch.name
            except TypeError as e:
                logging.warning(f"Extract git version failed due to {e}")
                return None
            commit_hash = repository.head.object.hexsha
            is_dirty = repository.is_dirty()
            uri = repository.remotes.origin.url
            url = f"{uri.split('.git')[0]}"
            return GitVersion(repository_name, branch_name, commit_hash, is_dirty, url)
        except InvalidGitRepositoryError:
            raise ValueError("Extracting the git version failed as the repository is invalid.")
        except NoSuchPathError:
            raise ValueError("Extracting the git version as the path is not correct.")
