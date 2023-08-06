"""general configuration
"""

from enum import Enum
from typing import NamedTuple, Optional
from os import getenv
from datetime import date
from datetime import date, timedelta, timezone


YEAR_START = 2015
MONTH_START = 12
DAY_START = 9
DATE_START = date(year=YEAR_START, month=MONTH_START, day=DAY_START)


FORMAT_DATE = "%Y%m%d"
TZ = timezone(timedelta(hours=-5))

class ParamsVarEnv(NamedTuple):
    key: str

    @property
    def value(self) -> Optional[str]:
        return getenv(self.key)


class VarEnv(ParamsVarEnv, Enum):
    TYPE_STORE = ParamsVarEnv(key="NYSMIX_STORE")
    FOLDER_ZIP = ParamsVarEnv(key="NYSMIX_FOLDER_ZIP")
    FOLDER_CSV = ParamsVarEnv(key="NYSMIX_FOLDER_CSV")
    TYPE_DB = ParamsVarEnv(key="NYSMIX_DB")