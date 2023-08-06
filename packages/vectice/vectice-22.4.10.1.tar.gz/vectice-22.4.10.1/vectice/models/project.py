from __future__ import annotations

import logging
from typing import Optional, List, TYPE_CHECKING, Dict, Union

from .datasource.datawrapper import DataWrapper
from .datasource.datawrapper.metadata import SourceUsage
from .phase import Phase
from vectice.api.json import IterationStepArtifactInput
from vectice.utils.automatic_link_utils import existing_dataset_logger, link_dataset_to_step
from vectice.utils.common_utils import _check_code_source

if TYPE_CHECKING:
    from vectice.models import Workspace


_logger = logging.getLogger(__name__)


class Project:
    """
    A project contains resources relative to a specific project.

    A project can contain:

    + Phases describing the project (goals, status, ...)
    + origin datasets

    A project can contain several datasets. Each dataset contains its own history.

    """

    __slots__ = [
        "_id",
        "_workspace",
        "_name",
        "_description",
        "_phase",
        "_origin_dataset",
        "_client",
    ]

    def __init__(
        self,
        id: int,
        workspace: Workspace,
        name: str,
        description: Optional[str] = None,
    ):
        """
        :param id: Project identifier
        :param workspace: The workspace reference this project belongs to
        :param name: Name of the project
        :param description: Brief description of the project
        """
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._phase: Optional[Phase] = None
        self._origin_dataset: Optional[DataWrapper] = None
        self._client = workspace._client

    def __repr__(self):
        return (
            f"Project(name='{self.name}', id={self._id}, description='{self.description}', workspace={self._workspace})"
        )

    def __eq__(self, other: object):
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        The project identifier.

        :return: int
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """
        The workspace object this project belongs to.

        :return: Workspace
        """
        return self._workspace

    @property
    def name(self) -> str:
        """
        Name of the project.

        :return: str
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        Brief description of the project.

        :return: Optional[str]
        """
        return self._description

    @property
    def properties(self) -> Dict:
        """
        Retrieve the relevant identifiers for the
        current project.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "workspace": self.workspace.id}

    def phase(self, phase: Union[str, int]) -> Optional[Phase]:
        """
        Get the Phase associated with the Phase name or id
        provided.

        :return: Optional[Phase]
        """
        item = self._client.get_phase(phase, project_id=self._id)  # type: ignore
        _logger.info(f"Phase with id: {item.id} successfully retrieved.")
        phase_object = Phase(item.id, self, item.name, item.index, item.status)
        self._phase = phase_object
        return phase_object

    @property
    def phases(self) -> List[Phase]:
        """
        Get the Phases associated with the Project.

        :return: List[Phase]
        """
        outputs = self._client.list_phases(project=self._id)
        return sorted(
            [Phase(item.id, self, item.name, item.index, item.status) for item in outputs], key=lambda x: x.index
        )

    @property
    def origin_dataset(self) -> Optional[DataWrapper]:
        """
        Get the wrapped origin dataset of the Project.

        :return: Optional[DataWrapper]
        """
        return self._origin_dataset

    @origin_dataset.setter
    def origin_dataset(self, data_source: DataWrapper):
        """
        Set the wrapped origin dataset of the Project. To access a DataWrapper that could suite your use case,
        you can access the available DataWrappers by doing the following;

        The DataWraper can be accessed via vectice.FileDataWrapper, vectice.GcsDataWrapper and vectice.S3DataWrapper.
        Or for example `from vectice import FileDataWrapper`.

        :param data_source: the origin dataset
        """
        if data_source.capture_code:
            code_version_id = _check_code_source(self._client, self._id, _logger)
        else:
            code_version_id = None
        self._origin_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source, SourceUsage.ORIGIN, project_id=self._id, code_version_id=code_version_id
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, project=self)
