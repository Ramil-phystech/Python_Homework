from typing import Callable


def is_floats_eq(lhs: float, rhs: float, eps: float = 1e-6) -> bool:
    return abs(lhs - rhs) < eps


def make_averager(accumulation_period: int) -> Callable[[float], float]:
    profits = [0] * (accumulation_period + 1)
    s = c = 0

    def get_avg(profit: int) -> float:
        nonlocal profits, s, c
        c += 1
        if c > accumulation_period:
            s += profit - profits[c % accumulation_period]
            profits[c % accumulation_period] = profit

            return s / accumulation_period

        else:
            s += profit
            profits[c % accumulation_period] = profit

            return s / c

    return get_avg
