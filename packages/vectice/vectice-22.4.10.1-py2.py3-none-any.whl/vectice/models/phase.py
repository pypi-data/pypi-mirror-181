from __future__ import annotations

import logging
from typing import List, Optional, TYPE_CHECKING, Dict

from vectice.api.json.phase import PhaseStatus
from vectice.models.iteration import Iteration, IterationStepArtifactInput
from vectice.api import Client
from vectice.models.datasource.datawrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.utils.automatic_link_utils import existing_dataset_logger, link_dataset_to_step
from vectice.utils.common_utils import _check_code_source

if TYPE_CHECKING:
    from vectice.models import Project


_logger = logging.getLogger(__name__)


class Phase:
    """
    Describes a phase. A phase represents a milestone of a data science project.
    """

    __slots__ = ["_id", "_project", "_name", "_index", "_status", "_clean_dataset", "_client", "_current_iteration"]

    def __init__(
        self,
        id: int,
        project: Project,
        name: str,
        index: int,
        status: PhaseStatus = PhaseStatus.NotStarted,
    ):
        """
        :param id: the phase identifier
        :param project: the project to which the phase belongs
        :param name: the name of the phase
        :param index: the index of the phase
        :param status: the status of the phase
        """
        self._id = id
        self._project = project
        self._name = name
        self._index = index
        self._status = status
        self._client: Client = self._project._client
        self._clean_dataset: Optional[DataWrapper] = None
        self._current_iteration: Optional[Iteration] = None

    def __repr__(self):
        return f"Phase (name='{self.name}', id={self.id}, status='{self.status.name}')"

    def __eq__(self, other: object):
        if not isinstance(other, Phase):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        Get the identifier for the phase.

        :return: int
        """
        return self._id

    @id.setter
    def id(self, phase_id: int):
        """
        Set the identifier for the phase.

        :param phase_id: the phase identifier to set
        """
        self._id = phase_id

    @property
    def name(self) -> str:
        """
        Get the name of the phase.

        :return: str
        """
        return self._name

    @property
    def index(self) -> int:
        """
        Get the index of the phase.

        :return: int
        """
        return self._index

    @property
    def status(self) -> PhaseStatus:
        """
        Get the status of the phase.

        :return: PhaseStatus
        """
        return self._status

    @property
    def properties(self) -> Dict:
        """
        Retrieve the relevant identifiers for the
        current project.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def iterations(self) -> List[Iteration]:
        """
        Get the list of iterations of the phase.

        :return: List[Iteration]
        """
        iteration_outputs = self._client.list_iterations(self.id)
        return sorted(
            [Iteration(item.id, item.index, self, item.status) for item in iteration_outputs], key=lambda x: x.index
        )

    def iteration(self, index: Optional[int] = None) -> Iteration:
        """
        Return the iteration with the specified index.
        If no index is specified, return the active iteration of the phase.

        :return: Iteration
        """
        if index:
            iteration_output = self._client.get_iteration_by_index(self.id, index)
            _logger.info(f"Iteration with index: {iteration_output.index} successfully retrieved.")
        else:
            iteration_output = self._client.get_or_create_iteration(self.id)
            _logger.info(f"Iteration with id: {iteration_output.id} successfully retrieved.")
        iteration_object = Iteration(iteration_output.id, iteration_output.index, self, iteration_output.status)
        self._current_iteration = iteration_object
        return iteration_object

    @property
    def clean_dataset(self) -> Optional[DataWrapper]:
        """
        If it exists, gets the wrapped clean dataset of the phase.

        :return: Optional[DataWrapper]
        """
        return self._clean_dataset

    @clean_dataset.setter
    def clean_dataset(self, data_source: DataWrapper) -> None:
        """
        Set a clean dataset using a DataWrapper, to access a DataWrapper that could suite your use case, you can access the
        available DataWrappers by doing the following;

        The DataWraper can be accessed via vectice.FileDataWrapper, vectice.GcsDataWrapper and vectice.S3DataWrapper.
        Or for example `from vectice import FileDataWrapper`.

        :param data_source: the clean dataset
        """
        if data_source.capture_code:
            code_version_id = _check_code_source(self._client, self._project._id, _logger)
        else:
            code_version_id = None
        self._clean_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source,
            SourceUsage.CLEAN,
            project_id=self._project._id,
            phase_id=self._id,
            code_version_id=code_version_id,
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        logging.getLogger("vectice.models.project").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, phase=self)
