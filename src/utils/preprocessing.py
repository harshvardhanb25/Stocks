import re
import pandas as pd


def to_snake_case(s: str) -> str:
    """Convert a given string (separated by spaces) to snake case"""
    s = s.strip()
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", s)
    s = re.sub(r"[^\w]+", "_", s)  # replace spaces & symbols with _
    s = re.sub(r"_+", "_", s)  # collapse multiple _
    return s.lower().strip("_")


def normalize_column_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names and conver them to snake case."""
    df.columns = [to_snake_case(c) for c in df.columns]

    return df


def strip_string_values(df: pd.DataFrame) -> pd.DataFrame:
    """Strips any string values of trailing/leading whitespace"""
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def convert_dates(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Convert dates to a datetime object"""
    df = df.copy()

    s = df[column_name]

    dt = pd.to_datetime(
        s, format="%d-%b-%y", errors="coerce"
    )  # Try parsing with 2-digit year first
    dt = dt.fillna(
        pd.to_datetime(s, format="%d-%b-%Y", errors="coerce")
    )  # If that fails, try parsing with 4-digit year
    dt = dt.fillna(
        pd.to_datetime(s, format="%d-%B-%Y", errors="coerce")
    )  # If that fails, try parsing with full month name and 4-digit year
    dt = dt.fillna(
        pd.to_datetime(s, format="%d %b %Y", errors="coerce")
    )  # If that fails, try parsing with spaces instead of dashes (this is for nifty indices)
    df[column_name] = dt

    # DEBUG — remove after fixing
    failed = df.loc[df[column_name].isna(), column_name]
    if not failed.empty:
        print(f"Failed to parse {len(failed)} rows:")
        print(failed.unique())

    assert df[column_name].notna().all()

    return df
