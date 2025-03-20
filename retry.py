from typing import Callable, TypeVar
from functools import wraps
import time

T = TypeVar("T")


def retry(retries: int = 3, timeout: float = 1) -> Callable[[T], T]:
    def _retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception:
                    if i == retries - 1:
                        raise Exception
                    time.sleep(timeout)

        return wrapper

    return _retry
