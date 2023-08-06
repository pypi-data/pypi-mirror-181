from __future__ import annotations

from typing import Optional, List, Dict

from .metadata import Metadata, SourceOrigin, SourceType, DatasetSourceUsage


class FilesMetadata(Metadata):
    """
    The metadata of a set of files.
    """

    def __init__(
        self,
        files_count: int,
        files: List[File],
        size: int,
        origin: SourceOrigin,
        usage: Optional[DatasetSourceUsage] = None,
    ):
        """
        :param files_count: the number of files contained in the list
        :param files: the list of files of the dataset
        :param size: the size of the set of files
        :param usage: the usage of the dataset
        :param origin: where the dataset files come from
        """
        super().__init__(size, SourceType.FILES.name, origin.name, usage if usage else None)
        self.files = files
        self.files_count = files_count

    def asdict(self) -> Dict:
        return {
            "filesCount": self.files_count,
            "files": [file.asdict() for file in self.files],
            "size": self.size,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin if self.origin else None,
            "type": self.type,
        }


class File:
    """
    Describe a dataset file.
    """

    def __init__(
        self,
        name: str,
        size: int,
        fingerprint: str,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        uri: Optional[str] = None,
    ):
        """
        :param name: the name of the file
        :param size: the size of the file
        :param fingerprint: the hash of the file
        :param created_date: the date of creation of the file
        :param updated_date: the date of last update of the file
        :param uri: the uri of the file
        """
        self.name = name
        self.size = size
        self.fingerprint = fingerprint
        self.created_date = created_date
        self.updated_date = updated_date
        self.uri = uri

    def asdict(self) -> Dict:
        return {
            "name": self.name,
            "size": self.size,
            "fingerprint": self.fingerprint,
            "createdDate": self.created_date,
            "updatedDate": self.updated_date,
            "uri": self.uri,
        }
