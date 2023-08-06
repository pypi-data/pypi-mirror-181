import os
import logging
from MainAccesslib import ex_accesspoint
from MainAccesslib import bc_accesspoint
from MainAccesslib import ac_accesspoint
from MainAccesslib.comm_accesspoint import Connection
from BridgeAccesslib import ExtendedBridge
from MainAccesslib.global_constants import GlobalConstants
from MainAccesslib.characteritzation.dac_scan import DacScan
from MainAccesslib.characteritzation.disc_scan import DiscScan
from MainAccesslib.characteritzation.ifeed_scan import IfeedScan
from MainAccesslib.characteritzation.disc_precision_scan import DiscScanPrecision
from MainAccesslib.equalization import one_ifeed
from MainAccesslib.equalization import two_disc
from MainAccesslib.equalization import three_disc_precision

input_data_path = os.path.abspath(os.path.dirname(__file__))
LOG_FILE_PATH = os.path.join(input_data_path, 'data', 'logg.txt')
LOGG_LEVEL = logging.INFO

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(LOGG_LEVEL)
logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

__author__ = "Jordi Arellano <jordiarellano1996@gmail.com>"
__status__ = "development"
# The following module attributes are no longer updated.
__version__ = "0.0.0.1"
__date__ = "25 Oct 2022"

__all__ = {
    ex_accesspoint,
    GlobalConstants,
    ExtendedBridge,
    Connection,
    bc_accesspoint,
    ac_accesspoint,
    DacScan,
    DiscScan,
    IfeedScan,
    DiscScanPrecision,
    one_ifeed,
    two_disc,
    three_disc_precision,

}
