import pandas as pd
import yfinance as yf


def fetch_current_prices(symbols: list[str]) -> pd.DataFrame:
    """
    Fetch current prices for a list of yfinance symbols.
    Returns a DataFrame with columns ['symbol', 'fetched_price"]
    """

    symbols = list(
        filter(lambda x: (x.endswith(".NS")), symbols)
    )  # Only fetch prices for symbols that end with .NS.

    # If the symbols list is empty, return an empty DataFrame with the correct columns
    if not symbols:
        return pd.DataFrame(columns=["symbol", "fetched_price"])

    prices = yf.download(
        tickers=symbols, period="1d", progress=False, threads=True
    )  # Fetch the latest price data for the given symbols using yfinance.

    # Extract the closing price for each symbol.
    if len(symbols) == 1:
        prices = {symbols[0]: prices["Close"].iloc[-1]}
    else:
        prices = prices["Close"].iloc[-1].to_dict()

    # Convert the prices dictionary to a DataFrame for easier merging with the portfolio data.
    prices_df = pd.DataFrame(
        list(prices.items()),
        columns=["symbol", "fetched_price"],
    )

    return prices_df


def fetch_historical_prices_n_years(
    symbols: list[str], n_years: int = 1
) -> pd.DataFrame:
    """Fetch historical prices for a list of yfinance symbols for the past n years."""

    # Filter the symbols to only include those that end with .NS.
    symbols = list(filter(lambda x: (x.endswith(".NS")), symbols))

    # If the symbols list is empty, return an empty DataFrame with the correct columns
    if not symbols:
        return pd.DataFrame(columns=["symbol", "fetched_price"])

    # Fetch historical price data for the given symbols and time period using yfinance.
    close_history_df = yf.download(
        tickers=symbols,
        period=str(n_years) + "y",
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=True,
    ).Close.copy()

    # Forward fill any missing values in the historical price data to ensure continuity in the time series.
    close_history_df = close_history_df.ffill()

    return close_history_df
