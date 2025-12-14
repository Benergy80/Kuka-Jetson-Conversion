"""
Mode Manager

Manages switching between control modes: G-code, ML autonomous, manual, and E-stop.
"""

from enum import Enum, auto
from typing import Optional, Callable, Dict
from dataclasses import dataclass
import threading
import time


class ControlMode(Enum):
    """Control modes for the robot."""
    IDLE = auto()
    GCODE = auto()  # Traditional G-code execution
    ML_AUTONOMOUS = auto()  # ML policy control
    MANUAL = auto()  # Teleoperation/jog mode
    ESTOP = auto()  # Emergency stop (highest priority)


@dataclass
class ModeTransition:
    """A mode transition event."""
    from_mode: ControlMode
    to_mode: ControlMode
    timestamp: float
    reason: str


class ModeManager:
    """
    Manages control mode transitions with safety validation.

    Ensures safe transitions between modes and prevents
    invalid state changes (e.g., cannot exit E-stop without reset).
    """

    # Valid mode transitions (from_mode -> list of allowed to_modes)
    VALID_TRANSITIONS: Dict[ControlMode, list] = {
        ControlMode.IDLE: [ControlMode.GCODE, ControlMode.ML_AUTONOMOUS, ControlMode.MANUAL, ControlMode.ESTOP],
        ControlMode.GCODE: [ControlMode.IDLE, ControlMode.ESTOP],
        ControlMode.ML_AUTONOMOUS: [ControlMode.IDLE, ControlMode.GCODE, ControlMode.ESTOP],
        ControlMode.MANUAL: [ControlMode.IDLE, ControlMode.ESTOP],
        ControlMode.ESTOP: [ControlMode.IDLE],  # Only can go to IDLE after reset
    }

    def __init__(self):
        """Initialize mode manager."""
        self._current_mode = ControlMode.IDLE
        self._mode_lock = threading.Lock()
        self._transition_callbacks: list = []
        self._estop_active = False
        self._estop_acknowledged = False

    @property
    def current_mode(self) -> ControlMode:
        """Get current control mode."""
        with self._mode_lock:
            return self._current_mode

    def request_mode_change(self, new_mode: ControlMode, reason: str = "") -> bool:
        """
        Request a mode change.

        Args:
            new_mode: Requested new mode
            reason: Reason for the change

        Returns:
            True if mode change was successful
        """
        with self._mode_lock:
            # E-stop can always be activated
            if new_mode == ControlMode.ESTOP:
                return self._activate_estop(reason)

            # Check if transition is valid
            if new_mode not in self.VALID_TRANSITIONS.get(self._current_mode, []):
                return False

            # Special handling for exiting E-stop
            if self._current_mode == ControlMode.ESTOP:
                if not self._estop_acknowledged:
                    return False

            # Perform transition
            old_mode = self._current_mode
            self._current_mode = new_mode

            transition = ModeTransition(
                from_mode=old_mode,
                to_mode=new_mode,
                timestamp=time.time(),
                reason=reason
            )

            # Notify callbacks
            self._notify_transition(transition)

            return True

    def trigger_estop(self, reason: str = "Manual E-stop") -> None:
        """
        Trigger emergency stop (can be called from any state).

        Args:
            reason: Reason for E-stop
        """
        self.request_mode_change(ControlMode.ESTOP, reason)

    def acknowledge_estop(self) -> None:
        """Acknowledge E-stop condition (required before reset)."""
        with self._mode_lock:
            if self._current_mode == ControlMode.ESTOP:
                self._estop_acknowledged = True

    def reset_from_estop(self) -> bool:
        """
        Reset from E-stop to IDLE.

        Returns:
            True if reset was successful
        """
        with self._mode_lock:
            if self._current_mode != ControlMode.ESTOP:
                return False
            if not self._estop_acknowledged:
                return False

            self._estop_active = False
            self._estop_acknowledged = False
            self._current_mode = ControlMode.IDLE

            transition = ModeTransition(
                from_mode=ControlMode.ESTOP,
                to_mode=ControlMode.IDLE,
                timestamp=time.time(),
                reason="E-stop reset"
            )
            self._notify_transition(transition)

            return True

    def register_callback(self, callback: Callable[[ModeTransition], None]) -> None:
        """
        Register callback for mode transitions.

        Args:
            callback: Function called on each transition
        """
        self._transition_callbacks.append(callback)

    def _activate_estop(self, reason: str) -> bool:
        """Activate E-stop."""
        old_mode = self._current_mode
        self._current_mode = ControlMode.ESTOP
        self._estop_active = True
        self._estop_acknowledged = False

        transition = ModeTransition(
            from_mode=old_mode,
            to_mode=ControlMode.ESTOP,
            timestamp=time.time(),
            reason=reason
        )
        self._notify_transition(transition)

        return True

    def _notify_transition(self, transition: ModeTransition) -> None:
        """Notify all registered callbacks of transition."""
        for callback in self._transition_callbacks:
            try:
                callback(transition)
            except Exception as e:
                # Log but don't fail on callback errors
                print(f"Mode transition callback error: {e}")
