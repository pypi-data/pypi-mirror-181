from pandera import SchemaModel, Field, dataframe_check
from pandera.typing import Series, DataFrame
from datetime import datetime, date
from .concepts import Fuel, NAME
from typing import Optional


class Snapshot(SchemaModel):
    timestamp: Series[datetime] = Field(alias="Time Stamp", coerce=True)
    timezone: Series[str] = Field(isin=["EST", "EDT"], alias="Time Zone")
    fuel: Series[str] = Field(isin=[NAME[fuel] for fuel in Fuel], alias="Fuel Category")
    gen_mwh: Optional[Series[float]] = Field(coerce=True, alias="Gen MWh", ge=0)
    gen_mw: Optional[Series[float]] = Field(coerce=True, alias="Gen MW", ge=0)

    @dataframe_check
    def has_one_gen_mw_field(self, df: DataFrame) -> bool:
        return len(set(df.columns).intersection({self.gen_mw, self.gen_mwh})) == 1


class Summary(SchemaModel):
    date: Series[date]
    fuel: Series[str] = Field(isin=[NAME[fuel] for fuel in Fuel], alias="Fuel Category")
    gen_mw: Series[float]
