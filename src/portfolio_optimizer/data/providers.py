from collections.abc import Sequence
from datetime import date
from typing import Protocol

import pandas as pd


class HistoricalPriceProvider(Protocol):
    """Interface for providers returning date-indexed prices by ticker."""

    def fetch_historical_prices(
        self,
        tickers: Sequence[str],
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """Return prices with dates as rows and requested tickers as columns."""
        ...
