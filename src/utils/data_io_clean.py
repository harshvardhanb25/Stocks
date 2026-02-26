import pandas as pd
from .preprocessing import normalize_column_headers, strip_string_values


def load_and_clean_nse_eq_master(path: str) -> pd.DataFrame:
    """Loads and cleans a cleaned nse master csv for equities as a dataframe"""

    # Load the csv containing the nse master data
    df = pd.read_csv(path)

    # Normalize column headers and fix any string values
    df = df.pipe(normalize_column_headers).pipe(strip_string_values)

    # Fixing some dataset specific naming style
    df = df.rename(columns={"isin_number": "isin", "date_of_listing": "list_date"})

    # TODO: Fix dates
    return df
