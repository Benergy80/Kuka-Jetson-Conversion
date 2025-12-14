"""Input Devices for Teleoperation"""
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional

class InputDevice(ABC):
    """Abstract base class for input devices."""

    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass

    @abstractmethod
    def get_command(self) -> Optional[np.ndarray]: pass

class SpaceMouse(InputDevice):
    """3Dconnexion SpaceMouse interface."""

    def __init__(self, device_path: str = "/dev/hidraw0"):
        self.device_path = device_path
        self._running = False

    def start(self):
        self._running = True
        # TODO: Open HID device

    def stop(self):
        self._running = False

    def get_command(self) -> Optional[np.ndarray]:
        if not self._running:
            return None
        # TODO: Read from SpaceMouse
        return np.zeros(6)

class Gamepad(InputDevice):
    """Gamepad/joystick interface."""

    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self._running = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def get_command(self) -> Optional[np.ndarray]:
        if not self._running:
            return None
        # TODO: Read from gamepad via pygame or similar
        return np.zeros(6)
