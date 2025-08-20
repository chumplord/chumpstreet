import pandas as pd

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


def notna_to_none(val):
    return val if pd.notna(val) else None


class Error(BaseModel):
    context: Optional[str] = None
    message: str


class Ticker(BaseModel):
    trade_date: datetime
    ticker: str
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]

    @classmethod
    def from_yf_download(cls, data: dict, ticker: str):
        print(data)
        return Ticker(
            trade_date=data["Date"].to_pydatetime(),
            ticker=ticker,
            open=notna_to_none(data['Open']),
            high=notna_to_none(data['High']),
            low=notna_to_none(data['Low']),
            close=notna_to_none(data['Close']),
            volume=notna_to_none(data['Volume'])
        )


class MarketDataResponse(BaseModel):
    start_date: str
    end_date: str
    data: List[Ticker]
    errors: List[Error] = []

    @classmethod
    def error(cls, start_date: str, end_date: str, error_message: str):
        return MarketDataResponse(
            start_date=start_date,
            end_date=end_date,
            data=[],
            errors=[Error(message=error_message)]
        )


class MacroSeries(BaseModel):
    observation_date: date = Field(..., description="Observation date")
    value: float = Field(..., description="Value of the macroeconomic indicator")


class MacroData(BaseModel):
    series: List[str] = Field(..., description="FRED series name, e.g. GDP, CPIAUCSL")
    start_date: date
    end_date: date
    data: List[MacroSeries] = []
    errors: List[Error] = []
