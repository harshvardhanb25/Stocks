import glob

import pandas as pd

from portfolio_optimizer import config
from portfolio_optimizer.data.cleaning import (
    convert_dates,
    normalize_column_headers,
    strip_string_values,
)


def build_index_proxies() -> None:
    """Combine downloaded raw TRI CSV chunks into processed index files."""
    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for index_name, output_filename in config.INDEX_MAP.items():
        pattern = str(config.RAW_DATA_DIR / f"{index_name}_Historical_TR_*.csv")
        print(pattern)
        files = sorted(glob.glob(pattern))
        if not files:
            print(f"No files found for: {index_name}")
            continue

        frames = [pd.read_csv(file_path) for file_path in files]
        combined = (
            pd.concat(frames, ignore_index=True)
            .dropna(subset="Date")
            .pipe(normalize_column_headers)
            .pipe(strip_string_values)
            .pipe(convert_dates, column_name="date")
            .drop_duplicates(subset=["date"])
            .set_index("date")
            .sort_index()
            .rename(columns={"total_returns_index": index_name})
        )
        combined[[index_name]].to_csv(config.PROCESSED_DATA_DIR / output_filename)


def main() -> None:
    """Run the India index proxy builder from the command line."""
    build_index_proxies()


if __name__ == "__main__":
    main()
