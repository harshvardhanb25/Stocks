import numpy as np
import pandas as pd
import pytest

from portfolio_optimizer.data import (
    convert_dates,
    normalize_column_headers,
    strip_string_values,
    to_snake_case,
    validate_price_history,
)
from portfolio_optimizer.models import Holding, Portfolio
from utils.preprocessing import fill_with_proxy


def test_generic_cleaning_helpers_and_legacy_exports():
    frame = pd.DataFrame({"Asset Name": ["  Example Corp  "]})

    assert to_snake_case("Asset Name") == "asset_name"
    normalize_column_headers(frame)
    strip_string_values(frame)

    assert frame.columns.tolist() == ["asset_name"]
    assert frame.loc[0, "asset_name"] == "Example Corp"


def test_convert_dates_supports_existing_source_formats_and_reports_bad_values():
    frame = pd.DataFrame({"date": ["01-Jan-24", "02-January-2024", "03 Jan 2024"]})

    converted = convert_dates(frame, "date")

    assert converted["date"].tolist() == [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-01-02"),
        pd.Timestamp("2024-01-03"),
    ]
    with pytest.raises(ValueError, match="Could not parse"):
        convert_dates(pd.DataFrame({"date": ["not a date"]}), "date")


def test_validate_price_history_sorts_dates_and_selects_requested_order():
    dates = pd.to_datetime(["2024-01-02", "2024-01-01"])
    prices = pd.DataFrame({"AAA": [11.0, 10.0], "BBB": [20.0, np.nan]}, index=dates)

    validated = validate_price_history(prices, tickers=["BBB", "AAA"])

    assert validated.index.is_monotonic_increasing
    assert validated.columns.tolist() == ["BBB", "AAA"]
    assert pd.isna(validated.loc[pd.Timestamp("2024-01-01"), "BBB"])


@pytest.mark.parametrize(
    "values, message",
    [
        ([100.0, 0.0], "must be positive"),
        ([100.0, np.inf], "infinite"),
    ],
)
def test_validate_price_history_rejects_invalid_observations(values, message):
    prices = pd.DataFrame({"AAA": values}, index=pd.date_range("2024-01-01", periods=2))

    with pytest.raises(ValueError, match=message):
        validate_price_history(prices)


def test_validate_price_history_rejects_bad_ticker_requests():
    prices = pd.DataFrame(
        {"AAA": [100.0]}, index=pd.date_range("2024-01-01", periods=1)
    )

    with pytest.raises(ValueError, match="at least one ticker"):
        validate_price_history(prices, tickers=[])
    with pytest.raises(ValueError, match="unique"):
        validate_price_history(prices, tickers=["AAA", "AAA"])
    with pytest.raises(ValueError, match="missing ticker"):
        validate_price_history(prices, tickers=["BBB"])


def test_holding_and_portfolio_validate_user_input():
    portfolio = Portfolio([Holding("  EXAMPLE  ", 3), Holding("OTHER", -1.5)])

    assert portfolio.tickers == ("EXAMPLE", "OTHER")
    assert portfolio.holdings[0].quantity == 3.0
    with pytest.raises(ValueError, match="unique"):
        Portfolio([Holding("ABC", 1), Holding(" abc ", 2)])
    with pytest.raises(ValueError, match="finite non-zero"):
        Holding("ABC", 0)


def test_legacy_proxy_helper_delegates_to_generic_core():
    dates = pd.date_range("2024-01-01", periods=3)
    returns = pd.DataFrame({"NEW": [np.nan, 0.02, 0.03]}, index=dates)
    proxies = pd.DataFrame({"INDEX": [0.01, 0.015, 0.02]}, index=dates)

    filled = fill_with_proxy(returns, proxies, {"NEW": "INDEX"})

    assert filled["NEW"].tolist() == [0.01, 0.02, 0.03]
    assert pd.isna(returns.loc[dates[0], "NEW"])
