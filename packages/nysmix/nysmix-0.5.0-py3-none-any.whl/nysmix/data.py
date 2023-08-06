"""
data implementations that optionally uses joblib caching
"""

from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from io import BytesIO
from logging import info
from typing import List, Optional

from pandas import concat, read_csv
from pandera import check_types
from pandera.typing import DataFrame

from .base import DayBase, MonthBase
from .config import TZ, YEAR_START, DATE_START
from .schema import Summary
from .utils import get_content, get_zip, summarize, collect_summaries
from .abstractions import TimeUnit
from abc import abstractproperty


class HasSubunits(TimeUnit):
    @abstractproperty
    def subunits(self) -> List[TimeUnit]:
        pass

    @property
    def last_modified(self) -> str:
        return self.subunits[-1].last_modified

    @property
    def summary(self) -> DataFrame[Summary]:
        return self.memory.cache(collect_summaries)(
            time_units=self.subunits, last_modified=self.last_modified
        )


@dataclass(frozen=True)
class Day(TimeUnit):
    day_base: DayBase = DayBase.from_date(DATE_START)

    @property
    def last_modified(self) -> str:
        return self.day_base.last_modified

    @cached_property
    def content(self) -> bytes:
        return self.memory.cache(get_content)(
            name_file_csv=self.day_base.name_file_csv,
            zip=self.month.zip,
            last_modified=self.last_modified,
        )

    @cached_property
    def df(self) -> DataFrame:
        with BytesIO(self.content) as f:
            df = read_csv(f, dtype=object)
        return df

    @property
    def summary(self) -> DataFrame[Summary]:
        info(f"summarizing {self}")
        return self.memory.cache(summarize)(df=self.df)

    @property
    def month(self):  # -> Month
        return Month(
            month_base=MonthBase.from_date(self.day_base.dt), memory=self.memory
        )


@dataclass(frozen=True)
class Month(HasSubunits):
    month_base: MonthBase = MonthBase.from_date(DATE_START)

    @property
    def subunits(self) -> List[TimeUnit]:
        days = []
        current = DayBase.from_date(dt=self.month_base.dt)
        while current.yearmonth == self.month_base:
            if not current.is_before_start and not current.is_future:
                days.append(current)
            current = current.next
        return [Day(day_base=day, memory=self.memory) for day in days]

    @property
    def last_modified(self) -> str:
        return self.month_base.last_modified

    @property
    def zip(self) -> bytes:
        return self.memory.cache(get_zip)(
            obj=self.month_base, last_modified=self.last_modified
        )


@dataclass(frozen=True)
class Year(HasSubunits):
    year: int = YEAR_START

    @property
    def subunits(self) -> List[TimeUnit]:
        return [
            Month(memory=self.memory, month_base=month)
            for month in [
                MonthBase(year=self.year, month=month) for month in range(1, 13)
            ]
            if not month.is_future and not month.is_before_start
        ]


@dataclass(frozen=True)
class All(HasSubunits):
    @property
    def subunits(self) -> List[TimeUnit]:
        now = datetime.now(TZ)
        return [
            Year(memory=self.memory, year=year)
            for year in range(YEAR_START, now.year + 1)
        ]
