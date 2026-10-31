import re

import pandas as pd

DATE_FORMATS = ("%d-%b-%y", "%d-%b-%Y", "%d-%B-%Y", "%d %b %Y")


def to_snake_case(value: str) -> str:
    """Convert a label to lowercase snake case."""
    value = value.strip()
    value = re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", value)
    value = re.sub(r"[^\w]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.lower().strip("_")


def normalize_column_headers(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe column labels in place."""
    frame.columns = [to_snake_case(str(column)) for column in frame.columns]
    return frame


def strip_string_values(frame: pd.DataFrame) -> pd.DataFrame:
    """Strip surrounding whitespace from string-valued dataframe cells."""
    for column in frame.select_dtypes(include=["object", "string"]).columns:
        frame[column] = frame[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    return frame


def convert_dates(frame: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Parse supported day-first date formats and report invalid source values."""
    converted = frame.copy()
    source = converted[column_name]
    parsed = pd.Series(pd.NaT, index=source.index, dtype="datetime64[ns]")

    for date_format in DATE_FORMATS:
        parsed = parsed.fillna(
            pd.to_datetime(source, format=date_format, errors="coerce")
        )

    invalid = parsed.isna()
    if invalid.any():
        values = source.loc[invalid].drop_duplicates().tolist()
        raise ValueError(
            f"Could not parse {int(invalid.sum())} value(s) in {column_name!r}: {values!r}"
        )

    converted[column_name] = parsed
    return converted
