# Stocks

A personal quantitative finance toolkit for analysing and optimising an Indian equity portfolio. Built around NSE data and the `yfinance` API, the project handles everything from raw data ingestion and cleaning through return computation, outlier treatment, and index benchmark construction with portfolio optimisation on the roadmap.

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
│   ├── config.py                     # Centralised path config (raw & processed dirs)
│   ├── scripts/
│   │   └── index_proxy.py            # Index benchmark builder (Nifty 500 / Next 50 / Smallcap 250)
│   └── utils/
│       ├── api_io.py                 # yfinance data fetching
│       ├── data_io_clean.py          # Raw data loaders & cleaners
│       ├── dataset_builder.py        # Canonical portfolio & price history builders
│       ├── features.py               # Return & volatility computations
│       ├── preprocessing.py          # General-purpose data cleaning helpers
│       └── universe.py               # Security universe management
├── .pre-commit-config.yaml
└── pyproject.toml
```

## What's Built So Far

### Data Ingestion & Cleaning (`data_io_clean.py`, `preprocessing.py`)
Loaders for four raw data sources — NSE equity master, NSE ETF master, SGB (Sovereign Gold Bond) price history, and a broker-exported portfolio CSV. Each loader normalises column headers to `snake_case`, strips whitespace, parses multiple date formats robustly, and standardises security type labels (`EQUITY STOCK` → `EQ`, etc.).

### API Layer (`api_io.py`)
Two `yfinance` wrappers for `.NS`-suffixed symbols:
- `fetch_current_prices` — fetches the latest closing price for a list of symbols using a 1-day download with threading.
- `fetch_historical_prices_n_years` — fetches `n` years of daily adjusted close history, forward-filling any gaps.

### Portfolio Builder (`dataset_builder.py`)
- `build_canonical_portfolio` — merges the broker portfolio with the NSE master data on ISIN, attaches live prices via `fetch_current_prices`, handles SGB separately (yfinance has no support), and outputs a single standardised dataframe with columns: `isin`, `symbol`, `security_type`, `sector`, `quantity`, `fetched_price`, `current_value`, and `weight`.
- `build_historical_price_dataset` — joins the yfinance equity/ETF price history with the SGB CSV history into one aligned time-series dataframe.

### Feature Engineering (`features.py`)
- Daily percentage returns (`compute_daily_ret`)
- Annualised mean return (`compute_annualized_mean_ret`, ×252)
- Annualised volatility (×√252)
- MAD-based winsorization (`winsorize_returns`) — clips extreme outliers beyond a configurable `k` robust-sigma threshold (default 8) per security independently, preserving genuine data while removing artefacts.

### Universe Management (`universe.py`)
- `remove_securities` — drops one or more symbols from both the canonical portfolio dataframe and the returns dataframe simultaneously, keeping them in sync. Accepts a single symbol string or a list.
- `remove_securities_leq_weight_w` — convenience wrapper that automatically identifies and removes all securities whose portfolio weight is at or below a threshold `w` (default 0.5%), useful for trimming negligible positions before optimisation.

### Index Benchmark Builder (`scripts/index_proxy.py`)
Processes historical total-return CSV files for three NSE indices — **Nifty 500**, **Nifty Next 50**, and **Nifty Smallcap 250** — downloaded from NSE India. For each index, the script:
- Globs all matching raw CSV files and concatenates them.
- Normalises headers, strips whitespace, and parses dates (with debug logging for failed parses).
- Deduplicates and sorts by date, then writes a clean, date-indexed CSV to `data/processed/`.

These cleaned index series serve as benchmarks for performance attribution and beta calculations.

### Configuration (`config.py`)
Centralised path resolution for all raw **and processed** data files relative to the project root, so nothing is hardcoded in notebooks or scripts. Exposes `RAW_DATA_DIR` and `PROCESSED_DATA_DIR`.

## Data Sources

| File | Location | Description |
|---|---|---|
| `nse_eq_master.csv` | `data/raw/` | NSE equity master list (ISIN, symbol, listing date) |
| `nse_etf_master.csv` | `data/raw/` | NSE ETF master list |
| `SGBMAY28.csv` | `data/raw/` | Sovereign Gold Bond (May 2028) price history |
| `current_portfolio.csv` | `data/raw/` | Broker-exported portfolio holdings |
| `NIFTY 500_Historical_TR_*.csv` | `data/raw/` | Nifty 500 total-return index history |
| `NIFTY NEXT 50_Historical_TR_*.csv` | `data/raw/` | Nifty Next 50 total-return index history |
| `NIFTY SMALLCAP 250_Historical_TR_*.csv` | `data/raw/` | Nifty Smallcap 250 total-return index history |
| `NIFTY500.csv`, `NEXT50.csv`, `SMALLCAP250.csv` | `data/processed/` | Cleaned, deduplicated index series |

> Raw data files are excluded from version control via `.gitignore`.

## Setup

```bash
# Install dependencies (requires Python 3.11+)
pip install -e .

# Install pre-commit hooks
pre-commit install
```

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

- **Python** — pandas, numpy, yfinance
- **Notebooks** — Jupyter
- **Code Quality** — pre-commit hooks (ruff / black)
