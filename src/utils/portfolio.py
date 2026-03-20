from __future__ import annotations

import numpy as np
import numpy.typing as npt

ArrayFloat = npt.NDArray[np.float64]


def portfolio_variance(w: ArrayFloat, covariance_matrix: ArrayFloat) -> float:
    # Use float() to ensure we return a plain Python float (not numpy scalar)
    return float(w.T @ covariance_matrix @ w)


def portfolio_volatility(w: ArrayFloat, covariance_matrix: ArrayFloat) -> float:
    return float(np.sqrt(portfolio_variance(w=w, covariance_matrix=covariance_matrix)))


def portfolio_return(w: ArrayFloat, mu: ArrayFloat) -> float:
    return float(w.T @ mu)
