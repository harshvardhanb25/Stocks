"""Compatibility exports for the original NSE and broker workflows."""

from portfolio_optimizer.core.returns import fill_with_proxy
from portfolio_optimizer.data.cleaning import (
    convert_dates,
    normalize_column_headers,
    strip_string_values,
    to_snake_case,
)

__all__ = [
    "convert_dates",
    "fill_with_proxy",
    "normalize_column_headers",
    "strip_string_values",
    "to_snake_case",
]
