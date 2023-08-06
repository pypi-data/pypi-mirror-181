import numpy as np
import numpy.typing as npt
import logging
from ExcelAccesslib import ExcelOperate, InvalidFileException
from MainAccesslib.global_constants import GlobalConstants

logger = logging.getLogger(__name__)
# Typing
NDArrayUint32 = npt.NDArray[np.uint32]

# Constants
gc = GlobalConstants()


def get_linda_matrix(absolute_path: str) -> (NDArrayUint32, NDArrayUint32):
    """
    Get data from LINDA excel
    :param absolute_path: Absolute path to excel document
    :return: Chip register matrix and pixel register matrix
    """
    try:
        workbook = ExcelOperate(absolute_path)
    except InvalidFileException:
        logger.error("openpyxl does not support  file format, please check you can open it with Excel first."
                     " Supported formats are: .xlsx,.xlsm, .xltx, .xltm")
        raise FileNotFoundError

    if gc.SYSTEM_CHIPS == 30:
        chip_reg_range = ["B2:AE20", ]
        pixel_reg_ranges = ["C6:V13", "Y6:AR13", "C16:V23", "Y16:AR23", "C26:V33", "Y26:AR33",
                            "C36:V43", "Y36:AR43", "C46:V53", "Y46:AR53", "C56:V63", "Y56:AR63",
                            "C66:V73", "Y66:AR73", "C76:V83", "Y76:AR83", "C86:V93", "Y86:AR93",
                            "C96:V103", "Y96:AR103", "C106:V113", "Y106:AR113", "C116:V123", "Y116:AR123",
                            "C126:V133", "Y126:AR133", "C136:V143", "Y136:AR143", "C146:V153", "Y146:AR153"]

    elif gc.SYSTEM_CHIPS == 60:
        chip_reg_range = ["B2:BI20", ]
        pixel_reg_ranges = ["C6:V13", "Y6:AR13", "C16:V23", "Y16:AR23", "C26:V33", "Y26:AR33",
                            "C36:V43", "Y36:AR43", "C46:V53", "Y46:AR53", "C56:V63", "Y56:AR63",
                            "C66:V73", "Y66:AR73", "C76:V83", "Y76:AR83", "C86:V93", "Y86:AR93",
                            "C96:V103", "Y96:AR103", "C106:V113", "Y106:AR113", "C116:V123", "Y116:AR123",
                            "C126:V133", "Y126:AR133", "C136:V143", "Y136:AR143", "C146:V153", "Y146:AR153",

                            "C156:V163", "Y156:AR163", "C166:V173", "Y166:AR173", "C176:V183", "Y176:AR183",
                            "C186:V193", "Y186:AR193", "C196:V203", "Y196:AR203", "C206:V213", "Y206:AR213",
                            "C216:V223", "Y216:AR223", "C226:V233", "Y226:AR233", "C236:V243", "Y236:AR243",
                            "C246:V253", "Y246:AR253", "C256:V263", "Y256:AR263", "C266:V273", "Y266:AR273",
                            "C276:V283", "Y276:AR283", "C286:V293", "Y286:AR293", "C296:V303", "Y296:AR303"]
    else:
        logger.error("System chips might be 30 or 60, to interact with ex_accesspoint")
        raise AssertionError

    # Getting chip register matrix
    sheet_name = "ChipReg"
    chip_reg = workbook.range_val_to_matrix(chip_reg_range, sheet_name)
    logger.info(np.shape(chip_reg))

    # Getting pixel register matrix
    sheet_pos_pixel_reg = "all"
    pixel_reg = workbook.get_n_sheet_matrix(pixel_reg_ranges, sheet_pos_pixel_reg)
    logger.info(np.shape(pixel_reg))

    return chip_reg, pixel_reg


def write_linda_matrix(absolute_path: str, chip_reg: NDArrayUint32, pixel_reg: NDArrayUint32) -> None:
    """
    Write data to LINDA excel
    :param absolute_path: Absolute path to excel document
    :param chip_reg: Chip register data
    :param pixel_reg: Pixel register data
    """
    workbook = ExcelOperate(absolute_path)

    if gc.SYSTEM_CHIPS == 30:
        chip_reg_range = [[2, 20, 2, 31], ]
        pixel_reg_ranges = [
            [6, 13, 3, 22], [6, 13, 25, 44], [16, 23, 3, 22], [16, 23, 25, 44], [26, 33, 3, 22], [26, 33, 25, 44],
            [36, 43, 3, 22], [36, 43, 25, 44], [46, 53, 3, 22], [46, 53, 25, 44], [56, 63, 3, 22], [56, 63, 25, 44],
            [66, 73, 3, 22], [66, 73, 25, 44], [76, 83, 3, 22], [76, 83, 25, 44], [86, 93, 3, 22], [86, 93, 25, 44],
            [96, 103, 3, 22], [96, 103, 25, 44], [106, 113, 3, 22], [106, 113, 25, 44],
            [116, 123, 3, 22], [116, 123, 25, 44], [126, 133, 3, 22], [126, 133, 25, 44], [136, 143, 3, 22],
            [136, 143, 25, 44], [146, 153, 3, 22], [146, 153, 25, 44]]

    elif gc.SYSTEM_CHIPS == 60:
        chip_reg_range = [[2, 20, 2, 61], ]
        pixel_reg_ranges = [
            [6, 13, 3, 22], [6, 13, 25, 44], [16, 23, 3, 22], [16, 23, 25, 44], [26, 33, 3, 22], [26, 33, 25, 44],
            [36, 43, 3, 22], [36, 43, 25, 44], [46, 53, 3, 22], [46, 53, 25, 44], [56, 63, 3, 22], [56, 63, 25, 44],
            [66, 73, 3, 22], [66, 73, 25, 44], [76, 83, 3, 22], [76, 83, 25, 44], [86, 93, 3, 22], [86, 93, 25, 44],
            [96, 103, 3, 22], [96, 103, 25, 44], [106, 113, 3, 22], [106, 113, 25, 44],
            [116, 123, 3, 22], [116, 123, 25, 44], [126, 133, 3, 22], [126, 133, 25, 44], [136, 143, 3, 22],
            [136, 143, 25, 44], [146, 153, 3, 22], [146, 153, 25, 44],

            [156, 163, 3, 22], [156, 163, 25, 44], [166, 173, 3, 22], [166, 173, 25, 44], [166, 173, 3, 22],
            [166, 173, 25, 44], [166, 173, 3, 22], [166, 173, 25, 44], [176, 183, 3, 22], [176, 183, 25, 44],
            [176, 183, 3, 22], [176, 183, 25, 44], [176, 183, 3, 22], [176, 183, 25, 44], [186, 193, 3, 22],
            [186, 193, 25, 44], [186, 193, 3, 22], [186, 193, 25, 44], [186, 193, 3, 22], [186, 193, 25, 44],
            [196, 203, 3, 22], [196, 203, 25, 44], [196, 203, 3, 22], [196, 203, 25, 44], [196, 203, 3, 22],
            [196, 203, 25, 44], [206, 213, 3, 22], [206, 213, 25, 44], [206, 213, 3, 22], [206, 213, 25, 44],
        ]
    else:
        logger.error("System chips might be 30 or 60, to interact with ex_accesspoint")
        raise AssertionError

    # Writing chip register matrix
    sheet_name = "ChipReg"
    workbook.matrix_to_range_val(chip_reg_range, sheet_name, chip_reg, False)  # I will use for C

    # Writing pixel register matrix
    workbook.send_pixel_reg_matrix(pixel_reg_ranges, pixel_reg)
    error = workbook.save()
    if error < 0:
        logger.error("Can't save file, check if xlsx is opened!")
        raise OSError
