from __future__ import annotations

from typing import List, Optional, Dict

from .metadata import Metadata, SourceOrigin, SourceType, DatasetSourceUsage


class DBMetadata(Metadata):
    """
    Class that describes metadata of dataset that comes from a database.
    """

    def __init__(
        self,
        dbs: List[MetadataDB],
        size: int,
        usage: DatasetSourceUsage,
        origin: SourceOrigin,
    ):
        """
        :param dbs: the list of databases
        :param size: the size of the metadata
        :param usage: the usage of the metadata
        :param origin: the origin of the metadata
        """
        super().__init__(size=size, type=SourceType.DB.name, usage=usage, origin=origin.name)
        self.dbs = dbs

    def asdict(self) -> Dict:
        return {
            "type": "DB",
            "dbs": [db.asdict() for db in self.dbs],
            "size": self.size,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin,
            "filesCount": None,
            "files": [],
        }


class Column:
    """
    Model a column of a dataset, like a database column.
    """

    def __init__(
        self,
        name: str,
        data_type: str,
        is_unique: Optional[bool] = None,
        nullable: Optional[bool] = None,
        is_private_key: Optional[bool] = None,
        is_foreign_key: Optional[bool] = None,
    ):
        """
        :param name: the name of the column
        :param data_type: the type of the data contained in the column
        :param is_unique: if the column uniquely defines a record,
        individually or with other columns (can be null)
        :param nullable: if the column can contain null value
        :param is_private_key: if the column uniquely defines a record,
        individually or with other columns (cannot be null)
        :param is_foreign_key: if the column refers to another one
        """
        self.name = name
        self.data_type = data_type
        self.is_unique = is_unique
        self.nullable = nullable
        self.is_private_key = is_private_key
        self.is_foreign_key = is_foreign_key

    def asdict(self) -> Dict:
        return {
            "name": self.name,
            "dataType": self.data_type,
            "isUnique": self.is_unique,
            "nullable": self.nullable,
            "isPK": self.is_private_key,
            "isFK": self.is_foreign_key,
        }


class MetadataDB:
    def __init__(self, name: str, columns: List[Column], rows_number: int, size: Optional[int] = None):
        """
        :param name: the name of the table
        :param columns: the columns that compose the table
        :param rows_number: the number of row of the table
        :param size: the size of the table
        """
        self.name = name
        self.size = size
        self.rows_number = rows_number
        self.columns = columns

    def asdict(self) -> Dict:
        return {
            "name": self.name,
            "size": self.size,
            "rowsNumber": self.rows_number,
            "columns": [column.asdict() for column in self.columns],
        }
