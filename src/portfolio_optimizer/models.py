from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Sequence


@dataclass(frozen=True)
class Holding:
    """A ticker and quantity supplied by the user."""

    ticker: str
    quantity: float

    def __post_init__(self) -> None:
        if not isinstance(self.ticker, str) or not self.ticker.strip():
            raise ValueError("ticker must be a non-empty string")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, Real):
            raise ValueError("quantity must be a finite non-zero number")

        quantity = float(self.quantity)
        if not math.isfinite(quantity) or quantity == 0:
            raise ValueError("quantity must be a finite non-zero number")

        object.__setattr__(self, "ticker", self.ticker.strip())
        object.__setattr__(self, "quantity", quantity)


@dataclass(frozen=True)
class Portfolio:
    """A collection of user-supplied holdings with unique tickers."""

    holdings: Sequence[Holding]

    def __post_init__(self) -> None:
        holdings = tuple(self.holdings)
        if not holdings:
            raise ValueError("portfolio must contain at least one holding")
        if not all(isinstance(holding, Holding) for holding in holdings):
            raise TypeError("all portfolio entries must be Holding instances")

        tickers = [holding.ticker.casefold() for holding in holdings]
        if len(tickers) != len(set(tickers)):
            raise ValueError("portfolio tickers must be unique")

        object.__setattr__(self, "holdings", holdings)

    @property
    def tickers(self) -> tuple[str, ...]:
        return tuple(holding.ticker for holding in self.holdings)
