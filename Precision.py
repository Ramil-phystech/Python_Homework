from decimal import Decimal, getcontext
from types import TracebackType
from typing import Optional


class Precision:
    _MIN_LIMIT: int = 1
    _prev_precision: Optional[int]

    def __init__(self, precision: int) -> None:
        try:
            self.precision = int(round(precision))
        except TypeError:
            raise TypeError(f"the type <{type(precision)}> "
                            f"cannot be converted to an integer")

        if self.precision < self._MIN_LIMIT:
            raise ValueError("precision must be natural number")

        self._prev_precision = None

    def __enter__(self):
        self._prev_precision = getcontext().prec
        getcontext().prec = self.precision

    def __exit__(self, exc_type, exc_val, exc_tb):
        getcontext().prec = self._prev_precision
