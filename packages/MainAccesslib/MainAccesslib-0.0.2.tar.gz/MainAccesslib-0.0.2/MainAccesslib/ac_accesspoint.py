""" Acquire data access point """
import time
import numpy as np
import numpy.typing as npt
import logging
from BridgeAccesslib import ExtendedBridge

logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]


def acq_and_pop_data(bridge: ExtendedBridge, pulses_width: int, pulses: int, timer_reg: int, belt_dir: bool,
                     test_pulses: bool, frames: int, chips_bitmap: int,
                     len_out_array: int = 14400) -> (int, NDArrayUint32):
    """
    Acquire the requested number of frames and stored in fpga buffer.
    Copies last frame of internal buffer to provided pointer or, if buffer is empty, wait for new data for
    up to timeout_ms
    :param bridge: BridgeAccesslib object
    :param pulses_width:
    :param pulses:
    :param timer_reg:
    :param belt_dir:
    :param test_pulses:
    :param frames:
    :param chips_bitmap: bitmap of the selected chip
    :param len_out_array:  expected output len
    :return: data extracted from buffer
    """
    bridge.reset_buffer()
    acq_error = _acq(bridge, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap)
    if acq_error:
        return True, np.full(len_out_array, 255, dtype=np.uint32)
    else:
        summed_data_frame = None

        for frame in range(frames):
            error, data_frame = bridge.pop_frame(time_out=600, len_out_array=len_out_array)
            if error < 0:
                logger.error("Time out to pop data frame.")
                return True, data_frame

            else:
                if frame == 0:
                    summed_data_frame = data_frame
                else:
                    summed_data_frame = np.add(summed_data_frame, data_frame)

        return False, summed_data_frame


def _acq(bridge: ExtendedBridge, pulses_width: int, pulses: int, timer_reg: int, belt_dir: bool,
         test_pulses: bool, frames: int, chips_bitmap: int) -> bool:
    """
    Acquire the requested number of frames and stored in fpga buffer. Note: see tdi is forced to False
    :param bridge: BridgeAccesslib object
    :param pulses_width:
    :param pulses:
    :param timer_reg:
    :param belt_dir:
    :param test_pulses:
    :param frames:
    :param chips_bitmap: bitmap of the selected chip
    :return: true if acq fails n times
    """
    tries: int = 6
    tdi: bool = False
    while bridge.acq(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses,
                     tdi, frames) < 0 and tries != 0:
        logger.warning("Tries: {}".format(tries))
        time.sleep(0.2)
        tries -= 1
        if tries == 1:
            logger.error("Impossible to run correctly acq dll function")
            return True

    return False


def continuous_acq_and_pop_data(bridge: ExtendedBridge, pulses_width: int, pulses: int, timer_reg: int, belt_dir: bool,
                                test_pulses: bool, tdi: bool, chips_bitmap: int,
                                len_out_array: int = 14400) -> (int, NDArrayUint32):
    """
    Copies last frame of internal buffer to provided pointer or, if buffer is empty, wait for new data for
    up to timeout_ms
    :param bridge: BridgeAccesslib object
    :param pulses_width:
    :param pulses:
    :param timer_reg:
    :param belt_dir:
    :param test_pulses:
    :param tdi:
    :param chips_bitmap: bitmap of the selected chip
    :param len_out_array:  expected output len
    :return: data extracted from buffer
    """
    bridge.reset_buffer()
    error = bridge.acq_cont(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)
    if error < 0:
        logger.error("Continuous acquisition failed. ")
        raise ConnectionError

    while True:
        error, data_frame = bridge.pop_frame(time_out=600, len_out_array=len_out_array)
        if error < 0:
            logger.error("Time out to pop data frame. Probably buffer is empty")
            raise BufferError
        yield data_frame
