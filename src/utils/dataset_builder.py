import pandas as pd
from .api_io import fetch_current_prices


def build_canonical_portfolio(
    portfolio_df: pd.DataFrame, nse_eq_df: pd.DataFrame, nse_etf_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge the user portfolio with the NSE masters for equities and etfs,
    produce a single canonical df that is standardized for further analysis"""

    # Only keep equities and etfs for now, since we don't have a good way to get current prices for the other security types.
    eq_etf_df = portfolio_df[portfolio_df.security_type.isin(["EQ", "ETF"])].copy()

    # Merge with the NSE master data to get the symbols and listing dates for the equities and etfs in the portfolio.
    complete_master = pd.concat([nse_eq_df, nse_etf_df], ignore_index=True)

    # Merge on isin to get the symbol and list date for each security in the portfolio.
    eq_etf_df = eq_etf_df.merge(
        complete_master[["isin", "symbol", "list_date"]], on="isin", how="left"
    )

    # Add the .NS suffix to the symbols to make them compatible with yfinance.
    eq_etf_df["symbol"] = eq_etf_df["symbol"] + ".NS"

    # Fetch current prices for the equities and etfs in the portfolio using yfinance,
    # and calculate the current value of each holding based on the quantity and fetched price.
    prices_df = fetch_current_prices(eq_etf_df["symbol"].unique().tolist())
    eq_etf_df = eq_etf_df.merge(prices_df, on="symbol", how="left")
    eq_etf_df["current_value"] = eq_etf_df["quantity"] * eq_etf_df["fetched_price"]

    eq_etf_df = eq_etf_df.loc[
        :,
        [
            "isin",
            "symbol",
            "security_type",
            "sector",
            "quantity",
            "fetched_price",
            "current_value",
        ],
    ]

    return eq_etf_df
