import time
from typing import Callable, TypeVar
from functools import wraps

T = TypeVar("T")


def collect_statistic(statistics: dict[str, list[float, int]]) -> Callable[[T], T]:
    def _collect_statistic(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            t1 = time.time()
            res = func(*args, **kwargs)
            t2 = time.time()

            name = func.__name__

            statistics[name] = statistics.get(name, [0, 0])

            new_count = statistics[name][1] + 1
            new_time = t2 - t1
            new_avg = (statistics[name][0] * statistics[name][1] + new_time) / new_count

            statistics[name] = [new_avg, new_count]

            return res

        return _wrapper

    return _collect_statistic
