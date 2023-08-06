import logging
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
# Typing
NDArrayInt32 = npt.NDArray[np.int32]


def step2(char_data: NDArrayInt32, char_values: NDArrayInt32, min_threshold: int, pct_high: int, pct_low: int,
          factor_std_optimum: int, n_pixels: int = 160) -> (NDArrayInt32, np.uint32):
    """
    Finds optimum discriminator value for each pixel based upon the counts chart
    :param char_data: Matrix containing characterization data with all parameters in the following ranges: [DISC][PIXELS][DAC_VALUES]
    :param char_values: Array containing DAC positions from the DACs characterization discriminator in each pixel
    :param min_threshold: Minimum value of counts above noise level
    :param pct_high: If the close DISC gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close DISC gain is lower than the pct + opt_gain, mask this pixel
    :param n_pixels: Number of pixels in the system
    :param factor_std_optimum: To control high and low cut on data bell
    :return: NDArray containing the optimum values of discriminator for each pixel [PIX]
    """

    container = np.empty((len(char_data), n_pixels))
    noise_width_analysis = np.zeros(n_pixels)

    if not char_data.any():
        logger.warning("Characterization data is empty, check 'char_data' input matrix.")
        return np.full(n_pixels, -1, dtype=np.int32), np.uint32(0)

    c: int = 0
    for DISC in range(len(char_data)):
        for pix in range(len(char_data[0])):
            mask = char_data[DISC][pix][0:] >= min_threshold
            if not np.all(mask is False):
                try:
                    min_pos = np.argmax(char_data[DISC][pix] > min_threshold)
                    relative_max_pos = np.argmax(np.flip(char_data[DISC][pix]) > min_threshold)
                    max_pos = len(char_data[DISC][pix]) - relative_max_pos
                    container[DISC][pix] = ((char_values[max_pos] - char_values[min_pos]) / 2) + char_values[min_pos]

                    # Noise width analysis
                    if DISC == 15:
                        c += 1
                        noise_width_analysis[pix] = (max_pos - min_pos)

                except (ValueError, IndexError):
                    container[DISC][pix] = -1
                    c += 1
            else:
                container[DISC][pix] = -1

    # Determining the optimum dac position
    arr = np.array(container[15])
    arr = arr[arr != -1]
    median = np.median(arr)
    data_cut_high = median + pct_high
    data_cut_low = median - pct_low
    mask = np.logical_or(arr >= data_cut_high, arr <= data_cut_low)
    arr = np.where(mask, np.nan, arr)
    opt_dac = np.nanmean(arr)

    # Mask pixels with noise with outliers
    arr = np.array(noise_width_analysis)
    median = np.median(arr)
    data_cut_high = median + factor_std_optimum
    mask_pixels = arr >= data_cut_high

    # Check for each value the best DISC value in each pixel.
    container_tp = container.transpose((1, 0))  # [pix][DISC].
    opt_disc_val = np.empty((n_pixels,))  # Pixel DISC optimum empty array.

    for pix in range(len(container_tp)):
        if opt_dac < container_tp[pix][0] \
                or opt_dac > container_tp[pix][len(container_tp[0]) - 1]:
            opt_disc_val[pix] = -1
        else:
            opt_disc_val[pix] = (np.abs(container_tp[pix] - opt_dac)).argmin()

    # Mask pixels noise out of distribution
    opt_disc_val = np.where(mask_pixels, -1, opt_disc_val)

    return np.int32(opt_disc_val), np.uint32(opt_dac)
