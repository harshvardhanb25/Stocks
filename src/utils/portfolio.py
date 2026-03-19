import numpy as np


def portfolio_variance(w: np.array, covariance_matrix: np.array) -> float:
    return w.T @ covariance_matrix @ w


def portfolio_volatility(w: np.array, covariance_matrix: np.array) -> float:
    return np.sqrt(portfolio_variance(w=w, covariance_matrix=covariance_matrix))


def portfolio_return(w: np.array, mu: np.array):
    return w.T @ mu
