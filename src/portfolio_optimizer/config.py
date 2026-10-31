"""Paths and index definitions for the legacy India-data adapters."""

import os
from pathlib import Path


def _resolve_project_root(start: Path | None = None) -> Path:
    """Use the configured root or find the nearest parent containing pyproject.toml."""
    override = os.environ.get("PORTFOLIO_PROJECT_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    directory = (start or Path.cwd()).resolve()
    for candidate in (directory, *directory.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find pyproject.toml in {directory} or any parent directory"
    )


PROJECT_ROOT = _resolve_project_root()
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
