import logging
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
# Typing
NDArrayInt32 = npt.NDArray[np.int32]


def step1(char_data: NDArrayInt32, char_values: NDArrayInt32, min_threshold: int, pct_high: int, pct_low: int,
          opt_gain: np.uint32, n_pixels: int = 160, factor_std_optimum: int = 3, ) -> NDArrayInt32:
    """
    Finds optimum IFEED values for every pixel based upon the counts chart
    :param char_data: Matrix containing characterization data with the parameters in the following ranges: [IFEED][PIXELS][DAC_VALUES]
    :param char_values: Array containing DAC values from the DAC's characterization
    :param min_threshold: Minimum value of counts above noise level
    :param pct_high: If the close IFEED gain is higher than the pct + opt_gain, mask this pixel
    :param pct_low: If the close IFEED gain is lower than the pct + opt_gain, mask this pixel
    :param n_pixels: Number of pixels in the system
    :param factor_std_optimum: To control high and low cut on data bell
    :param opt_gain: Optimum gain for every chip
    :return: NDArray containing best IFEED value for each pixel in case of not fitting the value will be -1
    """

    container = np.empty((len(char_data), n_pixels))

    if not char_data.any():
        logger.warning("Characterization data is empty, check 'char_data' input matrix.")
        return np.full(n_pixels, -1, dtype=np.int32)

    for IFEED in range(len(char_data)):
        for pos in range(len(char_data[0])):
            mask = char_data[IFEED][pos] > min_threshold
            if not np.all(mask is False):
                try:
                    min_pos = np.argmax(char_data[IFEED][pos] > min_threshold)
                    relative_max_pos = np.argmax(np.flip(char_data[IFEED][pos]) > min_threshold)
                    max_pos = len(char_data[IFEED][pos]) - relative_max_pos
                    container[IFEED][pos] = char_values[max_pos] - char_values[min_pos]
                except (ValueError, IndexError):
                    container[IFEED][pos] = -1
            else:
                container[IFEED][pos] = -1

    pixel_p_wop = np.empty(len(char_data))  # Pixel PULSE WIDTH optimum, gain optimum.

    for IFEED in range(len(container)):
        try:
            arr = np.array(container[IFEED])
            arr = arr[arr != -1]
            median = np.median(arr)
            std = np.std(arr)
            data_cut_high = median + (factor_std_optimum * std)
            data_cut_low = median - (factor_std_optimum * std)
            mask = np.logical_or(arr >= data_cut_high, arr <= data_cut_low)
            arr = np.where(mask, np.nan, arr)
            pixel_p_wop[IFEED] = np.nanmean(arr)

        except IndexError:
            "If in the pulse with calcule there is and error '-1', the gain optimum calcule will have an error too."
            pass

    if not opt_gain:
        mean_pixel_p_wop = np.mean(pixel_p_wop)  # Check the best IFEED per pixel comparing with the optimum gain.
    else:
        mean_pixel_p_wop = opt_gain

    trans_container = container.transpose(1, 0)
    pixel_ifeed: NDArrayInt32 = np.empty(n_pixels, dtype=np.int32)  # Best IFEED in each pixel.

    for pix in range(len(pixel_ifeed)):
        ifeed_pos = (np.abs(trans_container[pix] - mean_pixel_p_wop)).argmin()
        pixel_ifeed[pix] = ifeed_pos

        if trans_container[pix][ifeed_pos] > mean_pixel_p_wop + ((pct_high / 100) * mean_pixel_p_wop) or \
                trans_container[pix][ifeed_pos] < mean_pixel_p_wop - ((pct_low / 100) * mean_pixel_p_wop):
            pixel_ifeed[pix] = -1

    return pixel_ifeed


def get_opt_gain(char_data: NDArrayInt32, char_values: NDArrayInt32, min_threshold: int,
                 n_pixels: int = 160, factor_std_optimum: int = 3) -> np.uint32:
    """
    This algorithm calculate the optimum gain based on IFEED
    :param char_data: Input data, [IFEED][PIXELS][DATA]
    :param char_values: Dac values on the corresponding characterization test, [DAC_VALUES]
    :param min_threshold: If the counts acquired are under this threshold will be masked
    :param n_pixels: Number of pixels. Must be 160
    :param factor_std_optimum: To control high and low cut on data bell
    :return: Optimum gain
    """

    container = np.empty((len(char_data), n_pixels))

    if not char_data.any():
        logger.warning("Characterization data is empty, check 'char_data' input matrix.")
        return np.uint32(0)

    for IFEED in range(len(char_data)):
        for pos in range(len(char_data[0])):
            mask = char_data[IFEED][pos] > min_threshold
            if not np.all(mask is False):
                try:
                    min_pos = np.argmax(char_data[IFEED][pos] > min_threshold)
                    relative_max_pos = np.argmax(np.flip(char_data[IFEED][pos]) > min_threshold)
                    max_pos = len(char_data[IFEED][pos]) - relative_max_pos
                    container[IFEED][pos] = char_values[max_pos] - char_values[min_pos]
                except (ValueError, IndexError):
                    container[IFEED][pos] = -1
            else:
                container[IFEED][pos] = -1

    pixel_p_wop = np.empty(len(char_data))  # Pixel PULSE WIDTH optimum, gain optimum.

    for IFEED in range(len(container)):
        try:
            arr = np.array(container[IFEED])
            arr = arr[arr != -1]
            median = np.median(arr)
            std = np.std(arr)
            data_cut_high = median + (factor_std_optimum * std)
            data_cut_low = median - (factor_std_optimum * std)
            mask = np.logical_or(arr >= data_cut_high, arr <= data_cut_low)
            arr = np.where(mask, np.nan, arr)
            pixel_p_wop[IFEED] = np.nanmean(arr)
        except IndexError:
            "If in the pulse we are calculating there is and error '-1', the gain optimum calculated" \
            " will have an error too."
            pass

    return np.mean(pixel_p_wop)
