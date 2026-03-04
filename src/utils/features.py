import pandas as pd
import numpy as np


def compute_daily_ret(price_history: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns for each security independently"""
    return price_history.pct_change().dropna(how="all")


def compute_annualized_mean_ret(ret: pd.DataFrame) -> pd.Series:
    """ "Compute annualized mean return for each security independently"""
    return ret.mean() * 252


def compute_individual_annualized_volatility(ret: pd.DataFrame) -> pd.Series:
    """Compute annualized volatility for each security independently"""
    return ret.std() * np.sqrt(252)


def _clean_outliers_series(stock: pd.Series, k: float = 8) -> pd.Series:
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

    threshold = k * robust_sigma
    return stock.clip(lower=median - threshold, upper=median + threshold)


def winsorize_returns(returns: pd.DataFrame, k: float = 8) -> pd.DataFrame:
    """Apply MAD-based winsorization independently to each security."""
    return returns.apply(_clean_outliers_series, k=k)
