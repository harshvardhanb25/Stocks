import pandas as pd
import config
from utils.preprocessing import (
    normalize_column_headers,
    strip_string_values,
    convert_dates,
)
import glob
import os

INDEX_MAP = {
    "NIFTY 500": "NIFTY500.csv",
    "NIFTY NEXT 50": "NEXT50.csv",
    "NIFTY SMALLCAP 250": "SMALLCAP250.csv",
}

os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)

for index_name, out_file in INDEX_MAP.items():
    pattern = os.path.join(config.RAW_DATA_DIR, f"{index_name}_Historical_TR_*.csv")
    print(pattern)
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"no files found for: {index_name}")
        continue

    dfs = [pd.read_csv(file) for file in files]

    combined = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset="Date")
        .pipe(normalize_column_headers)
        .pipe(strip_string_values)
        .pipe(convert_dates, column_name="date")
        .drop_duplicates(subset=["date"])
        .set_index("date")
        .sort_index()
    )

    combined.to_csv(os.path.join(config.PROCESSED_DATA_DIR, out_file))
