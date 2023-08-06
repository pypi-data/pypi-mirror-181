from __future__ import annotations

import logging

from typing import Optional, Union, List

from vectice.utils.configuration import Configuration
from vectice.api import Client
from vectice.models.workspace import Workspace
from vectice.models.project import Project
from vectice.utils.last_assets import _get_last_used_assets_and_logging


_logger = logging.getLogger(__name__)
CAN_NOT_BE_EMPTY_ERROR_MESSAGE = "%s can not be empty."


class Connection:
    """
    This class allows you to connect to the Vectice application.
    Once the connection is established, information is logged automatically.
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        workspace: Optional[Union[str, int]] = None,
    ):
        """
        :param api_token: Your private api token.
        :param host: The address of the Vectice application.
        :param workspace: The workspace you want to work in.
        """
        logging.getLogger("Client").propagate = True
        self._client = Client(
            workspace=workspace,
            token=api_token,
            api_endpoint=host,
            auto_connect=True,
            allow_self_certificate=True,
        )
        _logger.info("Vectice successfully connected.")
        compatibility = self._client.check_compatibility()
        if compatibility.status != "OK":
            if compatibility.status == "Error":
                _logger.error(f"compatibility error: {compatibility.message}")
                raise RuntimeError(f"compatibility error: {compatibility.message}")
            else:
                _logger.warning(f"compatibility warning: {compatibility.message}")

    def __repr__(self) -> str:
        return (
            "Connection("
            + f"workspace={self._client.workspace.name if self._client.workspace else 'None'}, "
            + f"host={self._client.auth.api_base_url}, "
        )

    def workspace(self, workspace: Union[str, int]) -> Workspace:
        """
        Return the workspace object that id or name matches the reference specified.

        :param workspace: The id or the name of the desired workspace.
        :return: Workspace
        """
        output = self._client.get_workspace(workspace)
        result = Workspace(output.id, output.name, output.description)
        result.__post_init__(self._client)
        return result

    @property
    def workspaces(self) -> Optional[List[Workspace]]:
        """
        List workspaces.

        Lists the workspaces the user have access to with its user connection.

        :return: List of Workspaces
        """
        outputs = self._client.list_workspaces()
        results = [Workspace(id=output.id, name=output.name, description=output.description) for output in outputs.list]
        for workspace in results:
            workspace.__post_init__(self._client)
        return results

    @staticmethod
    def connect(
        api_token: Optional[str] = None,
        host: Optional[str] = None,
        config: Optional[str] = None,
        workspace: Optional[Union[str, int]] = None,
        project: Optional[str] = None,
    ) -> Optional[Union[Connection, Workspace, Project]]:
        """
        Attempts to create a client that connects and authenticates to Vectice using the api_token, host, workspace, project or json config provided. If
        a config is used the following keys must be set in the json file; The json config file is generated when you make an api token under your user
        profile.

        1. VECTICE_API_TOKEN - required
        2. VECTICE_API_ENDPOINT - required
        3. WORKSPACE - this key is optional
        4. PROJECT - this key is optional

        :param api_token: The api token found in the account/keys.
        :param host: The host which the client will try to connect to.
        :param config: A config file which is json and requires the keys VECTICE_API_TOKEN, VECTICE_API_ENDPOINT and an optional WORKSPACE and PROJECT.
        :param workspace: The workspace name or ID you want to use.
        :param project: The project name you want to use.
        :return: Vectice Object
        """
        if config:
            configuration = Configuration(config)
            workspace = configuration.workspace
            project = configuration.project
            api_token = configuration.api_token
            host = configuration.host
        if host == "":
            raise ValueError(CAN_NOT_BE_EMPTY_ERROR_MESSAGE % "The host")
        if api_token == "":  # nosec B105
            raise ValueError(CAN_NOT_BE_EMPTY_ERROR_MESSAGE % "The API token")  # nosec B105
        connection = Connection(api_token=api_token, host=host)
        if workspace == "":
            raise ValueError(CAN_NOT_BE_EMPTY_ERROR_MESSAGE % "The workspace name")
        if project == "":
            raise ValueError(CAN_NOT_BE_EMPTY_ERROR_MESSAGE % "The project name")
        if workspace and not project:
            workspace_output = connection.workspace(workspace)
            _logger.info(f"Your current workspace: {workspace_output.name}")
            _get_last_used_assets_and_logging(connection._client, _logger, workspace_output.name)
            return workspace_output
        elif workspace and project:
            logging.getLogger("vectice.models.workspace").propagate = False
            workspace_output = connection.workspace(workspace)
            project_output = workspace_output.project(project)
            _logger.info(f"Your current workspace: {workspace_output.name} and project: {project_output.name}")
            _get_last_used_assets_and_logging(connection._client, _logger, workspace_output.name)
            return project_output
        elif project and not workspace:
            raise ValueError("A workspace reference is needed to retrieve a project.")
        else:
            return connection
