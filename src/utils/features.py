import pandas as pd

from portfolio_optimizer.core.returns import (
    annualized_mean_return,
    daily_returns,
    winsorize_returns as _winsorize_returns,
)
from portfolio_optimizer.core.risk import (
    annualized_volatility,
    correlation_matrix,
    covariance_matrix,
)


def compute_daily_ret(price_history: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns for each security independently"""
    return daily_returns(price_history)


def compute_annualized_mean_ret(
    ret: pd.DataFrame, periods_per_year: int = 252
) -> pd.Series:
    """ "Compute annualized mean return for each security independently"""
    return annualized_mean_return(ret, periods_per_year=periods_per_year)


def compute_individual_annualized_volatility(
    ret: pd.DataFrame, periods_per_year: int = 252
) -> pd.Series:
    """Compute annualized volatility for each security independently"""
    return annualized_volatility(ret, periods_per_year=periods_per_year)


def winsorize_returns(ret: pd.DataFrame, k: float = 8) -> pd.DataFrame:
    """Apply MAD-based winsorization independently to each security."""
    return _winsorize_returns(ret, k=k)


def compute_covariance_matrix(
    ret: pd.DataFrame, periods_per_year: int = 252
) -> pd.DataFrame:
    """Compute the annualized covariance matrix of returns."""
    return covariance_matrix(ret, periods_per_year=periods_per_year)


def compute_correlation_matrix(ret: pd.DataFrame) -> pd.DataFrame:
    """Compute the correlation matrix of returns."""
    return correlation_matrix(ret)
