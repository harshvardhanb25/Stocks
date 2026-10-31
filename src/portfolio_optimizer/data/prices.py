from collections.abc import Sequence

import numpy as np
import pandas as pd


def validate_price_history(
    prices: pd.DataFrame, tickers: Sequence[str] | None = None
) -> pd.DataFrame:
    """Validate and order date-indexed positive prices, allowing missing observations."""
    if not isinstance(prices, pd.DataFrame) or prices.empty:
        raise ValueError("prices must be a non-empty DataFrame")
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise ValueError("prices must use a DatetimeIndex")
    if prices.index.hasnans:
        raise ValueError("price dates cannot be missing")
    if prices.index.has_duplicates:
        raise ValueError("price dates must be unique")
    if prices.columns.has_duplicates:
        raise ValueError("price ticker columns must be unique")
    if not all(isinstance(ticker, str) and ticker.strip() for ticker in prices.columns):
        raise ValueError("price columns must be non-empty ticker strings")

    validated = prices.copy()
    if tickers is not None:
        requested = list(tickers)
        if not requested:
            raise ValueError("tickers must contain at least one ticker")
        if not all(isinstance(ticker, str) and ticker.strip() for ticker in requested):
            raise ValueError("requested tickers must be non-empty strings")
        if len(requested) != len(set(requested)):
            raise ValueError("requested tickers must be unique")
        missing = [ticker for ticker in requested if ticker not in validated.columns]
        if missing:
            raise ValueError(f"price history is missing ticker(s): {missing!r}")
        validated = validated.loc[:, requested]

    try:
        validated = validated.apply(pd.to_numeric, errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError("prices must contain numeric values") from error

    values = validated.to_numpy(dtype=float)
    if np.isinf(values).any():
        raise ValueError("prices cannot contain infinite values")
    if (validated <= 0).any().any():
        raise ValueError("observed prices must be positive")
    if validated.isna().all().any():
        empty_tickers = validated.columns[validated.isna().all()].tolist()
        raise ValueError(f"price history has no observations for: {empty_tickers!r}")

    return validated.sort_index()
