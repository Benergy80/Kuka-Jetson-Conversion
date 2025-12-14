"""
Emergency Stop Handler

Hardware and software emergency stop implementation.
Response time requirement: <50ms
"""

from typing import Callable, Optional, List
from enum import Enum, auto
import threading
import time


class EStopSource(Enum):
    """Source of E-stop trigger."""
    HARDWARE_BUTTON = auto()
    SOFTWARE_LIMIT = auto()
    WATCHDOG_TIMEOUT = auto()
    COMMUNICATION_LOSS = auto()
    SAFETY_MONITOR = auto()
    OPERATOR_COMMAND = auto()


class EmergencyStop:
    """
    Emergency stop handler.

    Provides <50ms response time for safety-critical stop.
    Coordinates hardware and software E-stop actions.
    """

    def __init__(self, gpio_interface=None):
        """
        Initialize E-stop handler.

        Args:
            gpio_interface: GPIO interface for hardware E-stop signals
        """
        self.gpio = gpio_interface
        self._is_triggered = False
        self._trigger_source: Optional[EStopSource] = None
        self._trigger_time: Optional[float] = None
        self._lock = threading.Lock()
        self._callbacks: List[Callable] = []
        self._acknowledged = False

    @property
    def is_triggered(self) -> bool:
        """Check if E-stop is currently active."""
        with self._lock:
            return self._is_triggered

    def trigger(self, source: EStopSource, reason: str = "") -> float:
        """
        Trigger emergency stop.

        Args:
            source: Source of E-stop trigger
            reason: Description of trigger reason

        Returns:
            Response time in milliseconds
        """
        start_time = time.perf_counter()

        with self._lock:
            if self._is_triggered:
                return 0  # Already triggered

            self._is_triggered = True
            self._trigger_source = source
            self._trigger_time = time.time()
            self._acknowledged = False

        # Execute hardware stop (highest priority)
        self._hardware_stop()

        # Notify callbacks
        self._notify_callbacks(source, reason)

        # Calculate response time
        response_time_ms = (time.perf_counter() - start_time) * 1000

        # Log if response time exceeds requirement
        if response_time_ms > 50:
            print(f"WARNING: E-stop response time {response_time_ms:.2f}ms exceeds 50ms requirement")

        return response_time_ms

    def _hardware_stop(self) -> None:
        """Execute hardware emergency stop."""
        if self.gpio is not None:
            # Set E-stop output (active low for fail-safe)
            try:
                self.gpio.set_estop_output(False)  # Active low
            except Exception as e:
                print(f"Hardware E-stop error: {e}")

        # Zero all motor commands would happen in control loop
        # This is just the signal layer

    def check_hardware_estop(self) -> bool:
        """
        Check hardware E-stop input.

        Returns:
            True if hardware E-stop is pressed
        """
        if self.gpio is None:
            return False

        try:
            # E-stop input is active low (pressed = False/0)
            return not self.gpio.read_estop_input()
        except Exception:
            # Communication failure - assume E-stop for safety
            return True

    def acknowledge(self) -> bool:
        """
        Acknowledge E-stop condition.

        Must be called before reset is allowed.

        Returns:
            True if acknowledgement accepted
        """
        with self._lock:
            if not self._is_triggered:
                return False
            self._acknowledged = True
            return True

    def reset(self) -> bool:
        """
        Reset E-stop if conditions allow.

        Returns:
            True if reset successful
        """
        with self._lock:
            # Cannot reset if not acknowledged
            if not self._acknowledged:
                return False

            # Cannot reset if hardware E-stop still active
            if self.check_hardware_estop():
                return False

            self._is_triggered = False
            self._trigger_source = None
            self._trigger_time = None
            self._acknowledged = False

            # Re-enable hardware outputs
            if self.gpio is not None:
                try:
                    self.gpio.set_estop_output(True)  # Release E-stop
                except Exception:
                    return False

            return True

    def register_callback(self, callback: Callable[[EStopSource, str], None]) -> None:
        """
        Register callback for E-stop events.

        Args:
            callback: Function(source, reason) called on E-stop
        """
        self._callbacks.append(callback)

    def _notify_callbacks(self, source: EStopSource, reason: str) -> None:
        """Notify all registered callbacks."""
        for callback in self._callbacks:
            try:
                callback(source, reason)
            except Exception:
                pass  # Don't let callbacks affect E-stop

    def get_status(self) -> dict:
        """Get E-stop status information."""
        with self._lock:
            return {
                "triggered": self._is_triggered,
                "source": self._trigger_source.name if self._trigger_source else None,
                "trigger_time": self._trigger_time,
                "acknowledged": self._acknowledged,
                "hardware_estop": self.check_hardware_estop(),
            }
