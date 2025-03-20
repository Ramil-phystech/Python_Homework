import numpy as np


class ShapeMismatchError(BaseException):
    pass


def adaptive_filter(
        Vs: np.ndarray,
        Vj: np.ndarray,
        diag_A: np.ndarray
) -> np.ndarray:
    if Vs.shape[0] != Vj.shape[0] or Vj.shape[1] != diag_A.shape[0] or diag_A.ndim != 1:
        raise ShapeMismatchError()

    Vj_H = np.conj(Vj).T
    s = Vj_H @ Vj @ np.diag(diag_A)
    return Vs - Vj @ np.linalg.inv(np.eye(s.shape[0]) + s) @ (Vj_H @ Vs)
