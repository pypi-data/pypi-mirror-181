from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING, Optional, Dict

from vectice.api.json.iteration import IterationStepArtifact
from vectice.api.http_error_handlers import VecticeException


if TYPE_CHECKING:
    from vectice.models import Phase


_logger = logging.getLogger(__name__)


class Step:
    """
    Describes a step, which is a specific sequence of a phase.
    """

    def __init__(
        self,
        id: int,
        phase: Phase,
        name: str,
        index: int,
        description: Optional[str] = None,
        completed: bool = False,
        artifacts: Optional[List[IterationStepArtifact]] = None,
    ):
        """
        :param id: the phase identifier
        :param phase: the project to which the phase belongs
        :param name: the name of the phase
        :param description: the description of the phase
        """
        self._id = id
        self._phase = phase
        self._name = name
        self._index = index
        self._description = description
        self._client = self._phase._client
        self._completed = completed
        self._artifacts = artifacts

    def __repr__(self):
        return f"Step(name='{self.name}', id={self.id}, description='{self._description}', completed={self.completed})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    @property
    def name(self) -> str:
        """
        Get the name of the step.

        :return: str
        """
        return self._name

    @property
    def id(self) -> int:
        """
        Get the id of the step.

        :return: int
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        """
        Set the id of the step.

        :param step_id: the id to set
        """
        self._id = step_id

    @property
    def index(self) -> int:
        """
        Get the index of the step.

        :return: int
        """
        return self._index

    @property
    def properties(self) -> Dict:
        """
        Retrieve the relevant identifiers for the
        current project.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def artifacts(self) -> Optional[List[IterationStepArtifact]]:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: List[IterationStepArtifact]):
        self._artifacts = artifacts

    def next_step(self, message: Optional[str] = None) -> Optional[Step]:
        """
        Close the step and returns the next one if it exists.

        :return: Optional[Step]
        """
        self.close(message)
        steps_output = self._client.list_steps(self._phase.id)
        open_steps = sorted(
            [
                Step(item.id, self._phase, item.name, item.index, item.description)
                for item in steps_output
                if not item.completed
            ],
            key=lambda x: x.index,
        )
        if not open_steps:
            _logger.info("There are no active steps.")
            return None
        next_step = open_steps[0]
        _logger.info(f"Next step : {repr(next_step)}")
        return next_step

    def close(self, message: Optional[str] = None):
        try:
            self._client.close_step(self.id, message)
            _logger.info(f"'{self.name}' was successfully closed.")
            self._completed = True
        except VecticeException as e:
            raise e
