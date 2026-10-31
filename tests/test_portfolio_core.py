import numpy as np
import pandas as pd
import pytest

from portfolio_optimizer.core import (
    annualized_mean_return,
    annualized_volatility,
    covariance_matrix,
    daily_returns,
    portfolio_return,
    portfolio_variance,
    portfolio_volatility,
    winsorize_returns,
)
from portfolio_optimizer import daily_returns as package_daily_returns
from utils.features import compute_daily_ret, compute_covariance_matrix
from utils.portfolio import portfolio_return as legacy_portfolio_return


def test_daily_returns_and_legacy_name_match():
    prices = pd.DataFrame({"AAA": [100.0, 110.0, 99.0]})

    expected = pd.DataFrame({"AAA": [0.1, -0.1]}, index=[1, 2])
    pd.testing.assert_frame_equal(daily_returns(prices), expected)
    pd.testing.assert_frame_equal(package_daily_returns(prices), expected)
    pd.testing.assert_frame_equal(compute_daily_ret(prices), expected)


def test_annualized_metrics_accept_configurable_period_frequency():
    returns = pd.DataFrame({"AAA": [0.01, 0.03], "BBB": [0.02, 0.02]})

    pd.testing.assert_series_equal(
        annualized_mean_return(returns, periods_per_year=12),
        returns.mean() * 12,
    )
    pd.testing.assert_series_equal(
        annualized_volatility(returns, periods_per_year=12),
        returns.std() * np.sqrt(12),
    )
    pd.testing.assert_frame_equal(
        covariance_matrix(returns, periods_per_year=12), returns.cov() * 12
    )
    pd.testing.assert_frame_equal(
        compute_covariance_matrix(returns, periods_per_year=12), returns.cov() * 12
    )


def test_annualization_rejects_nonpositive_frequency():
    with pytest.raises(ValueError, match="positive integer"):
        annualized_mean_return(pd.DataFrame({"AAA": [0.01]}), periods_per_year=0)


def test_winsorization_uses_k_and_leaves_zero_mad_series_unchanged():
    returns = pd.DataFrame({"variable": [0.0, 0.01, -0.01, 0.02, -0.02, 0.9]})
    constant = pd.DataFrame({"constant": [0.0, 0.0, 0.0, 1.0]})

    clipped = winsorize_returns(returns, k=1)
    median = returns["variable"].median()
    mad = (returns["variable"] - median).abs().median()
    expected_upper = median + 1.4826 * mad

    assert clipped["variable"].max() == pytest.approx(expected_upper)
    assert winsorize_returns(returns, k=2)["variable"].max() > expected_upper
    pd.testing.assert_frame_equal(winsorize_returns(constant), constant)


def test_portfolio_metrics_and_legacy_api_match():
    weights = np.array([0.6, 0.4])
    expected_returns = np.array([0.08, 0.04])
    covariance = np.array([[0.04, 0.01], [0.01, 0.02]])

    assert portfolio_return(weights, expected_returns) == pytest.approx(0.064)
    assert legacy_portfolio_return(weights, expected_returns) == pytest.approx(0.064)
    assert portfolio_variance(weights, covariance) == pytest.approx(0.0224)
    assert portfolio_volatility(weights, covariance) == pytest.approx(np.sqrt(0.0224))


def test_portfolio_metrics_reject_mismatched_shapes():
    with pytest.raises(ValueError, match="match the weights"):
        portfolio_variance([0.5, 0.5], [[0.1]])
    with pytest.raises(ValueError, match="matching shapes"):
        portfolio_return([0.5, 0.5], [0.1])
