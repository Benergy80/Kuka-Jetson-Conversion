"""Teleoperation Controller"""
import numpy as np
from typing import Optional, Dict

class TeleoperationController:
    """Controls robot via human teleoperation input."""

    def __init__(self, robot_controller, input_device):
        self.robot = robot_controller
        self.input = input_device
        self._scaling = np.array([1.0, 1.0, 1.0, 0.5, 0.5, 0.5])  # Position and rotation scaling
        self._is_active = False

    def start(self):
        """Start teleoperation mode."""
        self._is_active = True
        self.input.start()

    def stop(self):
        """Stop teleoperation mode."""
        self._is_active = False
        self.input.stop()

    def update(self) -> Optional[np.ndarray]:
        """Get teleop command and apply to robot."""
        if not self._is_active:
            return None

        command = self.input.get_command()
        if command is None:
            return None

        scaled = command * self._scaling
        # Convert to joint space or send as Cartesian
        return scaled

    def set_scaling(self, scaling: np.ndarray):
        """Set motion scaling factors."""
        self._scaling = scaling
