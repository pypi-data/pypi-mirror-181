"""
base classes in the nysmix data
"""

from datetime import date, datetime, timedelta
from functools import cached_property

from requests import get
from nysmix.config import DATE_START

from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from .config import TZ, FORMAT_DATE
from logging import info
from .utils import get_last_modified


@dataclass(frozen=True)  # type: ignore
class TimeUnitBase(ABC):
    year: int
    month: int
    day: int = 1

    @abstractproperty
    def last_modified(self) -> str:
        pass

    @property
    def dt(self) -> date:
        return date(year=self.year, month=self.month, day=self.day)

    @property
    def str_date(self) -> str:
        return self.dt.strftime(FORMAT_DATE)

    @property
    def is_before_start(self) -> bool:
        return self.dt < self.from_date(DATE_START).dt

    @property
    def is_future(self) -> bool:
        return self.dt > datetime.now(TZ).date()

    @staticmethod
    @abstractmethod
    def from_date(dt: date):  # -> TimeUnit:
        pass


class MonthBase(TimeUnitBase):
    @property
    def name_file_zip(self) -> str:
        return f"{self.str_date}rtfuelmix_csv.zip"

    @property
    def url(self) -> str:
        return f"http://mis.nyiso.com/public/csv/rtfuelmix/{self.name_file_zip}"

    @cached_property
    def last_modified(self) -> str:
        return get_last_modified(obj=self)

    @staticmethod
    def from_date(dt: date):  # -> TimeUnit:
        return MonthBase(year=dt.year, month=dt.month)

    @property
    def zip(self) -> bytes:
        info(f"attempt to download {self.url}")
        with get(self.url) as r:
            content = r.content
        return content


class DayBase(TimeUnitBase):
    @property
    def next(self):  # -> Day
        return DayBase.from_date(dt=self.dt + timedelta(days=1))

    @cached_property
    def yearmonth(self) -> MonthBase:
        return MonthBase(year=self.year, month=self.month)

    @property
    def name_file_csv(self) -> str:
        return f"{self.str_date}rtfuelmix.csv"

    @cached_property
    def last_modified(self) -> str:
        return self.yearmonth.last_modified

    @staticmethod
    def from_date(dt: date):  # -> Day:
        return DayBase(year=dt.year, month=dt.month, day=dt.day)
