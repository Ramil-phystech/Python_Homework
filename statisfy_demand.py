import numpy as np


class ShapeMismatchError(BaseException):
    pass


def can_satisfy_demand(
        costs: np.ndarray,
        resource_amounts: np.ndarray,
        demand_expected: np.ndarray,
) -> bool:
    if len(demand_expected) != costs.shape[1] or len(resource_amounts) != costs.shape[0]:
        raise ShapeMismatchError()

    return not np.any(resource_amounts - (np.sum(demand_expected * costs, axis=1)) < 0)
