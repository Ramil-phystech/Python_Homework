import numpy as np


class ShapeMismatchError(BaseException):
    pass


def get_projections_components(
        matrix: np.ndarray,
        vector: np.ndarray,
) -> tuple[np.ndarray | None, np.ndarray | None]:
    if matrix.shape[0] != matrix.shape[1] or matrix.shape[1] != len(vector):
        raise ShapeMismatchError()

    if np.linalg.det(matrix) == 0:
        return None, None

    projections = (matrix.T * np.sum(matrix * vector, axis=1) / np.square(np.linalg.norm(matrix, axis=1))).T
    orthogonals = np.subtract(vector, projections)

    return projections, orthogonals
