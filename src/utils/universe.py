from typing import Optional, Union

import pandas as pd


def _remove_from_canon(
    canon_df: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    """Drop given symbols from the canonical portfolio DataFrame."""
    return canon_df[~canon_df["symbol"].isin(symbols)]


def _remove_from_returns(
    ret: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    """Drop given symbols from the returns/price series DataFrame."""
    return ret.drop(columns=[s for s in ret if s in symbols])


def remove_securities(
    canon_df: pd.DataFrame,
    ret: pd.DataFrame,
    symbols: Union[str, list[str], None] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Remove one or more securities from both canonical portfolio and return series."""
    if isinstance(symbols, str):
        symbols = [symbols]

    return (
        _remove_from_canon(canon_df=canon_df, symbols=symbols),
        _remove_from_returns(ret=ret, symbols=symbols),
    )


def remove_securities_leq_weight_w(
    canon_df: pd.DataFrame, ret: pd.DataFrame, w: float = 0.005
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop securities whose weight is less than or equal to threshold `w`."""
    symbols = canon_df[canon_df["weight"] <= w].index.to_list()

    return remove_securities(canon_df=canon_df, ret=ret, symbols=symbols)
