"""
helpful abstractions
"""

from abc import ABC, abstractproperty
from dataclasses import dataclass

from joblib import Memory
from pandera.typing import DataFrame

from .schema import Summary


@dataclass(frozen=True)  # type: ignore
class TimeUnit(ABC):
    memory: Memory = Memory()

    @abstractproperty
    def last_modified(self) -> str:
        pass

    @abstractproperty
    def summary(self) -> DataFrame[Summary]:
        pass


class HasURL(ABC):
    @abstractproperty
    def url(self) -> str:
        pass

class HasZip(ABC):
    @abstractproperty
    def zip(self) -> bytes:
        pass
