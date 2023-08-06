import logging
from BridgeAccesslib import ExtendedBridge
from MainAccesslib.characteritzation.logic.test_logic import Scan
from MainAccesslib.bc_accesspoint import chip_reg_to_pack_data, pixel_reg_to_pack_data
from MainAccesslib.global_constants import GlobalConstants
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]

# Constants
gc = GlobalConstants()


class DacScan(Scan):
    def __init__(self, dac_pos_arr: list, data_ref: int, data_low: int, data_max: int, data_incr: int,
                 bridge: ExtendedBridge, number_of_chips: int):
        """
        DAC specialization from SCAN class
        :param dac_pos_arr: List of the working DACs in the actual test, should be like: [0,1,2,3,4,5]
        :param data_ref: Reference DACs data
        :param data_low: Starting test dac value
        :param data_max: End test dac value
        :param data_incr: Increment test dac value
        :param bridge: BridgeAccesslib object
        :param number_of_chips: Number of chips in the system
        """
        super(DacScan, self).__init__(dac_pos_arr, data_ref, data_low, data_max, data_incr)
        self.bridge = bridge
        self.number_of_chips = number_of_chips

    def _init_registers(self, pixel_reg: NDArrayUint32, chip_reg: NDArrayUint32) -> NDArrayUint32:
        """
        Initialize registers
        :param pixel_reg: Pixel register data
        :param chip_reg: Chip register data
        :return: Updated chip register
        """
        md_pr = pixel_reg
        md_cr, _ = self.replace_data_in_matrix(chip_reg, self.data_ref, (0, self.DAC_REF_POS))

        for dac_pos in self.dac_pos_arr:
            md_cr, _ = self.replace_data_in_matrix(md_cr, self.data_low, (0, dac_pos))

        """ Programing chip register """
        # This is only for one chip, so we are writing the same data to all the chips.
        pack_data = chip_reg_to_pack_data(md_cr)
        self.bridge.chip_register_write(pack_data[:5], gc.BITMAP)

        """ Programing pixel register """
        # This is only for one chip, so we are writing the same data to all the chips.
        pack_data = pixel_reg_to_pack_data(md_pr)
        self.bridge.pixel_register_write(pack_data[:480], gc.BITMAP)

        return md_cr

    def test(self, pixel_reg: NDArrayUint32, chip_reg: NDArrayUint32, pulses_width: int, pulses: int, timer_reg: int,
             belt_dir: bool, test_pulses: bool, frames: int, folder_path: str, folder_name: str,
             save_flag: bool = True) -> NDArrayUint32:
        """
        Specific test scan
        :param pixel_reg: Pixel register data
        :param chip_reg: Chip register data
        :param pulses_width:
        :param pulses:
        :param timer_reg:
        :param belt_dir:
        :param test_pulses:
        :param frames:
        :param folder_path: Folder where test is saved
        :param folder_name: Name for files saved
        :param save_flag: If the user wants to save data on files
        :return: True if there is an error during the test
        """
        pixel_reg = pixel_reg.copy()
        chip_reg = chip_reg.copy()
        md_pr = self.mask_unmask_disc(pixel_reg)
        md_cr = self._init_registers(md_pr, chip_reg)
        len_out_array = self.number_of_chips * 480  # 14400

        # [ACQ_DATA][N_CHIPS][PIXELS][DAC_VALUE], [DAC_VALUE][N_CHIP]
        all_counters_data, dac_values = self.loop_scan(md_cr, pulses_width, pulses, timer_reg, belt_dir, test_pulses,
                                                       frames, self.bridge,
                                                       number_of_chips=self.number_of_chips,
                                                       len_out_array=len_out_array)

        if save_flag:
            chips_list = list(range(self.number_of_chips))  # Save data for all the chips
            self.save_data(all_counters_data, dac_values, folder_path, folder_name, chips_list)

        return all_counters_data, dac_values
