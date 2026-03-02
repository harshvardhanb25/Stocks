import pandas as pd
import numpy as np


def compute_daily_ret(price_history: pd.DataFrame) -> pd.DataFrame:
    return price_history.pct_change().dropna(how="all")


def compute_annualized_mean_ret(ret: pd.DataFrame) -> pd.Series:
    return ret.mean() * 252


def compute_individual_annualized_volatility(ret: pd.DataFrame) -> pd.Series:
    return ret.std() * np.sqrt(252)


# TODO: Implement cov matrix logic
