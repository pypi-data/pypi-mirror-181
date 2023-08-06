from __future__ import annotations

import logging
import pickle  # nosec
from typing import Optional, TYPE_CHECKING, List, Tuple, Dict, Any
from vectice.api.json import ModelVersionOutput
from vectice.api import Client
from vectice.api.json import (
    IterationInput,
    IterationStatus,
    IterationStepArtifactInput,
)
from vectice.api.json.dataset_register import DatasetRegisterInput
from vectice.models.datasource.datawrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.models.model import Model
from .attachment_container import AttachmentContainer
from vectice.utils.automatic_link_utils import existing_dataset_logger, existing_model_logger, link_assets_to_step
from vectice.utils.common_utils import _check_code_source, _check_for_code

if TYPE_CHECKING:
    from vectice.models import Phase
    from vectice.models import Step

_logger = logging.getLogger(__name__)

MISSING_DATASOURCE_ERROR_MESSAGE = "Cannot create modeling dataset. Missing %s data source."


class Iteration:
    """
    Describes an iteration which belongs to a Phase. The Iteration is a container for steps, it allows you to iteratively complete steps.
    The steps in an iteration originate from the Steps found under a Phase. When an Iteration is created it snapshots the current steps, thus a
    step created after the iteration is created won't belong to the already created Iteration.
    """

    __slots__ = ["_id", "_index", "_phase", "_status", "_client", "_modeling_dataset", "_model", "_current_step"]

    def __init__(
        self,
        id: int,
        index: int,
        phase: Phase,
        status: Optional[IterationStatus] = IterationStatus.NotStarted,
    ):
        """
        :param id: the iteration identifier
        :param index: the index of the iteration
        :param phase: the project to which the iteration belongs
        :param status: the status of the iteration
        """
        self._id = id
        self._index = index
        self._phase = phase
        self._status = status
        self._client: Client = self._phase._client
        self._modeling_dataset: Optional[Tuple[DataWrapper, DataWrapper, DataWrapper]] = None
        self._model: Optional[Model] = None
        self._current_step: Optional[Step] = None

    def __repr__(self):
        steps = len(self.steps)
        return f"Iteration (index={self._index}, status={self._status}, No. of steps={steps})"

    def __eq__(self, other: object):
        if not isinstance(other, Iteration):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        Get the identifier of the iteration.

        :return: int
        """
        return self._id

    @id.setter
    def id(self, iteration_id: int):
        """
        Set the identifier of the iteration.

        :param iteration_id: the identifier
        """
        self._id = iteration_id

    @property
    def index(self) -> int:
        """
        Get the index of the iteration.

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
        return {"id": self.id, "index": self.index}

    @property
    def step_names(self) -> List[str]:
        """
        Retrieve the name of the steps of the iteration.

        :return: List[str]
        """
        return [step.name for step in self.steps]  # type: ignore

    def step(self, step: str) -> Step:
        """
        Returns the Step available for the Iteration, whose name corresponds to the one passed in parameter.

        :param step: The name of the step
        :return: Step
        """
        from vectice.models import Step

        steps_output = self._client.get_step_by_name(step, self.id)
        _logger.info(f"Step: {steps_output.name} successfully retrieved.")
        step_object = Step(
            steps_output.id,
            self._phase,
            steps_output.name,
            steps_output.index,
            steps_output.description,
            steps_output.completed,
            steps_output.artifacts,
        )
        self._current_step = step_object
        return step_object

    @property
    def steps(self) -> List[Step]:
        """
        Returns a list of Steps available for the Iteration.

        :return: List[Step]
        """
        from vectice.models import Step

        steps_output = self._client.list_steps(self._phase.id, self.index, self._phase.name)
        return sorted(
            [
                Step(item.id, self._phase, item.name, item.index, item.description, item.completed)
                for item in steps_output
            ],
            key=lambda x: x.index,
        )

    @property
    def modeling_dataset(
        self,
    ) -> Optional[Tuple[DataWrapper, DataWrapper, DataWrapper]]:
        """
        Get the modeling dataset of the iteration.

        :return: Optional[Tuple[DataWrapper, DataWrapper, DataWrapper]]
        """
        return self._modeling_dataset

    @modeling_dataset.setter
    def modeling_dataset(self, data_sources: Tuple[DataWrapper, DataWrapper, DataWrapper]):
        """
        Set a modeling dataset, with three datasources : training, testing and validation datasources. The order does not matter and the
        combination of the data sources does not either. Thus, you could use whatever combination suites your needs.

        The DataWraper can be accessed via vectice.FileDataWrapper, vectice.GcsDataWrapper and vectice.S3DataWrapper.
        Or for example `from vectice import FileDataWrapper`.

        :param data_sources: a tuple of three datasources; their metadata must be of three types : training, testing and validation
        """
        logging.getLogger("vectice.models.iteration").propagate = True
        code_version_id = _check_for_code(data_sources, self._client, self._phase._project.id, _logger)
        train_datasource, test_datasource, validation_datasource = self._get_datasources_in_order(data_sources)
        self._modeling_dataset = train_datasource, test_datasource, validation_datasource

        name = self._client.get_dataset_name(train_datasource)
        inputs = self._client.get_dataset_inputs(train_datasource)
        dataset_sources = self._get_metadata_from_sources((train_datasource, test_datasource, validation_datasource))
        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=SourceUsage.MODELING.value,
            datasetSources=dataset_sources,
            inputs=inputs,
            codeVersionId=code_version_id,
        )
        data = self._client.register_dataset(
            dataset_register_input,
            iteration_id=self._id,
            project_id=self._phase._project._id,
            phase_id=self._phase.id,
        )
        existing_dataset_logger(data, name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, name, data, _logger)

    @staticmethod
    def _get_datasources_in_order(
        data_sources: Tuple[DataWrapper, DataWrapper, DataWrapper]
    ) -> Tuple[DataWrapper, DataWrapper, DataWrapper]:
        from vectice import DatasetSourceUsage

        if len(data_sources) != 3:
            raise ValueError("Exactly three datasources are needed to create a modeling dataset.")
        train_datasource, test_datasource, validation_datasource = None, None, None
        for data_source in data_sources:
            if data_source.metadata.usage == DatasetSourceUsage.TRAINING:
                train_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.TESTING:
                test_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.VALIDATION:
                validation_datasource = data_source
        if not train_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "training")
        if not test_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "testing")
        if not validation_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "validation")
        return train_datasource, test_datasource, validation_datasource

    @staticmethod
    def _get_metadata_from_sources(data_sources: Tuple[DataWrapper, DataWrapper, DataWrapper]) -> List[Dict]:
        return [data_source.metadata.asdict() for data_source in data_sources if data_source]

    @property
    def model(self) -> Optional[Model]:
        """
        Return the model.

        :return: Optional[Model]
        """
        return self._model

    @model.setter
    def model(self, model: Model):
        """
        Set the model for the iteration. The model can be created using the Model Wrapper, accessed via vectice.Model or
        `from vectice import Model`.

        :param model: the model
        """
        logging.getLogger("vectice.models.iteration").propagate = True
        if model.capture_code:
            code_version_id = _check_code_source(self._client, self._phase._project._id, _logger)
        else:
            code_version_id = None
        self._model = model
        data = model_output = self._client.register_model(
            model, self._phase._project._id, self._phase.id, self._id, code_version_id, model.inputs
        )
        model_version = model_output.model_version
        attachments = self._set_model_attachments(model, model_version)
        _logger.info(
            f"Successfully registered Model(name='{model.name}', library='{model.library}', "
            f"technique='{model.technique}', version='{model_version.name}')."
        )
        existing_model_logger(data, model.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["modelVersion"]["id"], type="ModelVersion")
        attachments = (
            [
                IterationStepArtifactInput(id=attach["fileId"], entityFileId=attach["entityId"], type="EntityFile")
                for attach in attachments
            ]
            if attachments
            else None
        )
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, model.name, data, _logger, attachments)

    def cancel(self) -> Iteration:
        """
        Cancel the iteration by abandoning all steps still open.

        :return: Iteration
        """
        iteration_input = IterationInput(status=IterationStatus.Abandoned.name)
        iteration_output = self._client.update_iteration(self.id, iteration_input)
        return Iteration(
            iteration_output.id,
            iteration_output.index,
            self._phase,
            iteration_output.status,
        )

    def _set_model_attachments(self, model: Model, model_version: ModelVersionOutput):
        logging.getLogger("vectice.models.attachment_container").propagate = True
        attachments = None
        if model.attachments:
            container = AttachmentContainer(model_version.name, model_version.id, self._client, "ModelVersion")
            attachments = container.add_attachments(model.attachments)
        if model.predictor:
            model_content = self._serialize_model(model.predictor)
            model_type_name = type(model.predictor).__name__
            container = AttachmentContainer(model_version.name, model_version.id, self._client, "ModelVersion")
            container.add_serialized_model(model_type_name, model_content)
        return attachments

    @staticmethod
    def _serialize_model(model: Any) -> bytes:
        return pickle.dumps(model)
