"""
Encoder Interface

Interface for absolute encoders providing position feedback.
"""

from typing import Optional
from dataclasses import dataclass
from enum import Enum


class EncoderType(Enum):
    """Types of encoders."""
    INCREMENTAL = "incremental"
    ABSOLUTE = "absolute"
    ABSOLUTE_MULTITURN = "absolute_multiturn"


@dataclass
class EncoderConfig:
    """Encoder configuration."""
    type: EncoderType
    resolution: int  # Counts per revolution
    max_turns: int = 1  # For multiturn encoders
    reverse_direction: bool = False
    zero_offset: int = 0  # Counts offset for zero position


class EncoderInterface:
    """
    Interface for position encoders.

    Supports absolute encoders typically used in industrial servo systems.
    Position is read via EtherCAT drive feedback.
    """

    def __init__(self, config: EncoderConfig, drive_interface=None):
        """
        Initialize encoder interface.

        Args:
            config: Encoder configuration
            drive_interface: Associated drive interface
        """
        self.config = config
        self.drive = drive_interface

        self._raw_position = 0
        self._position_rad = 0.0
        self._velocity_rad = 0.0
        self._last_position = 0
        self._last_time: Optional[float] = None

    @property
    def position(self) -> float:
        """Get current position in radians."""
        return self._position_rad

    @property
    def velocity(self) -> float:
        """Get current velocity in rad/s."""
        return self._velocity_rad

    @property
    def raw_counts(self) -> int:
        """Get raw encoder counts."""
        return self._raw_position

    def update(self, timestamp: float) -> None:
        """
        Update encoder readings.

        Called at 1kHz from control loop.

        Args:
            timestamp: Current time in seconds
        """
        # Read raw position from drive
        if self.drive is not None:
            # Position is typically in the drive's feedback PDO
            status = self.drive.get_status()
            self._raw_position = self._rad_to_counts(status.position)

        # Apply direction and offset
        adjusted = self._raw_position - self.config.zero_offset
        if self.config.reverse_direction:
            adjusted = -adjusted

        # Convert to radians
        self._position_rad = self._counts_to_rad(adjusted)

        # Calculate velocity
        if self._last_time is not None:
            dt = timestamp - self._last_time
            if dt > 0:
                delta_counts = adjusted - self._last_position
                self._velocity_rad = self._counts_to_rad(delta_counts) / dt

        self._last_position = adjusted
        self._last_time = timestamp

    def set_zero(self) -> None:
        """Set current position as zero."""
        self.config.zero_offset = self._raw_position

    def set_position(self, position_rad: float) -> None:
        """
        Set encoder position to specified value.

        Args:
            position_rad: Position in radians
        """
        target_counts = self._rad_to_counts(position_rad)
        if self.config.reverse_direction:
            target_counts = -target_counts
        self.config.zero_offset = self._raw_position - target_counts

    def _counts_to_rad(self, counts: int) -> float:
        """Convert counts to radians."""
        return counts * 2 * 3.14159 / self.config.resolution

    def _rad_to_counts(self, radians: float) -> int:
        """Convert radians to counts."""
        return int(radians * self.config.resolution / (2 * 3.14159))

    def get_turns(self) -> int:
        """
        Get number of complete turns (for multiturn encoders).

        Returns:
            Number of complete revolutions
        """
        if self.config.type != EncoderType.ABSOLUTE_MULTITURN:
            return 0

        return self._raw_position // self.config.resolution

    def is_valid(self) -> bool:
        """
        Check if encoder reading is valid.

        Returns:
            True if reading appears valid
        """
        # Check for obvious errors
        if self.config.type == EncoderType.ABSOLUTE_MULTITURN:
            if abs(self.get_turns()) > self.config.max_turns:
                return False

        # Check for unreasonable velocity (likely noise or error)
        max_velocity = 100  # rad/s - should be configurable
        if abs(self._velocity_rad) > max_velocity:
            return False

        return True
