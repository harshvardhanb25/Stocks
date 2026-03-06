import pandas as pd


def _remove_from_canon(
    canon_df: pd.DataFrame,
    symbols: str | list[str],
) -> pd.DataFrame:
    return canon_df[~canon_df["symbol"].isin(symbols)]


def _remove_from_returns(
    ret: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    return ret.drop(columns=[s for s in ret if s in symbols])
