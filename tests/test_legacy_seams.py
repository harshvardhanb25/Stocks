import importlib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import requests

from portfolio_optimizer import config as package_config
from utils.api_io import fetch_historical_prices_n_years
from utils.api_io import fetch_current_prices
from utils.dataset_builder import build_index_prices
from utils.preprocessing import fill_with_proxy
from utils.universe import remove_securities_leq_weight_w


def test_package_star_import_resolves_every_declared_export():
    namespace = {}
    exec("from portfolio_optimizer import *", namespace)

    assert "fill_with_proxy" in namespace


def test_legacy_proxy_argument_names_are_supported():
    dates = pd.date_range("2024-01-01", periods=2)
    returns = pd.DataFrame({"NEW": [np.nan, 0.02]}, index=dates)
    proxies = pd.DataFrame({"INDEX": [0.01, 0.015]}, index=dates)

    result = fill_with_proxy(
        ret=returns,
        proxy_rets=proxies,
        proxy_map={"NEW": "INDEX"},
    )

    assert result.loc[dates[0], "NEW"] == pytest.approx(0.01)


def test_build_index_prices_reads_lowercase_date_column(tmp_path):
    csv_path = tmp_path / "benchmark.csv"
    pd.DataFrame({"date": ["2024-01-01", "2024-01-02"], "TRI": [100.0, 101.0]}).to_csv(
        csv_path, index=False
    )

    result = build_index_prices("Example Index", str(csv_path))

    assert result.index.tolist() == list(pd.to_datetime(["2024-01-01", "2024-01-02"]))
    assert result.name == "Example Index"


def test_remove_securities_leq_weight_uses_symbols_not_row_labels():
    portfolio = pd.DataFrame(
        {"symbol": ["AAA", "BBB"], "weight": [0.001, 0.999]},
        index=[10, 20],
    )
    returns = pd.DataFrame(
        {"AAA": [0.01], "BBB": [0.02]}, index=pd.date_range("2024-01-01", periods=1)
    )

    reduced_portfolio, reduced_returns = remove_securities_leq_weight_w(
        portfolio, returns, w=0.005
    )

    assert reduced_portfolio["symbol"].tolist() == ["BBB"]
    assert reduced_returns.columns.tolist() == ["BBB"]


def test_empty_historical_request_returns_empty_price_table():
    result = fetch_historical_prices_n_years(["NOT_A_SUPPORTED_SYMBOL"])

    assert result.empty
    assert len(result.columns) == 0
    assert isinstance(result.index, pd.DatetimeIndex)


def test_empty_current_price_request_keeps_current_price_schema():
    result = fetch_current_prices(["NOT_A_SUPPORTED_SYMBOL"])

    assert result.empty
    assert result.columns.tolist() == ["symbol", "fetched_price"]


def test_package_config_has_legacy_project_defaults():
    import config as legacy_config

    assert package_config.PROJECT_ROOT == Path.cwd()
    assert legacy_config.INDEX_MAP == package_config.INDEX_MAP
    assert legacy_config.PROCESSED_DATA_DIR == package_config.PROCESSED_DATA_DIR


def test_packaged_india_scripts_are_safe_to_import(monkeypatch):
    def reject_network(*args, **kwargs):
        raise AssertionError("Importing a script must not make network requests")

    monkeypatch.setattr(requests, "Session", reject_network)
    modules = [
        "portfolio_optimizer.adapters.india.fetch_tri_history",
        "portfolio_optimizer.adapters.india.index_proxy",
    ]

    for module_name in modules:
        module = importlib.import_module(module_name)
        assert callable(module.main)
