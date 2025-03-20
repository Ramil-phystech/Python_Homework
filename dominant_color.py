import numpy as np


class ShapeMismatchError(BaseException):
    pass


def get_dominant_color_info(
        image: np.ndarray[np.uint8],
        threshold: int = 5,
) -> tuple[np.uint8, float]:
    if threshold < 1:
        raise ValueError

    unique_colors = np.unique(image)

    mask = np.abs(image[:, :, np.newaxis] - unique_colors) <= threshold
    counts = np.sum(mask, axis=(0, 1))
    index = np.argmax(counts)
    color = unique_colors[index]

    percent = (counts[index] / image.size) * 100

    return np.uint8(color), float(percent)
