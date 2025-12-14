"""
Motor Drive Interface

Interface for servo drives using CiA 402 (CANopen Drive Profile).
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import IntEnum
import struct


class DriveState(IntEnum):
    """CiA 402 drive state machine states."""
    NOT_READY = 0
    SWITCH_ON_DISABLED = 1
    READY_TO_SWITCH_ON = 2
    SWITCHED_ON = 3
    OPERATION_ENABLED = 4
    QUICK_STOP_ACTIVE = 5
    FAULT_REACTION_ACTIVE = 6
    FAULT = 7


class OperationMode(IntEnum):
    """CiA 402 operation modes."""
    PROFILE_POSITION = 1
    VELOCITY = 2
    PROFILE_VELOCITY = 3
    PROFILE_TORQUE = 4
    HOMING = 6
    CYCLIC_SYNC_POSITION = 8
    CYCLIC_SYNC_VELOCITY = 9
    CYCLIC_SYNC_TORQUE = 10


@dataclass
class DriveConfig:
    """Configuration for a motor drive."""
    slave_id: int
    gear_ratio: float = 1.0
    encoder_resolution: int = 262144  # Counts per revolution
    torque_constant: float = 1.0  # Nm/A
    max_current: float = 10.0  # A
    max_velocity: float = 100.0  # rad/s
    position_offset: float = 0.0  # rad


@dataclass
class DriveStatus:
    """Current status of a drive."""
    state: DriveState
    position: float  # rad
    velocity: float  # rad/s
    torque: float  # Nm
    current: float  # A
    fault_code: int
    enabled: bool
    referenced: bool


class DriveInterface:
    """
    Interface for a single servo drive.

    Uses CiA 402 drive profile for standardized control.
    Supports cyclic synchronous position/velocity/torque modes.
    """

    def __init__(self, config: DriveConfig, ethercat_master=None):
        """
        Initialize drive interface.

        Args:
            config: Drive configuration
            ethercat_master: EtherCAT master instance
        """
        self.config = config
        self.master = ethercat_master
        self._state = DriveState.SWITCH_ON_DISABLED
        self._mode = OperationMode.CYCLIC_SYNC_POSITION

        # Position in encoder counts
        self._position_counts = 0
        self._target_position_counts = 0

    @property
    def position(self) -> float:
        """Get current position in radians."""
        return self._counts_to_rad(self._position_counts)

    @property
    def state(self) -> DriveState:
        """Get current drive state."""
        return self._state

    def enable(self) -> bool:
        """
        Enable the drive (transition to OPERATION_ENABLED).

        Returns:
            True if drive is now enabled
        """
        # CiA 402 state transitions
        transitions = [
            (DriveState.SWITCH_ON_DISABLED, DriveState.READY_TO_SWITCH_ON, 0x06),
            (DriveState.READY_TO_SWITCH_ON, DriveState.SWITCHED_ON, 0x07),
            (DriveState.SWITCHED_ON, DriveState.OPERATION_ENABLED, 0x0F),
        ]

        for from_state, to_state, control_word in transitions:
            if self._state == from_state:
                self._send_control_word(control_word)
                self._state = to_state

        return self._state == DriveState.OPERATION_ENABLED

    def disable(self) -> None:
        """Disable the drive."""
        self._send_control_word(0x00)  # Disable voltage
        self._state = DriveState.SWITCH_ON_DISABLED

    def quick_stop(self) -> None:
        """Execute quick stop."""
        self._send_control_word(0x02)  # Quick stop
        self._state = DriveState.QUICK_STOP_ACTIVE

    def fault_reset(self) -> bool:
        """
        Reset drive fault.

        Returns:
            True if fault was reset
        """
        if self._state != DriveState.FAULT:
            return False

        self._send_control_word(0x80)  # Fault reset
        self._state = DriveState.SWITCH_ON_DISABLED
        return True

    def set_mode(self, mode: OperationMode) -> bool:
        """
        Set operation mode.

        Args:
            mode: Desired operation mode

        Returns:
            True if mode change successful
        """
        if self._state == DriveState.OPERATION_ENABLED:
            # Must disable before mode change on most drives
            return False

        self._mode = mode
        # TODO: Write to modes of operation object (0x6060)
        return True

    def set_target_position(self, position: float) -> None:
        """
        Set target position (CSP mode).

        Args:
            position: Target position in radians
        """
        self._target_position_counts = self._rad_to_counts(position)

    def set_target_velocity(self, velocity: float) -> None:
        """
        Set target velocity (CSV mode).

        Args:
            velocity: Target velocity in rad/s
        """
        # TODO: Implement velocity control
        pass

    def set_target_torque(self, torque: float) -> None:
        """
        Set target torque (CST mode).

        Args:
            torque: Target torque in Nm
        """
        # TODO: Implement torque control
        pass

    def get_status(self) -> DriveStatus:
        """Get current drive status."""
        return DriveStatus(
            state=self._state,
            position=self.position,
            velocity=0.0,  # TODO: Implement
            torque=0.0,  # TODO: Implement
            current=0.0,  # TODO: Implement
            fault_code=0,
            enabled=self._state == DriveState.OPERATION_ENABLED,
            referenced=True,  # TODO: Implement homing status
        )

    def update_pdo(self) -> None:
        """
        Update PDO data for cyclic exchange.

        Called at 1kHz from control loop.
        """
        if self.master is None:
            return

        # Pack output PDO data
        # Typical CSP PDO: Control word (2) + Target position (4)
        output_data = struct.pack("<Hi", 0x0F, self._target_position_counts)
        self.master.write_pdo(self.config.slave_id, output_data)

        # Read input PDO data
        input_data = self.master.read_pdo(self.config.slave_id)
        if input_data and len(input_data) >= 6:
            # Typical CSP feedback: Status word (2) + Actual position (4)
            status_word, self._position_counts = struct.unpack("<Hi", input_data[:6])
            self._state = self._parse_status_word(status_word)

    def _counts_to_rad(self, counts: int) -> float:
        """Convert encoder counts to radians."""
        revolutions = counts / self.config.encoder_resolution
        return (revolutions * 2 * 3.14159 / self.config.gear_ratio
                + self.config.position_offset)

    def _rad_to_counts(self, radians: float) -> int:
        """Convert radians to encoder counts."""
        adjusted = radians - self.config.position_offset
        revolutions = adjusted * self.config.gear_ratio / (2 * 3.14159)
        return int(revolutions * self.config.encoder_resolution)

    def _send_control_word(self, control_word: int) -> None:
        """Send control word to drive."""
        # TODO: Implement via PDO or SDO
        pass

    def _parse_status_word(self, status_word: int) -> DriveState:
        """Parse CiA 402 status word to drive state."""
        if status_word & 0x4F == 0x00:
            return DriveState.NOT_READY
        elif status_word & 0x4F == 0x40:
            return DriveState.SWITCH_ON_DISABLED
        elif status_word & 0x6F == 0x21:
            return DriveState.READY_TO_SWITCH_ON
        elif status_word & 0x6F == 0x23:
            return DriveState.SWITCHED_ON
        elif status_word & 0x6F == 0x27:
            return DriveState.OPERATION_ENABLED
        elif status_word & 0x6F == 0x07:
            return DriveState.QUICK_STOP_ACTIVE
        elif status_word & 0x4F == 0x0F:
            return DriveState.FAULT_REACTION_ACTIVE
        elif status_word & 0x4F == 0x08:
            return DriveState.FAULT
        return DriveState.NOT_READY
