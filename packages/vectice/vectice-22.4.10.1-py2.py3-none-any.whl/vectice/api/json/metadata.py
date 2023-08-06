from typing import List

from vectice.models.datasource.datawrapper.metadata.db_metadata import MetadataDB
from vectice.models.datasource.datawrapper.metadata.files_metadata import File
from vectice.models.datasource.datawrapper.metadata.metadata import DatasetSourceUsage


class MetadataInput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._files = self._init_files()
        self._dbs = self._init_dbs()

    def _init_files(self) -> List[File]:
        files: List[File] = []
        if "files" in self:
            for file in self["files"]:
                files.append(File(**file))
        return files

    def _init_dbs(self) -> List[MetadataDB]:
        dbs: List[MetadataDB] = []
        if "dbs" in self:
            for db in self["dbs"]:
                dbs.append(MetadataDB(**db))
        return dbs

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def size(self) -> int:
        return int(self["size"])

    @property
    def usage(self) -> DatasetSourceUsage:
        return DatasetSourceUsage(self["usage"])

    @property
    def origin(self) -> str:
        return str(self["origin"])

    @property
    def files_count(self) -> int:
        return int(self["filesCount"])

    @files_count.setter
    def files_count(self, files_count) -> None:
        self._files_count = files_count

    @property
    def files(self) -> List[File]:
        return List[File](self._files)

    @files.setter
    def files(self, files) -> None:
        self._files = files

    @property
    def dbs(self) -> List[MetadataDB]:
        return List[MetadataDB](self._dbs)

    @dbs.setter
    def dbs(self, dbs) -> None:
        self._dbs = dbs


class MetadataOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
