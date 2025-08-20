import logging
import os
from typing import List

import yfinance as yf
from fastmcp import FastMCP
from fredapi import Fred

from chumpstreet.model import (
    Ticker,
    MacroData,
    MacroSeries,
    MarketDataResponse,
    Error
)

fred_api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=fred_api_key)
logger = logging.getLogger(__name__)


def no_tickers_given_error_response(start_date: str, end_date: str) -> MarketDataResponse:
    return MarketDataResponse.error(start_date, end_date, 'Tickers must be a non-empty list of strings')


def download_failed_error_response(start_date: str, end_date: str, error: str) -> MarketDataResponse:
    return MarketDataResponse.error(start_date, end_date, f'Download failed: {error}')


def no_tickers_data_error_response(start_date: str, end_date: str, tickers: str) -> MarketDataResponse:
    return MarketDataResponse.error(start_date, end_date, f'No data returned for tickers: {tickers}')


def create_server() -> FastMCP:
    """Create and return the FastMCP server instance with all tools registered."""
    app = FastMCP("ChumpStreet")

    @app.tool
    def get_market_data(tickers: List[str], start_date: str, end_date: str) -> MarketDataResponse:
        """Return OHLCV market data for a given ticker and date range."""
        if not tickers or not isinstance(tickers, list):
            return no_tickers_given_error_response(start_date, end_date)

        try:
            df = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
        except Exception as e:
            logger.exception("yfinance download failed")
            return download_failed_error_response(start_date, end_date, str(e))

        if df.empty:
            return no_tickers_data_error_response(start_date, end_date, tickers)

        errors: List[Error] = []
        all_data: List[Ticker] = []

        for ticker in tickers:
            try:
                ticker_df = df[ticker].reset_index()
            except KeyError:
                errors.append(Error(context=ticker, message="No data found for ticker"))
                continue

            for _, row in ticker_df.iterrows():
                try:
                    record = Ticker.from_yf_download(row, ticker)
                    all_data.append(record)
                except Exception as e:
                    logger.error(f"Failed to parse row for ticker {ticker}: {e}")
                    errors.append(Error(context=ticker, message=f"Row parse failed: {e}"))

        return MarketDataResponse(
            start_date=start_date,
            end_date=end_date,
            data=all_data,
            errors=errors
        )

    @app.tool
    def get_macro_data(series_list: List[str], start_date: str, end_date: str) -> MacroData:
        """Return macroeconomic data from FRED for a given list of series and date range."""
        records: List[MacroSeries] = []
        errors: List[Error] = []

        for series in series_list:
            try:
                data = fred.get_series(series, observation_start=start_date, observation_end=end_date)
                records.extend(MacroSeries(observation_date=index.date(), value=float(val)) for index, val in data.items())
            except ValueError as e:
                errors.append(Error(context=series, message=str(e)))

        return MacroData(
            series=series_list,
            start_date=start_date,
            end_date=end_date,
            data=records,
            errors=errors
        )

    return app


if __name__ == "__main__":
    chump_street = create_server()
    chump_street.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        show_banner=True
    )
