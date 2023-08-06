import logging
from abc import abstractmethod, ABCMeta
from typing import Dict, Optional, List

from .metadata import FilesMetadata, DatasetSourceUsage

_logger = logging.getLogger(__name__)


class DataWrapper(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        name: str,
        usage: Optional[DatasetSourceUsage] = None,
        inputs: Optional[List[int]] = None,
        capture_code: bool = True,
    ):
        """
        :param usage: The usage of the dataset
        :param name: The name of the :py:class:`DataWrapper`
        :param inputs: The list of dataset ids to create a new dataset from
        :param capture_code: Automatically capture active commit in .git folder
        """
        self._old_name = name
        self._name = name
        self._inputs = inputs
        self._usage = usage
        self._metadata = None
        self._data = None
        self._capture_code = capture_code

    @property
    def data(self) -> Dict[str, bytes]:
        """
        Get the data from the wrapper.
        :return: Dict[str, bytes]
        """
        if self._data is None:
            self._data = self._fetch_data()  # type: ignore
        return self._data  # type: ignore

    @abstractmethod
    def _fetch_data(self) -> Dict[str, bytes]:
        pass

    @abstractmethod
    def _build_metadata(self) -> FilesMetadata:
        pass

    @property
    def name(self) -> str:
        """
        Get the name of the wrapper.
        :return: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the wrapper.
        """
        self._name = value
        self._clear_data_and_metadata()

    @property
    def usage(self) -> Optional[DatasetSourceUsage]:
        """
        Get the usage of the wrapper.
        :return: Optional[DatasetSourceUsage]
        """
        return self._usage

    @property
    def inputs(self) -> Optional[List[int]]:
        """
        Get the inputs of the wrapper.
        :return: Optional[List[int]]
        """
        return self._inputs

    @property
    def metadata(self) -> FilesMetadata:
        """
        Get the metadata of the wrapper.
        :return: FilesMetadata
        """
        if self._metadata is None:
            self.metadata = self._build_metadata()
        return self._metadata  # type: ignore

    @metadata.setter
    def metadata(self, value):
        """
        Set the metadata of the wrapper.
        """
        self._metadata = value

    @property
    def capture_code(self) -> bool:
        """
        Capture code of the dataset.

        :return: CodeSource
        """
        return self._capture_code

    def _clear_data_and_metadata(self):
        self._data = None
        self._metadata = None
