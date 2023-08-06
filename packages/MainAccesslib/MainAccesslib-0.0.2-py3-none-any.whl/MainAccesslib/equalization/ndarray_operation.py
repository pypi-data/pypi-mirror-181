import numpy as np
import numpy.typing as npt

# Typing
NDArrayInt32 = npt.NDArray[np.int32]


def range_split_IFEED(pixel_ifeed_data: NDArrayInt32) -> (NDArrayInt32, NDArrayInt32, NDArrayInt32):
    # 0 a 22
    # 0 a 14 -> +1 -> 1 a 15 => IFEEDRANGE = False
    # 15 a 22 --> -7 --> 8 a 15 => IFEEDRANGE = True
    range_ = np.logical_and(pixel_ifeed_data >= 15, pixel_ifeed_data != -1)
    range2_ = np.logical_and(pixel_ifeed_data < 15, pixel_ifeed_data != -1)
    masked = pixel_ifeed_data == - 1
    pixel_ifeed_data = np.where(masked, 15, pixel_ifeed_data)
    pixel_ifeed_data = np.where(range2_, pixel_ifeed_data + 1, pixel_ifeed_data)
    pixel_ifeed_data = np.where(range_, pixel_ifeed_data - 7, pixel_ifeed_data)
    return pixel_ifeed_data, range_, masked


def range_split_DISC(pixel_disc_data: NDArrayInt32) -> (NDArrayInt32, NDArrayInt32, NDArrayInt32):
    range_ = np.logical_and(pixel_disc_data >= 16, pixel_disc_data != -1)
    range2_ = np.logical_and(pixel_disc_data <= 15, pixel_disc_data != -1)
    masked = pixel_disc_data == - 1
    pixel_disc_data = np.where(masked, 0, pixel_disc_data)
    pixel_disc_data = np.where(range2_, pixel_disc_data, pixel_disc_data)
    pixel_disc_data = np.where(range_, 31 - pixel_disc_data, pixel_disc_data)
    return pixel_disc_data, range_, masked
