import pandas as pd

from .returns import _validate_periods_per_year


def annualized_volatility(
    returns: pd.DataFrame, periods_per_year: int = 252
) -> pd.Series:
    """Annualize each asset's sample volatility."""
    _validate_periods_per_year(periods_per_year)
    return returns.std() * periods_per_year**0.5


def covariance_matrix(
    returns: pd.DataFrame, periods_per_year: int = 252
) -> pd.DataFrame:
    """Estimate annualized covariance from periodic returns."""
    _validate_periods_per_year(periods_per_year)
    return returns.cov() * periods_per_year


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Estimate pairwise asset return correlations."""
    return returns.corr()
