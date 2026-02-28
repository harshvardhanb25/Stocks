import pandas as pd


def build_canonical_portfolio(
    portfolio_df: pd.DataFrame, nse_eq_df: pd.DataFrame, nse_etf_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge the user portfolio with the NSE masters for equities and etfs,
    produce a single canonical df that is standardized for further analysis"""

    eq_etf_df = portfolio_df[portfolio_df.security_type.isin(["EQ", "ETF"])].copy()

    # print(eq_etf_df)

    complete_master = pd.concat([nse_eq_df, nse_etf_df], ignore_index=True)

    eq_etf_df = eq_etf_df.merge(
        complete_master[["isin", "symbol", "list_date"]], on="isin", how="left"
    )

    eq_etf_df["symbol"] = eq_etf_df["symbol"] + ".NS"

    eq_etf_df = eq_etf_df.loc[
        :,
        [
            "isin",
            "symbol",
            "security_type",
            "sector",
            "quantity",
            # "fetched_price", TODO
        ],
    ]

    # TODO: Use yf data to fix the current price to avoid any broker anomalies

    return eq_etf_df
