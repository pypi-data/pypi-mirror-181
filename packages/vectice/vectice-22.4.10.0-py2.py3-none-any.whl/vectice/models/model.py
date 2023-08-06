import logging
import pickle  # nosec
from typing import Optional, Dict, Union, List, Any

from vectice.models import Metric, Property

_logger = logging.getLogger(__name__)


class Model:
    """
    This class is used to create a model, which then can be added to an iteration.

    The Model Wrapper requires a library for example 'scikit-learn' and technique for example 'linear regression'.
    Furthermore, you can add metrics by passing a dictionary for example {"MSE": 1}. Properties by passing a dictionary
    for example {"folds": 32}. Name, which is an optional string. Attachments which are whatever file paths you would like to
    attach to the model, for example a graph. Predictor, the trained predictor/classifier, this is pickled and attached
    to the model.

    The Capture Code flag is whether or not code is tracked and linked to the Model being created. A .git must be present in
    either the working directory or parent directories.

    Inputs are the IDs for any assets you would like to link to your Model, for example you could link a Dataset Version that
    was created for your Training Dataset.
    """

    def __init__(
        self,
        library: str,
        technique: str,
        metrics: Optional[Union[Dict[str, int], List[Metric], Metric]] = None,
        properties: Optional[Union[Dict[str, str], Dict[str, int], List[Property], Property]] = None,
        name: Optional[str] = None,
        attachments: Optional[Union[str, List[str]]] = None,
        predictor: Any = None,
        capture_code: bool = True,
        inputs: Optional[List[int]] = None,
    ):
        """
        The Model Wrapper requires a library for example 'scikit-learn' and technique for example 'linear regression'.
        Furthermore, you can add metrics by passing a dictionary for example {"MSE": 1}. Properties by passing a dictionary
        for example {"folds": 32}. Name, which is an optional string. Attachments which are whatever file paths you would like to
        attach to the model, for example a graph. Predictor, the trained predictor/classifier, this is pickled and attached
        to the model.

        The Capture Code flag is whether or not code is tracked and linked to the Model being created. A .git must be present in
        either the working directory or parent directories.

        Inputs are the IDs for any assets you would like to link to your Model, for example you could link a Dataset Version that
        was created for your Training Dataset.

        :param library: The library used to generate the model
        :param technique: The modeling technique used
        :param metrics: The metrics describing the model
        :param properties: The properties describing the model
        :param name: The name of the model. If no name is passed, one will be generated based on the library and technique.
        :param attachments: The file/s paths that will be attached to the model version.
        :param capture_code: Automatically capture active commit in .git folder
        :param inputs: The list of dataset version ids to link as lineage
        """
        self._library = library
        self._technique = technique
        self._name = name if name else self._generate_name()
        self._metrics = self._format_metrics(metrics) if metrics else None
        self._properties = self._format_properties(properties) if properties else None
        self._attachments = self._format_attachments(attachments) if attachments else None
        self._capture_code = capture_code
        self._predictor = pickle.dumps(predictor)  # nosec
        self._inputs = inputs

    def __repr__(self):
        return (
            f"Model(name='{self.name}', library='{self.library}', technique='{self.technique}', "
            f"metrics={self.metrics}, properties={self.properties}, attachments={self.attachments})"
        )

    @property
    def name(self) -> str:
        """
        Name of the model.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the model.

        :param name: the name for the model
        """
        self._name = name

    @property
    def predictor(self) -> Any:
        """
        Return the predictor.

        :return: Any
        """
        return pickle.loads(self._predictor)  # nosec

    @predictor.setter
    def predictor(self, predictor: Any):
        """
        Set the predictor.

        :param predictor: the predictor
        """
        self._predictor = pickle.dumps(predictor)  # nosec

    @classmethod
    def read_predictor_file(cls, path: str) -> Any:
        return pickle.load(open(path, "rb"))  # nosec

    @property
    def library(self) -> str:
        """
        Library used to generate the model.

        :return: str
        """
        return self._library

    @library.setter
    def library(self, library):
        """
        Set the library used to create the model.

        :param library: the library used to create the model.
        """
        self._library = library

    @property
    def technique(self) -> str:
        """
        The modeling technique used.

        :return: str
        """
        return self._technique

    @technique.setter
    def technique(self, technique):
        """
        Set the modeling technique used.

        :param technique: the modeling technique used
        """
        self._technique = technique

    @property
    def metrics(self) -> Optional[List[Metric]]:
        """
        The metrics of the model.

        :return: Optional[List[Metric]]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics: Optional[Union[Dict[str, int], List[Metric], Metric]]):
        """
        Set the metrics defining the model.

        :param metrics: the metrics of the model
        """
        self._format_metrics(metrics)

    @property
    def properties(self) -> Optional[List[Property]]:
        """
        The properties of the model.

        :return: Optional[List[Property]]
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Optional[Union[Dict[str, str], List[Property], Property]]):
        """
        Set the properties defining the model.

        :param properties: the properties of the model
        """
        self._format_properties(properties)

    @property
    def attachments(self) -> Optional[List[str]]:
        """
        The attachments of the model.

        :return: Optional[List[str]]
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: Union[List[str], str]):
        """
        Set the file or set of files to attach to the model.

        :param attachments: the filename or filenames of the file or set of files to attach to the model
        """
        self._attachments = self._format_attachments(attachments)

    @property
    def capture_code(self) -> bool:
        """
        Capture code of the model.

        :return: CodeSource
        """
        return self._capture_code

    @property
    def inputs(self) -> Any:
        """
        Return the inputs.

        :return: Any
        """
        return self._inputs

    def _generate_name(self) -> str:
        return f"{self.library} {self.technique} model"

    def _format_metrics(self, metrics: Optional[Union[Dict[str, int], List[Metric], Metric]]) -> List[Metric]:
        if metrics is None:
            return []
        if isinstance(metrics, Metric):
            return [metrics]
        if isinstance(metrics, List):
            metrics = self._remove_incorrect_metrics(metrics)
            key_list = [metric.key for metric in metrics]
            self._check_key_duplicates(key_list)
            return metrics
        if isinstance(metrics, Dict):
            return [Metric(key, value) for (key, value) in metrics.items()]
        else:
            raise ValueError("Please check metric type.")

    @staticmethod
    def _check_key_duplicates(key_list: List[str]):
        if len(key_list) != len(set(key_list)):
            raise ValueError("Duplicate keys are not allowed.")

    @staticmethod
    def _remove_incorrect_metrics(metrics: List[Metric]) -> List[Metric]:
        for metric in metrics:
            if not isinstance(metric, Metric):
                logging.warning(f"Incorrect metric '{metric}'. Please check metric type.")
                metrics.remove(metric)
        return metrics

    @staticmethod
    def _format_attachments(attachments: Union[str, List[str]]) -> List[str]:
        return [attachment for attachment in set(attachments)] if isinstance(attachments, list) else [attachments]

    def _format_properties(
        self, properties: Optional[Union[Dict[str, str], Dict[str, int], List[Property], Property]]
    ) -> List[Property]:
        if properties is None:
            return []
        if isinstance(properties, Property):
            return [properties]
        if isinstance(properties, List):
            properties = self._remove_incorrect_properties(properties)
            key_list = [prop.key for prop in properties]
            self._check_key_duplicates(key_list)
            return properties
        if isinstance(properties, Dict):
            return [Property(key, str(value)) for (key, value) in properties.items()]
        else:
            raise ValueError("Please check property type.")

    @staticmethod
    def _remove_incorrect_properties(properties: List[Property]) -> List[Property]:
        for prop in properties:
            if not isinstance(prop, Property):
                logging.warning(f"Incorrect property '{prop}'. Please check property type.")
                properties.remove(prop)
        return properties
