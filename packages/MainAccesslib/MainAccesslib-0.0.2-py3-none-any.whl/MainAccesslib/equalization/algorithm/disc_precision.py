import logging
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
# Typing
NDArrayInt32 = npt.NDArray[np.int32]


def get_otp_dac_pos(char_data: NDArrayInt32, min_threshold: int, pct_high: int, pct_low: int,
                    n_pixels: int = 160) -> np.uint32:
    """
    Finds optimum value for disc 15 value
    :param char_data: Matrix containing characterization data with all parameters in the following ranges: [DISC][PIXELS][DAC_VALUES]
    :param min_threshold: Minimum value of counts above noise level
    :param pct_high: If the close DISC gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close DISC gain is lower than the pct + opt_gain, mask this pixel
    :param n_pixels: Number of pixels in the system
    :return: Optimum value on DISC 15
    """

    disc = 15
    char_data = np.array(char_data)
    container = np.empty((len(char_data), n_pixels))

    if not char_data.any():
        logger.warning("Characterization data is empty, check 'char_data' input matrix.")
        return np.uint32(0)

    else:
        for pix in range(len(char_data[0])):
            mask = char_data[disc][pix][0:] >= min_threshold
            if not np.all(mask is False):
                try:
                    relative_threshold_pos = np.argmax(np.flip(char_data[disc][pix]) > min_threshold)
                    threshold_pos = len(char_data[disc][pix]) - relative_threshold_pos
                    container[disc][pix] = threshold_pos

                except (ValueError, IndexError):
                    container[disc][pix] = -1
            else:
                container[disc][pix] = -1

        # Determining the optimum dac position
        arr = np.array(container[disc])
        arr = arr[arr != -1]
        median = np.median(arr)
        data_cut_high = median + pct_high
        data_cut_low = median - pct_low
        mask = np.logical_or(arr >= data_cut_high, arr <= data_cut_low)
        arr = np.where(mask, np.nan, arr)

        return np.uint32(np.nanmean(arr))


def step3(char_data: NDArrayInt32, char_values: NDArrayInt32, min_threshold: int, factor_std_optimum: int,
          opt_dac_pos: int, n_pixels: int = 160) -> NDArrayInt32:
    """
    Finds optimum discriminator value for each pixel based upon the counts chart
    :param char_data: Matrix containing characterization data with all parameters in the following ranges: [DISC][PIXELS][DAC_VALUES]
    :param char_values: Array containing DAC positions from the DACs characterization discriminator in each pixel
    :param min_threshold: Minimum value of counts above noise level
    :param factor_std_optimum: To control high and low cut on data bell
    :param opt_dac_pos: Optimum dac value calculated before
    :param n_pixels: Number of pixels in the system
    :return: NDArray containing the optimum values of discriminator for each pixel [PIX]
    """

    opt_dac_count = char_values[opt_dac_pos]
    threshold_dac_counts_mx = np.empty((len(char_data), n_pixels))
    noise_width_analysis = np.zeros(n_pixels)

    if not char_data.any():
        return np.int32(np.full(160, -1))

    else:
        for DISC in range(len(char_data)):
            for pix in range(len(char_data[0])):
                mask = char_data[DISC][pix][0:] >= min_threshold
                if not np.all(mask is False):
                    try:
                        relative_threshold_pos = np.argmax(np.flip(char_data[DISC][pix]) > min_threshold)
                        threshold_pos = len(char_data[DISC][pix]) - relative_threshold_pos
                        threshold_dac_counts_mx[DISC][pix] = char_values[threshold_pos]

                        # Noise width analysis
                        if DISC == 15:
                            noise_width_analysis[pix] = threshold_pos

                    except (ValueError, IndexError):
                        threshold_dac_counts_mx[DISC][pix] = -1
                else:
                    threshold_dac_counts_mx[DISC][pix] = -1

        # Mask pixels with noise with outlier
        arr = np.array(noise_width_analysis)
        median = np.median(arr)
        data_cut_high = median + factor_std_optimum
        mask_pixels = arr >= data_cut_high

        # Check for each IFEED the best DISC value in each pixel.
        threshold_dac_counts_mx_tp = threshold_dac_counts_mx.transpose((1, 0))  # [pix][DISC].
        opt_disc_val = np.empty((n_pixels,))  # Pixel DISC optimum empty array.

        for pix in range(len(threshold_dac_counts_mx_tp)):
            opt_disc_val[pix] = (np.abs(threshold_dac_counts_mx_tp[pix] - opt_dac_count)).argmin()

            if opt_dac_count < threshold_dac_counts_mx_tp[pix][0] or opt_dac_count > threshold_dac_counts_mx_tp[pix][len(threshold_dac_counts_mx_tp[0]) - 1]:
                opt_disc_val[pix] = -1

        # Mask pixels noise out of distribution
        opt_disc_val = np.where(mask_pixels, -1, opt_disc_val)

        return np.int32(opt_disc_val)
