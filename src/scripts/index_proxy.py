import pandas as pd
import config
from utils.preprocessing import (
    normalize_column_headers,
    strip_string_values,
    convert_dates,
)
import glob
import os

os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)

# For each index, find all raw CSV chunks and merge them into a single cleaned series.
for index_name, out_file in config.INDEX_MAP.items():
    pattern = os.path.join(config.RAW_DATA_DIR, f"{index_name}_Historical_TR_*.csv")
    print(pattern)
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"no files found for: {index_name}")
        continue

    # Read all chunk files for this index.
    dfs = [pd.read_csv(file) for file in files]

    # Concatenate, clean up, and keep only the index series.
    combined = (
        pd.concat(dfs, ignore_index=True)
        .dropna(subset="Date")
        .pipe(normalize_column_headers)
        .pipe(strip_string_values)
        .pipe(convert_dates, column_name="date")
        .drop_duplicates(subset=["date"])
        .set_index("date")
        .sort_index()
        .rename(columns={"total_returns_index": index_name})
    )

    combined = combined[[index_name]]

    combined.to_csv(os.path.join(config.PROCESSED_DATA_DIR, out_file))
