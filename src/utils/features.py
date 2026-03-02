import pandas as pd


def compute_daily_ret(price_history: pd.DataFrame) -> pd.DataFrame:
    return price_history.pct_change().dropna(how="all")


def compute_annualized_mean_ret(ret: pd.DataFrame) -> pd.Series:
    return ret.mean() * 252


# TODO: Implement cov matrix logic
