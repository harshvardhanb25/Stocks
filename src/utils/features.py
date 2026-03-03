import pandas as pd
import numpy as np


def compute_daily_ret(price_history: pd.DataFrame) -> pd.DataFrame:
    return price_history.pct_change().dropna(how="all")


def compute_annualized_mean_ret(ret: pd.DataFrame) -> pd.Series:
    return ret.mean() * 252


def compute_individual_annualized_volatility(ret: pd.DataFrame) -> pd.Series:
    return ret.std() * np.sqrt(252)


def _clean_outliers_series(stock: pd.Series) -> pd.Series:
    """
    MAD-based winsorization for a single return series.
    Only clips values beyond 8 robust sigma — genuine data artifacts only.
    """
    median = stock.median()
    mad = (stock - median).abs().median()
    robust_sigma = 1.4826 * mad

    extreme_mask = ((stock - median) / robust_sigma).abs() >= 8
    if not extreme_mask.any():
        return stock

    threshold = 8 * robust_sigma
    return stock.clip(lower=median - threshold, upper=median + threshold)


def winsorize_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Apply MAD-based winsorization independently to each security."""
    return returns.apply(_clean_outliers_series)


# TODO: Implement cov matrix logic
