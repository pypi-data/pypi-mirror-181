from __future__ import annotations

import logging
from typing import List, Optional, TYPE_CHECKING, Union, Dict

from .project import Project

if TYPE_CHECKING:
    from vectice.api import Client


_logger = logging.getLogger(__name__)


class Workspace:
    """
    Workspace is a space where you can find :py:class:`Project` for a team.

    In a workspace, you can get and list projects.

    """

    def __init__(self, id: int, name: str, description: Optional[str] = None):
        """
        :param id: the workspace identifier
        :param name: the name of the workspace
        :param description: the description of the workspace
        """
        self._id = id
        self._name = name
        self._description = description
        self._client: Client

    def __post_init__(self, client: Client):
        self._client = client

    def __eq__(self, other: object):
        if not isinstance(other, Workspace):
            return NotImplemented
        return self.id == other.id

    def __repr__(self):
        return f"Workspace(name={self.name}, id={self._id}, description={self.description})"

    @property
    def id(self) -> int:
        """
        The workspace identifier.

        :return: int
        """
        return self._id

    @property
    def name(self) -> str:
        """
        The name of the workspace.

        :return: str
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        The description of the workspace.

        :return: Optional[str]
        """
        return self._description

    @property
    def properties(self) -> Dict:
        """
        Retrieve the relevant identifiers for the current workspace.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id}

    def project(self, project: Union[str, int]) -> Project:
        """
        Gets a project.

        Gets a project instance with the specified project name or id in the current workspace.

        :param project: The project name or id to get.

        :return: Project
        """
        item = self._client.get_project(project, self.id)
        _logger.info(f"Your current project: {item.id}")
        return Project(item.id, self, item.name, item.description)

    @property
    def projects(self) -> List[Project]:
        """
        Get the list of the projects that belong to the workspace.

        :return: List[Project]
        """
        response = self._client.list_projects(self.id)
        return [Project(item.id, self, item.name, item.description) for item in response.list]
