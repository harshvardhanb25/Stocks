from __future__ import annotations

import numpy as np
import numpy.typing as npt

from portfolio_optimizer.core.portfolio import (
    portfolio_return as _portfolio_return,
    portfolio_variance as _portfolio_variance,
    portfolio_volatility as _portfolio_volatility,
)

ArrayFloat = npt.NDArray[np.float64]


def portfolio_variance(w: ArrayFloat, covariance_matrix: ArrayFloat) -> float:
    return _portfolio_variance(weights=w, covariance=covariance_matrix)


def portfolio_volatility(w: ArrayFloat, covariance_matrix: ArrayFloat) -> float:
    return _portfolio_volatility(weights=w, covariance=covariance_matrix)


def portfolio_return(w: ArrayFloat, mu: ArrayFloat) -> float:
    return _portfolio_return(weights=w, expected_returns=mu)
