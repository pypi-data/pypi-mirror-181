import logging
import numpy as np
import numpy.typing as npt
from typing import List
from MainAccesslib.equalization.algorithm.ifeed import step1, get_opt_gain
from MainAccesslib.equalization.ndarray_operation import range_split_IFEED

logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]
NDArrayInt32 = npt.NDArray[np.int32]
NDArrayBool = npt.NDArray[np.bool_]


def equalize(char_data: NDArrayUint32, char_dac: NDArrayUint32, min_threshold: int, pct_high: int,
             pct_low: int) -> (NDArrayInt32, NDArrayBool, NDArrayBool):
    """
    Equalize ifeed characterization scan using data saved on disk
    :param char_data: NDArray containing IFEED data, expected format: [IFEED][ACQ_DATA][N_CHIPS][PIXELS]
    :param char_dac: NDArray containing DAC values, expected format: [DAC_VALUE][N_CHIP]
    :param min_threshold: If the counts acquired are under this threshold will be masked
    :param pct_high: If the close IFEED gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close IFEED gain is lower than the pct + opt_gain, mask this pixel
    :return: Ifeed matrix, range matrix, masked pixel matrix, chips analyzed list
    """
    """ Getting necessary data """
    char_data = char_data.transpose((2, 0, 3, 1))   # [N_CHIPS][IFEED][PIXELS][ACQ_DATA]
    char_dac = char_dac.T[0]  # [DAC_VALUE]

    """ Start determine optimum gain process """
    opt_gain: List[np.uint32] = []

    for chip in range(len(char_data)):
        """Appending opt gain of each chip"""
        opt_gain.append(get_opt_gain(char_data[chip], char_dac, min_threshold))

    """ For all the chips determine which is the optimum gain"""
    logger.info(f"Optimum gain for each chip: {opt_gain}")
    arr = np.array(opt_gain)
    # If optimum gain in any chip is lower than 100 counts, change value to 'np.nan'
    arr = np.where(arr > 100, arr, np.nan)
    opt_gain: np.uint32 = np.nanmean(arr)
    logger.info(f"Optimum gain for all teh chips: {opt_gain}")

    """ Start equalization loop """
    pixel_ifeed_matrix: List[NDArrayInt32] = []
    pixel_ifeed_range_matrix: List[NDArrayInt32] = []
    masked_pixel_matrix: List[NDArrayInt32] = []

    for chip in range(len(char_data)):
        """ Equalization for each chip """
        pixel_ifeed_data = step1(char_data[chip], char_dac, min_threshold, pct_high, pct_low, opt_gain=opt_gain)
        pixel_ifeed, pixel_ifeed_range, masked_pixel = range_split_IFEED(pixel_ifeed_data)
        pixel_ifeed_matrix.append(pixel_ifeed.reshape((8, 20)))
        pixel_ifeed_range_matrix.append(pixel_ifeed_range.reshape((8, 20)))
        masked_pixel_matrix.append(masked_pixel.reshape((8, 20)))

    return np.int32(pixel_ifeed_matrix), np.bool_(pixel_ifeed_range_matrix), np.bool_(
        masked_pixel_matrix)
