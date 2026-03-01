import pandas as pd
from .api_io import fetch_current_prices, fetch_historical_prices_n_years


def build_canonical_portfolio(
    portfolio_df: pd.DataFrame,
    nse_eq_df: pd.DataFrame,
    nse_etf_df: pd.DataFrame,
    sgb_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge the user portfolio with the NSE masters for equities, etfs, and sgb,
    produce a single canonical df that is standardized for further analysis"""

    # SGB data needs to be used from the csv since yfinance doesn't have proper support.
    sgb_row = portfolio_df[portfolio_df.security_type == "BOND"].copy()
    sgb_row["symbol"] = "SGBMAY28"
    sgb_row["fetched_price"] = sgb_df["SGBMAY28"].iloc[-1]

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
    prices_df = fetch_current_prices(symbols=eq_etf_df["symbol"].unique().tolist())
    eq_etf_df = eq_etf_df.merge(prices_df, on="symbol", how="left")

    # Combining EQ/ETF data with SGB data, and calculating current value and weights.
    canon = pd.concat([eq_etf_df, sgb_row], ignore_index=True)
    canon["current_value"] = canon["quantity"] * canon["fetched_price"]

    canon["weight"] = canon["current_value"] / canon["current_value"].sum()

    canon = canon.loc[
        :,
        [
            "isin",
            "symbol",
            "security_type",
            "sector",
            "quantity",
            "fetched_price",
            "current_value",
            "weight",
        ],
    ]

    return canon


def build_historical_price_dataset(
    eq_etf_historical: pd.DataFrame,
    sgb_df: pd.DataFrame,
) -> pd.DataFrame:
    """Join the fetched historical prices for eq+etf and sgb to get complete
    price history dataset"""
    return eq_etf_historical.join(sgb_df, how="left").ffill()
