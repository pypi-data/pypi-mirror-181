import logging
import numpy as np
import numpy.typing as npt
from typing import List
from MainAccesslib.equalization.algorithm.disc import step2
from MainAccesslib.equalization.ndarray_operation import range_split_DISC

logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]
NDArrayInt32 = npt.NDArray[np.int32]
NDArrayBool = npt.NDArray[np.bool_]


def equalize(char_data: NDArrayUint32, char_dac: NDArrayUint32, min_threshold: int, pct_high: int, pct_low: int,
             factor_std_noise: int) -> (NDArrayInt32, NDArrayBool, NDArrayBool, np.uint32):
    """
    Equalize disc characterization scan using data saved on disk
    :param char_data: NDArray containing DISC data, expected format: [DISC][ACQ_DATA][N_CHIPS][PIXELS]
    :param char_dac: NDArray containing DAC values, expected format: [DAC_VALUE][N_CHIP]
    :param min_threshold: If the counts acquired are under this threshold will be masked
    :param pct_high: If the close DISC gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close DISC gain is lower than the pct + opt_gain, mask this pixel
    :param factor_std_noise:
    :return: Ifeed matrix, range matrix, masked pixel matrix, chips analyzed list
    """
    """ Getting necessary data """
    char_data = char_data.transpose((2, 0, 3, 1))  # [N_CHIPS][DISC][PIXELS][ACQ_DATA]
    char_dac = char_dac.T[0]  # [DAC_VALUE]

    """ Start equalization loop """
    pixel_disc_matrix: List[NDArrayInt32] = []
    pixel_disc_range_matrix: List[NDArrayInt32] = []
    masked_pixel_matrix: List[NDArrayInt32] = []
    opt_dac_matrix: List[np.uint32] = []

    for chip in range(len(char_data)):
        """ Equalization for each chip """
        pixel_disc_data, opt_dac = step2(char_data[chip], char_dac, min_threshold, pct_high, pct_low, factor_std_noise)
        pixel_ifeed, pixel_ifeed_range, masked_pixel = range_split_DISC(pixel_disc_data)
        pixel_disc_matrix.append(pixel_ifeed.reshape((8, 20)))
        pixel_disc_range_matrix.append(pixel_ifeed_range.reshape((8, 20)))
        masked_pixel_matrix.append(masked_pixel.reshape((8, 20)))
        opt_dac_matrix.append(opt_dac)

    return np.int32(pixel_disc_matrix), np.bool_(pixel_disc_range_matrix), np.bool_(masked_pixel_matrix), np.uint32(
        opt_dac_matrix)
