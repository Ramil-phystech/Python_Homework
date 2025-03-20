from calendar import month_name
import numpy as np


class ShapeMismatchError(BaseException):
    pass


class InconsistentDataError(BaseException):
    pass


def get_most_profitable_month_name(
        amounts_of_sold_subscriptions: np.ndarray,
        subscriptions_prices: np.ndarray,
) -> str:
    if amounts_of_sold_subscriptions.shape[1] != len(subscriptions_prices):
        raise InconsistentDataError()

    return month_name[(np.argmax(np.sum(amounts_of_sold_subscriptions * subscriptions_prices, axis=1)) + 1)]


class Strategies(Enum):
    BY_GOOD = 'by_good'
    BY_MONTH = 'by_month'


def get_mean_profit(
        amounts_of_sold_subscriptions: np.ndarray,
        subscriptions_prices: np.ndarray,
        strategy: Strategies | None = None,
) -> np.ndarray | Real:
    if amounts_of_sold_subscriptions.shape[1] != len(subscriptions_prices):
        raise InconsistentDataError()

    if strategy is None:
        return np.mean(amounts_of_sold_subscriptions * subscriptions_prices)

    if strategy == Strategies.BY_MONTH:
        return np.mean(amounts_of_sold_subscriptions * subscriptions_prices, axis=1)

    return np.mean(amounts_of_sold_subscriptions * subscriptions_prices, axis=0)


def sort_month_names_by_profits(
        amounts_of_sold_subscriptions: np.ndarray,
        subscriptions_prices: np.ndarray,
        ascending: bool = True,
) -> list[str]:
    if amounts_of_sold_subscriptions.shape[1] != len(subscriptions_prices):
        raise InconsistentDataError()

    if ascending:
        rev = 1
    else:
        rev = -1

    profits_sorted = np.argsort(rev * np.sum(amounts_of_sold_subscriptions * subscriptions_prices, axis=1)) + 1

    return [month_name[i] for i in profits_sorted]
