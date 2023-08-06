"""
    This submodule is the bridge between top layer manager and bit converter functionalities.
    Bit converter access point
"""
import numpy as np
from BitConvertAccesslib import DeepDataUnpacker, DeepDataPacker
from BitConvertAccesslib import acq_unpack
from MainAccesslib.global_constants import GlobalConstants
import numpy.typing as npt

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]

# Constants
gc = GlobalConstants()
N_SYSTEM_CHIPS = gc.SYSTEM_CHIPS
bit_len_config_chip_reg = [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 6, 1, 1, 4, 4, 14, 14, 1, 1]
bit_len_packs_chip_reg = 32
bit_len_config_pixel_reg = [1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4,
                            1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4,
                            1, 1, 1, 1, 1, 4,
                            2, 2, 2, 1, 1, 1]

bit_len_packs_pixel_reg = 32
bit_len_packs_acq = 32
bit_len_config_acq = [16, 16, 16, 16, 16, 16]

deep_data_packer = DeepDataPacker()
deep_data_unpacker = DeepDataUnpacker()


# Chip register functions
def pack_chip_reg_to_data(chip_reg_pack: list) -> NDArrayUint32:
    """
    Convert data packed inside uint32 list to the correspond matrix
    :param chip_reg_pack: List of uint32
    :return:  Register data
    """
    expected_output_shape = (N_SYSTEM_CHIPS, 19)
    mx_data_out = deep_data_unpacker.pack_to_chip_reg(chip_reg_pack, expected_output_shape, bit_len_packs_chip_reg,
                                                      bit_len_config_chip_reg)
    # (N_SYSTEM_CHIPS, 19) -> (1, N_SYSTEM_CHIPS, 19) -> (1, 19, N_SYSTEM_CHIPS)
    mx_data_out = np.expand_dims(mx_data_out, axis=0).transpose((0, 2, 1))
    return mx_data_out


def chip_reg_to_pack_data(chip_reg_data: NDArrayUint32) -> NDArrayUint32:
    """
    Convert register data to unit32 packs list
    :param chip_reg_data: Register data
    :return: Uint32 pack list
    """
    # (1, 19, N_SYSTEM_CHIPS) -> (N_SYSTEM_CHIPS, 19)
    chip_reg_data = np.array(np.squeeze(chip_reg_data, axis=0).transpose(), dtype=np.uint32)
    mx_pack_data_out = deep_data_packer.chip_reg_to_pack(chip_reg_data, bit_len_config_chip_reg, bit_len_packs_chip_reg)
    return np.array(mx_pack_data_out, dtype=np.uint32).reshape(-1)  # Converting to dimension array to one dimension


# Pixel register functions
def pack_pixel_reg_to_data(pixel_reg_pack: list) -> NDArrayUint32:
    """
    Convert data packed inside uint32 list to the correspond matrix
    :param pixel_reg_pack: List of uint32
    :return: Register data
    """
    expected_output_shape = (N_SYSTEM_CHIPS, 8, 20, 44)
    mx_data_out = deep_data_unpacker.pack_to_pixel_reg(pixel_reg_pack, expected_output_shape, bit_len_packs_pixel_reg,
                                                       bit_len_config_pixel_reg)
    # Flips columns data, (N_SYSTEM_CHIPS, 8, 20, 44) -> (44, N_SYSTEM_CHIPS, 8, 20)
    return np.flip(mx_data_out, 2).transpose((3, 0, 1, 2))


def pixel_reg_to_pack_data(pixel_reg_data: NDArrayUint32) -> NDArrayUint32:
    """
    Convert register data to unit32 packs list
    :param pixel_reg_data: Register data
    :return: Uint32 pack list
    """
    # (44, N_SYSTEM_CHIPS, 8, 20) -> (N_SYSTEM_CHIPS, 8, 20, 44)
    pixel_reg_data = np.array(pixel_reg_data, dtype=np.uint32).transpose((1, 2, 3, 0))
    mx_pack_data_out = deep_data_packer.pixel_reg_to_pack(pixel_reg_data, bit_len_config_pixel_reg,
                                                          bit_len_packs_pixel_reg)
    return np.array(mx_pack_data_out, dtype=np.uint32).reshape(-1)  # Converting to dimension array to one dimension


# ACQ
def pack_acq_to_data(acq_pack: list, tuple_transpose: tuple, tuple_reshape: tuple) -> NDArrayUint32:
    """
    Convert data packed inside uint32 list to the correspond matrix
    :param acq_pack: List of uint32
    :param tuple_transpose: Transpose tuple
    :param tuple_reshape: Reshape tuple
    :return: Acq data
    """
    out = np.array(acq_unpack(acq_pack, (N_SYSTEM_CHIPS, 8, 20, 6)), dtype=np.uint32)
    tr_mx = np.flip(np.transpose(out, (3, 0, 1, 2)), 3)  # (6,N_SYSTEM_CHIPS,8,20), and also flip columns
    return _enlarge_mx(tr_mx, tuple_transpose, tuple_reshape)


def pack_acq_to_data_tdi(acq_pack: list, tuple_transpose: tuple, tuple_reshape: tuple) -> NDArrayUint32:
    """
    Convert data packed inside uint32 list to the correspond matrix
    :param acq_pack: List of uint32
    :param tuple_transpose: Transpose tuple
    :param tuple_reshape: Reshape tuple
    :return: Acq data
    """
    out = np.array(acq_unpack(acq_pack, (8, N_SYSTEM_CHIPS, 20, 6)), dtype=np.uint32)
    flip_arr = np.flip(out, 2)  # flip columns
    return _enlarge_mx(flip_arr, tuple_transpose, tuple_reshape)


def _enlarge_mx(matrix, tuple_transpose, tuple_reshape):
    """
    Enlarge acq matrix
    :param matrix: Input acq matrix
    :param tuple_transpose: Transpose tuple
    :param tuple_reshape: Reshape tuple
    :return: Acq data
    """
    tr = matrix.transpose(tuple_transpose).reshape(tuple_reshape)
    container = np.zeros(tuple_reshape, dtype=np.uint32)
    out = np.where(container >= 0, tr, container)
    return out
