"""
General utilities
"""
from functools import cache
from io import BytesIO
from logging import info
from typing import Dict, Optional, List
from zipfile import ZipFile

from pandas import concat
from pandera import check_types
from pandera.typing import DataFrame
from requests import get

from .abstractions import HasURL, HasZip, TimeUnit
from .concepts import SimpleFuel
from .schema import Snapshot, Summary

LABEL: Dict[SimpleFuel, str] = {
    SimpleFuel.FOSSIL_FUEL: "Fossil fuel",
    SimpleFuel.RENEWABLE: "Renewable",
    SimpleFuel.NUCLEAR: "Nuclear",
}

@cache
def get_last_modified(obj: HasURL) -> str:
    info(f"getting last modified for {obj}")
    with get(obj.url) as r:
        headers = r.headers
    return headers["Last-Modified"]


def get_zip(obj: HasZip, last_modified: Optional[str] = None) -> bytes:
    return obj.zip


def get_content(name_file_csv: str, zip: bytes, last_modified: Optional[str] = None) -> bytes:
    with BytesIO(zip) as f:
        with ZipFile(f) as zf:
            content = zf.read(name_file_csv)
    return content


def get_name_field_gen_mw(df: DataFrame[Snapshot]) -> str:
    return set(df.columns).intersection({Snapshot.gen_mw, Snapshot.gen_mwh}).pop()


@check_types
def summarize(df: DataFrame[Snapshot]) -> DataFrame[Summary]:
    df[Summary.date] = df[Snapshot.timestamp].dt.date
    return (
        df.rename(columns={get_name_field_gen_mw(df): Summary.gen_mw})
        .groupby([Summary.date, Snapshot.fuel], as_index=False)
        .agg({Summary.gen_mw: "sum"})
    )


@check_types
def collect_summaries(
    time_units: List[TimeUnit], last_modified: Optional[str] = None
) -> DataFrame[Summary]:
    return concat([time_unit.summary for time_unit in time_units])
