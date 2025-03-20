import numpy as np


class ShapeMismatchError(BaseException):
    pass


def pad_image(image: np.ndarray, pad_size: int) -> np.ndarray:
    if pad_size < 1:
        raise ValueError

    if len(image.shape) == 2:
        width, height = image.shape
        padded_image = np.zeros((width + 2 * pad_size, height + 2 * pad_size))
        padded_image[pad_size:(pad_size + width), pad_size:(pad_size + height)] = image
    else:
        width, height, depth = image.shape
        padded_image = np.zeros((width + 2 * pad_size, height + 2 * pad_size, depth))
        padded_image[pad_size:(pad_size + width), pad_size:(pad_size + height), :] = image

    return padded_image


def blur_image(
        image: np.ndarray,
        kernel_size: int,
) -> np.ndarray:
    if kernel_size < 1 or kernel_size % 2 == 0:
        raise ValueError

    blured_image = np.zeros(shape=image.shape)
    padding_width = kernel_size // 2
    padded_image = pad_image(image, padding_width)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if len(image.shape) == 2:
                window = padded_image[i: i + kernel_size, j: j + kernel_size]
                blured_image[i, j] = np.mean(window)
            else:
                window = padded_image[i: i + kernel_size, j: j + kernel_size, :]
                blured_image[i, j, :] = np.mean(window, axis=(0, 1))

    return blured_image.astype(image.dtype)
