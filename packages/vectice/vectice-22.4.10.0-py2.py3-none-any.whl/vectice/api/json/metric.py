from __future__ import annotations

import inspect
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Union


@dataclass
class MetricInput(dict):
    def __init__(self, key: str, value: Union[float, int], timestamp: Optional[Union[datetime, str]] = None):
        super().__init__()
        self.key: str = key
        """"""
        self.value: Union[float, int] = value
        """"""
        if timestamp is None:
            self.timestamp: str = datetime.now(timezone.utc).isoformat()
        else:
            self.timestamp = timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp


@dataclass
class MetricOutput:
    key: str
    value: float
    timestamp: datetime
    name: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, metrics):
        return cls(**{k: v for k, v in metrics.items() if k in inspect.signature(cls).parameters})

    def as_dict(self):
        return asdict(self)
