import pandas as pd


def _remove_from_canon(
    canon_df: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    return canon_df[~canon_df["symbol"].isin(symbols)]


def _remove_from_returns(
    ret: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    return ret.drop(columns=[s for s in ret if s in symbols])


def remove_securities(
    canon_df: pd.DataFrame,
    ret: pd.DataFrame,
    symbols: str | list[str] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    if isinstance(symbols, str):
        symbols = [symbols]

    return (
        _remove_from_canon(canon_df=canon_df, symbols=symbols),
        _remove_from_returns(ret=ret, symbols=symbols),
    )


def remove_securities_leq_weight_w(
    canon_df: pd.DataFrame, ret: pd.DataFrame, w: float = 0.005
) -> tuple[pd.DataFrame, pd.DataFrame]:

    symbols = canon_df[canon_df["weight"] <= w].index.to_list()

    return remove_securities(canon_df=canon_df, ret=ret, symbols=symbols)
