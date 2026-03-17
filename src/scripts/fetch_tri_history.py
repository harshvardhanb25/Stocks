import time
import json
import requests
import pandas as pd
import os
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import config
from utils.preprocessing import (
    normalize_column_headers,
    strip_string_values,
    convert_dates,
)

os.makedirs(config.RAW_DATA_DIR, exist_ok=True)

BASE_URL = "https://www.niftyindices.com"
TRI_ENDPOINT = f"{BASE_URL}/Backpage.aspx/getTotalReturnIndexString"
DATE_FMT = "%d-%b-%Y"
CHUNK_DAYS = 364

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": f"{BASE_URL}/reports/historical-data",
}


def date_chunks(
    start: date, end: date, chunk_days: int = CHUNK_DAYS
) -> list[tuple[date, date]]:
    """Split a date range into non-overlapping windows of at most chunk_days."""
    chunks = []
    cursor = start
    while cursor <= end:
        window_end = min(cursor + timedelta(days=chunk_days - 1), end)
        chunks.append((cursor, window_end))
        cursor = window_end + timedelta(days=1)
    return chunks


def fetch_tri_history(index_name: str, n_years: int = 10) -> pd.DataFrame:
    """Fetch TRI history for a niftyindices.com index, chunked into sub-year windows."""
    end_date = date.today()
    start_date = end_date - relativedelta(years=n_years)

    session = requests.Session()
    # Seed cookies by hitting the historical data page first
    session.get(
        f"{BASE_URL}/reports/historical-data",
        headers={"User-Agent": HEADERS["User-Agent"]},
    )

    chunks = date_chunks(start_date, end_date)
    frames = []

    for i, (chunk_start, chunk_end) in enumerate(chunks, 1):
        print(
            f"  [{index_name}] chunk {i}/{len(chunks)}: {chunk_start.strftime(DATE_FMT)} → {chunk_end.strftime(DATE_FMT)}"
        )

        resp = session.post(
            TRI_ENDPOINT,
            headers=HEADERS,
            json={
                "cinfo": f"{{'name':'{index_name}','startDate':'{chunk_start.strftime(DATE_FMT)}','endDate':'{chunk_end.strftime(DATE_FMT)}','indexName':'{index_name}'}}"
            },
        )
        resp.raise_for_status()

        # API returns JSON with escaped JSON in "d"
        frames.append(pd.DataFrame(json.loads(json.loads(resp.text)["d"])))

        time.sleep(0.5)

    combined = (
        pd.concat(frames, ignore_index=True)
        .pipe(normalize_column_headers)
        .pipe(strip_string_values)
        .pipe(convert_dates, column_name="date")
        .drop_duplicates(subset=["date"])
        .set_index("date")
        .sort_index()
        .rename(columns={"total_returns_index": index_name})
    )

    return combined[[index_name]]


for index_name in config.INDEX_MAP:
    print(f"\nFetching: {index_name}")
    df = fetch_tri_history(index_name=index_name, n_years=10)

    out_filename = f"{config.INDEX_MAP[index_name]}"
    out_path = os.path.join(config.PROCESSED_DATA_DIR, out_filename)
    df.to_csv(out_path)

    print(f"  Saved → {out_path}  ({len(df)} rows)")
