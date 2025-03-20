import numpy as np


class ShapeMismatchError(BaseException):
    pass


def convert_from_sphere(
        distances: np.ndarray,
        azimuth: np.ndarray,
        inclination: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not (len(distances) == len(azimuth) == len(inclination)):
        raise ShapeMismatchError()

    x = distances * np.sin(inclination) * np.cos(azimuth)
    y = distances * np.sin(inclination) * np.sin(azimuth)
    z = distances * np.cos(inclination)

    return x, y, z


def convert_to_sphere(
        abscissa: np.ndarray,
        ordinates: np.ndarray,
        applicates: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not (len(abscissa) == len(ordinates) == len(applicates)):
        raise ShapeMismatchError()

    distances = np.sqrt(abscissa ** 2 + ordinates ** 2 + applicates ** 2)
    azimuth = np.arctan2(ordinates, abscissa)
    inclination = np.arccos(applicates / distances)

    return distances, azimuth, inclination
