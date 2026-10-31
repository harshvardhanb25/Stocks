"""Paths and index definitions for the legacy India-data adapters."""

import os
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("PORTFOLIO_PROJECT_ROOT", Path.cwd())).resolve()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

NSE_EQ_PATH = RAW_DATA_DIR / "nse_eq_master.csv"
NSE_ETF_PATH = RAW_DATA_DIR / "nse_etf_master.csv"
SGB_PATH = RAW_DATA_DIR / "SGBMAY28.csv"
PORTFOLIO_PATH = RAW_DATA_DIR / "current_portfolio.csv"

INDEX_MAP = {
    "NIFTY 500": "NIFTY500.csv",
    "NIFTY NEXT 50": "NEXT50.csv",
    "NIFTY SMALLCAP 250": "SMALLCAP250.csv",
    "NIFTY IT": "NIFTYIT.csv",
}

__all__ = [
    "DATA_DIR",
    "INDEX_MAP",
    "NSE_EQ_PATH",
    "NSE_ETF_PATH",
    "PORTFOLIO_PATH",
    "PROCESSED_DATA_DIR",
    "PROJECT_ROOT",
    "RAW_DATA_DIR",
    "SGB_PATH",
]
