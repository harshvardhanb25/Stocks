import pandas as pd
from .preprocessing import normalize_column_headers, strip_string_values, convert_dates


def load_and_clean_nse_eq_master(path: str) -> pd.DataFrame:
    """Loads and cleans the nse master csv for equities as a dataframe"""

    # Load the csv containing the nse master data
    df = pd.read_csv(path)

    # Normalize column headers and fix any string values
    df = df.pipe(normalize_column_headers).pipe(strip_string_values)

    # Fixing some dataset specific naming style
    df = df.rename(columns={"isin_number": "isin", "date_of_listing": "list_date"})

    # Convert lisitng dates to datetime
    df = df.pipe(convert_dates, column_name="list_date")

    return df


def load_and_clean_nse_etf_master(path: str) -> pd.DataFrame:
    """Loads and cleans the nse master csv for equities as a dataframe"""

    # Load the csv containing nse master data
    df = pd.read_csv(path)

    # Normalize column headers and fix any string values
    df = df.pipe(normalize_column_headers).pipe(strip_string_values)

    df = df.rename(columns={"isinnumber": "isin", "dateof_listing": "list_date"})

    # Convert listing dates to datetime
    df = df.pipe(convert_dates, column_name="list_date")

    return df


def load_and_clean_sgb(path: str) -> pd.DataFrame:
    """Loads and cleans the sgb price history"""

    # Load the csv containing the sgb price history
    df = pd.read_csv(path)

    # Convert dates to datetime and fix any string values
    df = df.pipe(convert_dates, column_name="Date")

    # Only keep the date and close price columns, and rename the close price column to SGBMAY28
    df = df[["Date", "Close Price"]].copy()

    # Fixing some dataset specific naming style
    df = df.rename(columns={"Close Price": "SGBMAY28"})

    # Set the date as the index and sort by date
    df = df.set_index("Date").sort_index()

    # Convert the close price to numeric

    return df
