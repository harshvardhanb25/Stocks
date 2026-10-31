# Stocks

A portfolio analytics and optimization toolkit being refactored from an NSE- and broker-specific prototype into a provider-independent Python package. The new package establishes the reusable input models, price-data contract, and portfolio calculations before adding global ticker resolution, optimization workflows, or the Streamlit interface.

## Project Structure

```
Stocks/
├── data/
│   ├── raw/                          # Raw CSV data files (gitignored)
│   └── processed/                    # Processed / cleaned outputs
├── notebooks/
│   ├── 00_exploration.ipynb          # Initial data exploration and rough experimentation
│   └── 01_data_cleaning.ipynb        # Data cleaning walkthroughs
├── src/
│   ├── portfolio_optimizer/          # Provider-independent toolkit package
│   │   ├── core/                     # Return, risk, and portfolio calculations
│   │   ├── data/                     # Cleaning and price-data contracts
│   │   │   └── providers.py           # Historical price provider interface
│   │   ├── adapters/india/           # Packaged India-specific index adapters and commands
│   │   ├── config.py                 # Config for retained India-data workflows
│   │   └── models.py                 # Ticker-and-quantity holdings models
│   ├── config.py                     # Compatibility import for old notebooks
│   ├── scripts/                      # Compatibility launchers for packaged commands
│   └── utils/                        # Legacy NSE/broker workflow and compatibility imports
│       ├── __init__.py               # Public API exports
│       ├── api_io.py                 # yfinance data fetching
│       ├── data_io_clean.py          # Raw data loaders & cleaners
│       ├── dataset_builder.py        # Portfolio, price history & index dataset builders
│       ├── features.py               # Return & volatility computations
│       ├── preprocessing.py          # General-purpose data cleaning helpers
│       └── universe.py               # Security universe management
├── tests/                            # Tests for the extracted core
├── .pre-commit-config.yaml
└── pyproject.toml
```

### Package Boundary

`portfolio_optimizer` contains ticker-and-quantity models, provider-independent return and risk calculations, generic tabular cleaning helpers, and a historical-price provider interface. The old `utils` modules remain available to keep the NSE/broker notebooks working, but they are not the new toolkit API. No provider implementation currently resolves worldwide tickers, and currency conversion, optimization workflows, and the Streamlit UI remain future work.

## What's Built So Far

### Data Ingestion & Cleaning (`data_io_clean.py`, `preprocessing.py`)
Loaders for four raw data sources — NSE equity master, NSE ETF master, SGB (Sovereign Gold Bond) price history, and a broker-exported portfolio CSV. Each loader normalises column headers to `snake_case`, strips whitespace, parses multiple date formats robustly, and standardises security type labels (`EQUITY STOCK` → `EQ`, etc.).

### API Layer (`api_io.py`)
Two `yfinance` wrappers for `.NS`-suffixed symbols:
- `fetch_current_prices` — fetches the latest closing price for a list of symbols using a 1-day download with threading.
- `fetch_historical_prices_n_years` — fetches `n` years of daily adjusted close history, forward-filling any gaps.

### TRI History Fetcher (`scripts/fetch_tri_history.py`)
Automatically downloads Total Return Index (TRI) history from [niftyindices.com](https://www.niftyindices.com) for all indices defined in `config.INDEX_MAP`. Key details:
- Splits the requested date range (default: 10 years) into ≤364-day chunks to comply with the API's window limits.
- Seeds session cookies by first hitting the niftyindices historical-data page, then POSTs to the `getTotalReturnIndexString` endpoint for each chunk.
- Concatenates all chunks, normalises headers, strips whitespace, parses dates, deduplicates, sorts, and writes a clean CSV per index to `data/processed/`.
- Run it directly (`python src/scripts/fetch_tri_history.py`) to refresh all benchmark CSVs in one go.

### Portfolio Builder (`dataset_builder.py`)
- `build_canonical_portfolio` — merges the broker portfolio with the NSE master data on ISIN, attaches live prices via `fetch_current_prices`, handles SGB separately (yfinance has no support), and outputs a single standardised dataframe with columns: `isin`, `symbol`, `security_type`, `sector`, `quantity`, `fetched_price`, `current_value`, and `weight`.
- `build_historical_price_dataset` — joins the yfinance equity/ETF price history with the SGB CSV history into one aligned time-series dataframe.
- `build_index_prices` — loads a single pre-processed index price series from `data/processed/` by name, returning a labelled `pd.Series`.
- `build_index_price_dataset` — combines all index price series defined in `config.INDEX_MAP` into one aligned `pd.DataFrame`.

### Feature Engineering (`features.py`)
- Daily percentage returns (`compute_daily_ret`)
- Annualised mean return (`compute_annualized_mean_ret`, ×252)
- Annualised volatility per security (`compute_individual_annualized_volatility`, ×√252)
- MAD-based winsorization (`winsorize_returns`) — clips extreme outliers beyond a configurable `k` robust-sigma threshold (default 8) per security independently, preserving genuine data while removing artefacts.

### Universe Management (`universe.py`)
- `remove_securities` — drops one or more symbols from both the canonical portfolio dataframe and the returns dataframe simultaneously, keeping them in sync. Accepts a single symbol string or a list.
- `remove_securities_leq_weight_w` — convenience wrapper that automatically identifies and removes all securities whose portfolio weight is at or below a threshold `w` (default 0.5%), useful for trimming negligible positions before optimisation.

### Index Benchmark Builder (`scripts/index_proxy.py`)
Processes historical total-return CSV files for NSE indices downloaded from NSE India. For each index, the script:
- Globs all matching raw CSV files and concatenates them.
- Normalises headers, strips whitespace, and parses dates (with debug logging for failed parses).
- Deduplicates and sorts by date, then writes a clean, date-indexed CSV to `data/processed/`.

> **Note:** `fetch_tri_history.py` supersedes the manual CSV workflow handled by `index_proxy.py` for most use cases.

### Configuration (`config.py`)
Centralised path resolution for all raw and processed data files relative to the project root, so nothing is hardcoded in notebooks or scripts. Exposes:
- `RAW_DATA_DIR`, `PROCESSED_DATA_DIR` — base directory paths
- `NSE_EQ_PATH`, `NSE_ETF_PATH`, `SGB_PATH`, `PORTFOLIO_PATH` — individual raw file paths
- `INDEX_MAP` — mapping of index names to their processed CSV filenames, used by `build_index_price_dataset` and `fetch_tri_history.py`

Currently tracked indices:

| Index Name | Processed File |
|---|---|
| `NIFTY 500` | `NIFTY500.csv` |
| `NIFTY NEXT 50` | `NEXT50.csv` |
| `NIFTY SMALLCAP 250` | `SMALLCAP250.csv` |
| `NIFTY IT` | `NIFTYIT.csv` |

### Public API (`utils/__init__.py`)
All utility functions are re-exported from `src/utils` for clean imports in notebooks:

```python
from utils import (
    # Preprocessing
    to_snake_case, normalize_column_headers, strip_string_values, convert_dates, fill_with_proxy,
    # Data IO + Cleaning
    load_and_clean_nse_eq_master, load_and_clean_nse_etf_master, load_and_clean_sgb, load_and_clean_broker,
    # Dataset building
    build_canonical_portfolio, build_historical_price_dataset, build_index_price_dataset, build_index_prices,
    # API IO
    fetch_current_prices, fetch_historical_prices_n_years,
    # Features
    compute_daily_ret, compute_annualized_mean_ret, compute_individual_annualized_volatility, winsorize_returns,
    # Universe
    remove_securities, remove_securities_leq_weight_w,
)
```

## Data Sources

| File | Location | Description |
|---|---|---|
| `nse_eq_master.csv` | `data/raw/` | NSE equity master list (ISIN, symbol, listing date) |
| `nse_etf_master.csv` | `data/raw/` | NSE ETF master list |
| `SGBMAY28.csv` | `data/raw/` | Sovereign Gold Bond (May 2028) price history |
| `current_portfolio.csv` | `data/raw/` | Broker-exported portfolio holdings |
| `NIFTY500.csv`, `NEXT50.csv`, `SMALLCAP250.csv`, `NIFTYIT.csv` | `data/processed/` | Cleaned, deduplicated TRI index series |

> Raw data files are excluded from version control via `.gitignore`. Processed index CSVs are auto-generated by `fetch_tri_history.py`.

## Setup

```bash
# Install dependencies (requires Python 3.11+)
pip install -e ".[dev]"

# Run tests
python -m pytest

# Install pre-commit hooks
pre-commit install

# Install dependencies used by the legacy yfinance notebooks
pip install -e ".[legacy,notebooks]"

# Install optional dependencies for India-specific TRI data scripts
pip install -e ".[india-data]"

# Fetch/refresh all TRI benchmark data
portfolio-fetch-tri-history

# Build index files from previously downloaded raw CSVs
portfolio-build-index-proxies
```

The India-data configuration searches the current directory and its parents for the nearest `pyproject.toml`. Set `PORTFOLIO_PROJECT_ROOT` to override that root.

## Roadmap

### Portfolio Optimisation
- [ ] Mean-variance optimisation (maximum Sharpe, minimum volatility) using `cvxpy` or `PyPortfolioOpt`
- [ ] Efficient frontier visualisation
- [ ] Target return / target risk constrained optimisation
- [ ] Weight bounds and sector concentration constraints

### Risk Analytics
- [ ] Sharpe ratio, Sortino ratio, Calmar ratio
- [ ] Maximum drawdown and drawdown duration
- [ ] Portfolio Beta vs. Nifty 50
- [ ] Value at Risk (VaR) and Conditional VaR (CVaR)
- [ ] Rolling correlation heatmaps

### Allocation & Attribution
- [ ] Sector-level and asset-class-level allocation breakdown
- [ ] Performance attribution vs. a benchmark (Nifty 500)
- [ ] Drift tracking and rebalancing triggers

### Backtesting
- [ ] Historical backtest of current portfolio weights
- [ ] Rebalancing strategy simulation (monthly, quarterly)
- [ ] Comparison of buy-and-hold vs. rebalanced returns

### Data & Coverage
- [ ] Mutual fund NAV support (via AMFI or MFApi)
- [ ] Auto-refresh of NSE master CSVs
- [ ] Scheduled price history updates

### Reporting
- [ ] Automated portfolio snapshot report (PDF/HTML)
- [ ] Interactive Plotly dashboard for portfolio drill-down

## Tech Stack

- **Python** — pandas, numpy, scipy, yfinance, cvxpy
- **Visualisation** — matplotlib, seaborn
- **Notebooks** — Jupyter
- **Code Quality** — pre-commit hooks (Black)
