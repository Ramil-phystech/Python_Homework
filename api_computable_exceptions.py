from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def api_computable_exceptions(
        exception_mapping: dict[type[Exception], type[Exception]]
) -> Callable[[T], T]:
    def comp_exc(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)

                return res

            except Exception as exc:
                if type(exc) in exception_mapping:
                    raise exception_mapping[type(exc)]() from None

                raise

        return wrapper

    return comp_exc
