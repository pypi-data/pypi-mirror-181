from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Union, Optional


@dataclass
class Property:
    """
    Defines a property for a model or a dataset.

    :param key: the key to identify the property
    :param value: the value of the property
    :param timestamp: the timestamp of the property. Corresponds to the property creation time if not explicitly passed.
    :param name: the name of the property
    """

    key: str
    value: str
    timestamp: Union[datetime, str] = datetime.now(timezone.utc).isoformat()
    name: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.value, str):
            self.value = str(self.value)

    def __repr__(self) -> str:
        return f"Property(key='{self.key}', value='{self.value}')"
