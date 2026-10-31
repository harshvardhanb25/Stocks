import math
from collections.abc import Mapping

import pandas as pd


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple period-over-period returns for each asset."""
    return prices.pct_change(fill_method=None).dropna(how="all")


def annualized_mean_return(
    returns: pd.DataFrame, periods_per_year: int = 252
) -> pd.Series:
    """Annualize each asset's arithmetic mean return."""
    _validate_periods_per_year(periods_per_year)
    return returns.mean() * periods_per_year


def winsorize_returns(returns: pd.DataFrame, k: float = 8) -> pd.DataFrame:
    """Clip returns beyond ``k`` median absolute deviations, scaled to sigma."""
    if not math.isfinite(k) or k <= 0:
        raise ValueError("k must be a finite positive number")

    def clip_series(series: pd.Series) -> pd.Series:
        median = series.median()
        mad = (series - median).abs().median()
        if pd.isna(mad) or mad == 0:
            return series.copy()

        threshold = k * 1.4826 * mad
        return series.clip(lower=median - threshold, upper=median + threshold)

    return returns.apply(clip_series)


def fill_with_proxy(
    returns: pd.DataFrame,
    proxy_returns: pd.DataFrame,
    proxy_map: Mapping[str, str],
) -> pd.DataFrame:
    """Backfill each asset's pre-history returns from its mapped proxy."""
    filled = returns.copy()
    aligned_proxies = proxy_returns.reindex(filled.index)

    for ticker, proxy_ticker in proxy_map.items():
        if ticker not in filled.columns:
            continue

        first_valid_date = filled[ticker].first_valid_index()
        if first_valid_date is None:
            continue
        if proxy_ticker not in aligned_proxies.columns:
            raise ValueError(f"Proxy returns do not contain {proxy_ticker!r}")

        before_history = filled.index < first_valid_date
        filled.loc[before_history, ticker] = aligned_proxies.loc[
            before_history, proxy_ticker
        ]

    return filled


def _validate_periods_per_year(periods_per_year: int) -> None:
    if (
        isinstance(periods_per_year, bool)
        or not isinstance(periods_per_year, int)
        or periods_per_year <= 0
    ):
        raise ValueError("periods_per_year must be a positive integer")
