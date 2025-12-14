"""
Hardware Interface Module

Low-level interfaces for EtherCAT, motor drives, GPIO, and encoders.
"""

from .ethercat_master import EtherCATMaster
from .drive_interface import DriveInterface, DriveConfig
from .gpio_interface import GPIOInterface
from .encoder_interface import EncoderInterface
from .io_module import IOModule

__all__ = [
    "EtherCATMaster",
    "DriveInterface",
    "DriveConfig",
    "GPIOInterface",
    "EncoderInterface",
    "IOModule",
]
