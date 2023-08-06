import logging
import numpy as np
import numpy.typing as npt
from typing import List
from MainAccesslib.equalization.algorithm.disc_precision import get_otp_dac_pos, step3
from MainAccesslib.equalization.ndarray_operation import range_split_DISC

N_PIXELS = 160
logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]
NDArrayInt32 = npt.NDArray[np.int32]
NDArrayBool = npt.NDArray[np.bool_]


def equalize(char_data: NDArrayUint32, char_dac: NDArrayUint32, min_threshold: int, pct_high: int, pct_low: int,
             factor_std_noise: int) -> (NDArrayInt32, NDArrayBool, NDArrayBool):
    """
    Equalize disc characterization scan using data saved on disk
    :param char_data: NDArray containing DISC data, expected format: [DISC][ACQ_DATA][N_CHIPS][PIXELS]
    :param char_dac: NDArray containing DAC values, expected format: [DAC_VALUE][N_CHIP]
    :param min_threshold: If the counts acquired are under this threshold will be masked
    :param pct_high: If the close DISC gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close DISC gain is lower than the pct + opt_gain, mask this pixel
    :param factor_std_noise:
    :return: Ifeed matrix, range matrix, masked pixel matrix
    """
    """ Getting necessary data """
    char_data = char_data.transpose((2, 0, 3, 1))  # [N_CHIPS][DISC][PIXELS][ACQ_DATA]
    char_dac = char_dac.T  # [N_CHIPS][DAC_VALUES]

    """ Determine optimum threshold position """
    opt_threshold_pos_arr: List[np.uint32] = []
    for chip in range(len(char_data)):
        """ Get optimum """
        opt_data = get_otp_dac_pos(char_data[chip], min_threshold, pct_high, pct_low, N_PIXELS)
        opt_threshold_pos_arr.append(opt_data)

    mask = np.array(opt_threshold_pos_arr) < 10
    opt_dac_pos_arr = np.where(mask, np.nan, opt_threshold_pos_arr)
    try:
        opt_dac_pos_val = int(np.nanmean(opt_dac_pos_arr))
    except ValueError:
        opt_dac_pos_val = 0
    logger.info(f"Optimum threshold position array: {opt_threshold_pos_arr}")
    logger.info(f"Optimum threshold mean value: {opt_dac_pos_val}")

    """ Start equalization loop """
    pixel_disc_matrix: List[NDArrayInt32] = []
    pixel_disc_range_matrix: List[NDArrayInt32] = []
    masked_pixel_matrix: List[NDArrayInt32] = []

    for chip in range(len(char_data)):
        """ Equalization for each chip """
        try:
            pixel_disc_data = step3(char_data[chip], char_dac[chip], min_threshold, factor_std_noise, opt_dac_pos_val)
        except IndexError:
            logger.error(f"Wer are expecting on dac_data this shape [{len(char_data)}][N_DAC_VALUES], instead we"
                         f" get {char_dac.shape}")
            raise IndexError
        pixel_ifeed, pixel_ifeed_range, masked_pixel = range_split_DISC(pixel_disc_data)
        pixel_disc_matrix.append(pixel_ifeed.reshape((8, 20)))
        pixel_disc_range_matrix.append(pixel_ifeed_range.reshape((8, 20)))
        masked_pixel_matrix.append(masked_pixel.reshape((8, 20)))

    return np.int32(pixel_disc_matrix), np.bool_(pixel_disc_range_matrix), np.bool_(masked_pixel_matrix)
