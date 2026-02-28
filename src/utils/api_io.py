import pandas as pd
import yfinance as yf


def fetch_current_prices(symbols: list[str]) -> pd.DataFrame:
    """
    Fetch current prices for a list of yfinance symbols.
    Returns a DataFrame with columns ['symbol', 'fetched_price"]
    """
    if not symbols:
        return pd.DataFrame(columns=["symbol", "fetched_price"])

    prices = yf.download(tickers=symbols, period="1d", progress=False, threads=True)

    if len(symbols) == 1:
        prices = {symbols[0]: prices["Close"].iloc[-1]}
    else:
        prices = prices["Close"].iloc[-1].to_dict()

    prices_df = pd.DataFrame(
        list(prices.items()),
        columns=["symbol", "fetched_price"],
    )

    return prices_df


def fetch_historical_prices_n_years(
    symbols: list[str], n_years: int = 1
) -> pd.DataFrame:
    symbols = list(filter(lambda x: (x.endswith(".NS")), symbols))

    close_history_df = yf.download(
        tickers=symbols,
        period=str(n_years) + "y",
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=True,
    ).Close.copy()

    return close_history_df
