import logging
from typing import List
import numpy as np
import numpy.typing as npt
from BridgeAccesslib import ExtendedBridge
from MainAccesslib.global_constants import GlobalConstants
from MainAccesslib.doc_operations import ManageCsv
from MainAccesslib.characteritzation.logic.use_matrix_operations import pr_unmask, pr_mask
from MainAccesslib.ac_accesspoint import acq_and_pop_data
from MainAccesslib.bc_accesspoint import chip_reg_to_pack_data, acq_unpack

logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]

# Constants
gc = GlobalConstants()


class Scan:
    def __init__(self, dac_pos_arr: list, data_ref: int, data_low: int, data_max: int,
                 data_incr: int):
        """
        Initialize scan class
        :param dac_pos_arr: List of the working DACs in the actual test, should be like: [0,1,2,3,4,5]
        :param data_ref: Reference DACs data
        :param data_low: Starting test dac value
        :param data_max: End test dac value
        :param data_incr: Increment test dac value
        """
        self.ERROR_MAX_ITERATIONS: int = 10  # If there are n errors on acq, exit logic and raise error
        self.CHIP_ANALYZED: int = 0  # Only saves this chip data
        self.DAC_REF_POS: int = 8  # Position inside chip_reg_matrix for the data reference
        self.data_ref = data_ref
        self.data_low = data_low
        self.data_max = data_max
        self.data_incr = data_incr
        self.dac_pos_arr = dac_pos_arr

    def mask_unmask_disc(self, pixel_reg: NDArrayUint32) -> NDArrayUint32:
        """
        Unmask working DACs and mask none working DACs
        :param pixel_reg: Pixel register data
        :return: Updated pixel_register data
        """
        md_cr = pixel_reg
        all_dac_pos = [0, 1, 2, 3, 4, 5]
        remaining_pos = list(set(all_dac_pos).symmetric_difference(set(self.dac_pos_arr)))
        for dac_pos in self.dac_pos_arr:
            md_cr = pr_unmask(md_cr, dac_pos)
        for dac_pos in remaining_pos:
            md_cr = pr_mask(md_cr, dac_pos)

        return md_cr

    def loop_scan(self, chip_register: NDArrayUint32, pulses_width: int, pulses: int, timer_reg: int, belt_dir: bool,
                  test_pulses: bool, frames: int, bridge: ExtendedBridge, len_out_array: int = 14400,
                  number_of_chips: int = 30, precision_flag: bool = False) -> (NDArrayUint32, NDArrayUint32):
        """
        It does dac scan loop with the correspond acquisitions
        :param chip_register: Chip register data
        :param pulses_width:
        :param pulses:
        :param timer_reg:
        :param belt_dir:
        :param test_pulses:
        :param frames:
        :param bridge: BridgeAccesslib object
        :param len_out_array: expected output len
        :param number_of_chips: current number of teh system
        :param precision_flag: If it is set to True, use full_array_chip_register_write
        :return: data acquired on test, and dac positions on this test
        """
        container: list = []
        dac_values_container: List[NDArrayUint32] = []
        iter_dac: int = 0
        counter_error: int = 0

        times_incr = int((self.data_max - self.data_low) / self.data_incr)

        for time_incr in range(times_incr):
            if counter_error >= self.ERROR_MAX_ITERATIONS:
                logger.error(f"Exit program,  counter_error >= {self.ERROR_MAX_ITERATIONS}")
                raise ValueError

            """Making one acq for all chips"""
            summed_data = None
            for i in range(self.ERROR_MAX_ITERATIONS):
                error, summed_data = acq_and_pop_data(bridge, pulses_width, pulses, timer_reg, belt_dir,
                                                      test_pulses, frames, gc.BITMAP, len_out_array)
                if not error:
                    break
                else:
                    counter_error += 1

            container.append(summed_data)
            iter_dac += 1

            """ ¡¡¡¡¡Here changing chip register matrix!!!!!"""
            for dac_pos in self.dac_pos_arr:
                data_incremented = np.add(chip_register[0][dac_pos], + self.data_incr)
                chip_register, error = self.replace_data_in_matrix(chip_register, data_incremented, (0, dac_pos))
                dac_values_container.append(data_incremented)

            # This is only for one chip, so we are writing the same data to all the chips.
            pack_data = chip_reg_to_pack_data(chip_register)
            if precision_flag:
                bridge.full_array_chip_register_write(pack_data, gc.BITMAP)
            else:
                bridge.chip_register_write(pack_data[:5], gc.BITMAP)

        logger.info(f"Iterations done in scan test: {iter_dac}")

        list_data = np.reshape(container, -1)
        try:
            all_counters_data = acq_unpack(list_data, (iter_dac, number_of_chips, 160, 6))
            return all_counters_data, np.uint32(dac_values_container)
        except ValueError:
            logger.info(f"All counters in data acquired are None")
            raise ValueError

    def save_data(self, all_counters_data: NDArrayUint32, dac_values: NDArrayUint32, folder_path: str, folder_name: str,
                  chips_analyzed: list) -> bool:
        """
        Save data for the correspond chips
        :param chips_analyzed: List of the chips to be analyzed
        :param all_counters_data: Data from acquisition
        :param dac_values: Dacs values from acquisition
        :param folder_path: Folder path
        :param folder_name: File name path
        :return: Error out
        """
        gen_doc = ManageCsv()
        main_folder_path = gen_doc.create_folder(folder_path, folder_name, add_time=False)
        iter_dac = len(all_counters_data)

        """ Saving dacs values"""
        gen_doc.doc_creation(dac_values, main_folder_path + f"dac_values")

        # [ACQ_DATA][N_CHIPS][PIXELS][DAC_VALUE]
        for chip in chips_analyzed:
            """ Creating folder for chip """
            folder_path = gen_doc.create_folder(main_folder_path, f"chip{chip}", add_time=False)

            # [DAC_VALUE][ACQ_DATA][PIXELS]
            data_new = all_counters_data.transpose((1, 3, 0, 2))[chip]
            data_new = np.flip(data_new, 2)
            # [DAC_VALUE][ACQ_DATA][PIXELS ROW][PIXEL COLUMNS]
            data_new = np.reshape(data_new, (len(data_new), len(data_new[0]), 8, 20))
            data_new = np.flip(data_new, 2)
            # [DAC_VALUE][PIXELS ROW][PIXEL COLUMNS][ACQ_DATA]
            data_new = data_new.transpose((0, 2, 3, 1))

            """Generating the corresponding csv"""
            for dac_pos in self.dac_pos_arr:
                # [PIXELS ROW][PIXEL COLUMNS][ACQ_DATA]
                new_chip_data = data_new[dac_pos].reshape((len(data_new[dac_pos]) *
                                                           len(data_new[dac_pos][0])), iter_dac)
                gen_doc.doc_creation(new_chip_data, folder_path + f"DAC{dac_pos}")

        return False

    def replace_data_in_matrix(self, in_matrix, new_value_matrix, pos_tuple):
        try:
            in_matrix[pos_tuple] = new_value_matrix
            return in_matrix, False
        except ValueError:
            return in_matrix, True
