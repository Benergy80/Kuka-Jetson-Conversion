"""
Hardware Watchdog

Ensures control loop is running and triggers E-stop on timeout.
"""

import threading
import time
from typing import Optional, Callable


class Watchdog:
    """
    Hardware watchdog timer.

    Must be kicked regularly by the control loop.
    Triggers E-stop if not kicked within timeout period.
    """

    def __init__(
        self,
        timeout_ms: float = 100.0,
        gpio_interface=None,
        estop_callback: Optional[Callable] = None
    ):
        """
        Initialize watchdog.

        Args:
            timeout_ms: Watchdog timeout in milliseconds
            gpio_interface: GPIO interface for hardware watchdog
            estop_callback: Callback function on timeout
        """
        self.timeout_ms = timeout_ms
        self.gpio = gpio_interface
        self.estop_callback = estop_callback

        self._last_kick_time = time.perf_counter()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start watchdog monitoring."""
        if self._running:
            return

        self._running = True
        self._last_kick_time = time.perf_counter()

        self._thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="WatchdogMonitor"
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop watchdog monitoring."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)

    def kick(self) -> None:
        """
        Kick the watchdog to prevent timeout.

        Must be called regularly from control loop.
        """
        with self._lock:
            self._last_kick_time = time.perf_counter()

        # Also toggle hardware watchdog output if available
        if self.gpio is not None:
            try:
                self.gpio.toggle_watchdog()
            except Exception:
                pass

    def get_time_since_kick(self) -> float:
        """Get time since last kick in milliseconds."""
        with self._lock:
            return (time.perf_counter() - self._last_kick_time) * 1000

    def _monitor_loop(self) -> None:
        """Monitor thread that checks for timeout."""
        check_interval = self.timeout_ms / 4 / 1000  # Check 4x per timeout period

        while self._running:
            time.sleep(check_interval)

            time_since_kick = self.get_time_since_kick()

            if time_since_kick > self.timeout_ms:
                self._handle_timeout(time_since_kick)

    def _handle_timeout(self, elapsed_ms: float) -> None:
        """Handle watchdog timeout."""
        self._running = False

        # Trigger hardware E-stop
        if self.gpio is not None:
            try:
                self.gpio.set_estop_output(False)  # Active low
            except Exception:
                pass

        # Call E-stop callback
        if self.estop_callback is not None:
            try:
                self.estop_callback(
                    f"Watchdog timeout: {elapsed_ms:.1f}ms > {self.timeout_ms}ms"
                )
            except Exception:
                pass

        print(f"WATCHDOG TIMEOUT: Control loop not responding ({elapsed_ms:.1f}ms)")
