import pandas as pd
import yfinance as yf


def fetch_current_prices(symbols: list[str]) -> pd.DataFrame:
    """
    Fetch current prices for a list of yfinance symbols.
    Returns a DataFrame with columns ['symbol', 'fetched_price"]
    """
    if not symbols:
        return pd.DataFrame(columns=["symbol", "fetched_price"])

    prices = yf.download(symbols, period="1d", progress=False, threads=True)

    if len(symbols) == 1:
        prices = {symbols[0]: prices["Close"].iloc[-1]}
    else:
        prices = prices["Close"].iloc[-1].to_dict()

    prices_df = pd.DataFrame(
        list(prices.items()),
        columns=["symbol", "fetched_price"],
    )

    return prices_df
