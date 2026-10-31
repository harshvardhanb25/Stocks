import numpy as np
import numpy.typing as npt


def portfolio_variance(weights: npt.ArrayLike, covariance: npt.ArrayLike) -> float:
    """Calculate portfolio variance from weights and a covariance matrix."""
    weight_array = np.asarray(weights, dtype=float)
    covariance_array = np.asarray(covariance, dtype=float)
    if weight_array.ndim != 1:
        raise ValueError("weights must be one-dimensional")
    if covariance_array.shape != (weight_array.size, weight_array.size):
        raise ValueError("covariance must be square and match the weights")
    return float(weight_array.T @ covariance_array @ weight_array)


def portfolio_volatility(weights: npt.ArrayLike, covariance: npt.ArrayLike) -> float:
    """Calculate portfolio volatility from weights and covariance."""
    return float(np.sqrt(portfolio_variance(weights, covariance)))


def portfolio_return(weights: npt.ArrayLike, expected_returns: npt.ArrayLike) -> float:
    """Calculate weighted portfolio return from asset returns."""
    weight_array = np.asarray(weights, dtype=float)
    return_array = np.asarray(expected_returns, dtype=float)
    if weight_array.ndim != 1 or return_array.ndim != 1:
        raise ValueError("weights and expected_returns must be one-dimensional")
    if weight_array.shape != return_array.shape:
        raise ValueError("weights and expected_returns must have matching shapes")
    return float(weight_array.T @ return_array)
