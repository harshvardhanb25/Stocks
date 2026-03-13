import os

# Base directory relative path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# File Paths
NSE_EQ_PATH = os.path.join(RAW_DATA_DIR, "nse_eq_master.csv")
NSE_ETF_PATH = os.path.join(RAW_DATA_DIR, "nse_etf_master.csv")
SGB_PATH = os.path.join(RAW_DATA_DIR, "SGBMAY28.csv")
PORTFOLIO_PATH = os.path.join(RAW_DATA_DIR, "current_portfolio.csv")

# Index map for proxy/benchmarking
INDEX_MAP = {
    "NIFTY 500": "NIFTY500.csv",
    "NIFTY NEXT 50": "NEXT50.csv",
    "NIFTY SMALLCAP 250": "SMALLCAP250.csv",
}
