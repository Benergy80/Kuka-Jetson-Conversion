"""
GPIO Interface

GPIO control for safety signals, status LEDs, and digital I/O.
Designed for Jetson Orin Nano GPIO pins.
"""

from typing import Dict, Optional, Callable
from enum import Enum
import threading


class PinMode(Enum):
    """GPIO pin modes."""
    INPUT = "in"
    OUTPUT = "out"


class PinState(Enum):
    """GPIO pin states."""
    LOW = 0
    HIGH = 1


# Jetson Orin Nano GPIO pin mapping (placeholder - verify with actual board)
GPIO_PIN_MAP = {
    "ESTOP_INPUT": 7,      # Hardware E-stop input (active low)
    "ESTOP_OUTPUT": 11,    # E-stop relay output
    "WATCHDOG": 12,        # Watchdog toggle output
    "SAFETY_OK": 13,       # Safety status LED
    "ML_ACTIVE": 15,       # ML mode indicator LED
    "GCODE_ACTIVE": 16,    # G-code mode indicator LED
    "ENABLE_INPUT": 18,    # Enable switch input
    "HOME_SENSOR_1": 22,   # Homing sensor inputs
    "HOME_SENSOR_2": 29,
    "HOME_SENSOR_3": 31,
    "HOME_SENSOR_4": 32,
    "HOME_SENSOR_5": 33,
    "HOME_SENSOR_6": 35,
}


class GPIOInterface:
    """
    GPIO interface for Jetson Orin Nano.

    Provides:
    - E-stop input/output
    - Watchdog toggle
    - Status LEDs
    - Enable switch input
    - Homing sensor inputs
    """

    def __init__(self, simulation_mode: bool = False):
        """
        Initialize GPIO interface.

        Args:
            simulation_mode: If True, don't access real GPIO (for testing)
        """
        self.simulation_mode = simulation_mode
        self._pin_states: Dict[str, PinState] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._initialized = False

    def initialize(self) -> bool:
        """
        Initialize GPIO pins.

        Returns:
            True if initialization successful
        """
        if self.simulation_mode:
            self._initialized = True
            return True

        try:
            # Import Jetson GPIO library
            import Jetson.GPIO as GPIO
            self._gpio = GPIO

            GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers

            # Configure pins
            GPIO.setup(GPIO_PIN_MAP["ESTOP_INPUT"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(GPIO_PIN_MAP["ENABLE_INPUT"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(GPIO_PIN_MAP["ESTOP_OUTPUT"], GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(GPIO_PIN_MAP["WATCHDOG"], GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(GPIO_PIN_MAP["SAFETY_OK"], GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(GPIO_PIN_MAP["ML_ACTIVE"], GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(GPIO_PIN_MAP["GCODE_ACTIVE"], GPIO.OUT, initial=GPIO.LOW)

            # Configure homing sensor inputs
            for i in range(1, 7):
                pin = GPIO_PIN_MAP.get(f"HOME_SENSOR_{i}")
                if pin:
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Set up E-stop interrupt
            GPIO.add_event_detect(
                GPIO_PIN_MAP["ESTOP_INPUT"],
                GPIO.FALLING,
                callback=self._estop_callback,
                bouncetime=50
            )

            self._initialized = True
            return True

        except Exception as e:
            print(f"GPIO initialization failed: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        if not self.simulation_mode and self._initialized:
            try:
                self._gpio.cleanup()
            except Exception:
                pass
        self._initialized = False

    def read_estop_input(self) -> bool:
        """
        Read hardware E-stop input.

        Returns:
            True if E-stop is NOT pressed (safe)
        """
        if self.simulation_mode:
            return self._pin_states.get("ESTOP_INPUT", PinState.HIGH) == PinState.HIGH

        try:
            return self._gpio.input(GPIO_PIN_MAP["ESTOP_INPUT"]) == self._gpio.HIGH
        except Exception:
            return False  # Fail safe

    def set_estop_output(self, state: bool) -> None:
        """
        Set E-stop relay output.

        Args:
            state: True = release E-stop, False = trigger E-stop
        """
        with self._lock:
            if self.simulation_mode:
                self._pin_states["ESTOP_OUTPUT"] = PinState.HIGH if state else PinState.LOW
            else:
                try:
                    self._gpio.output(
                        GPIO_PIN_MAP["ESTOP_OUTPUT"],
                        self._gpio.HIGH if state else self._gpio.LOW
                    )
                except Exception:
                    pass

    def toggle_watchdog(self) -> None:
        """Toggle watchdog output pin."""
        with self._lock:
            if self.simulation_mode:
                current = self._pin_states.get("WATCHDOG", PinState.LOW)
                self._pin_states["WATCHDOG"] = PinState.HIGH if current == PinState.LOW else PinState.LOW
            else:
                try:
                    current = self._gpio.input(GPIO_PIN_MAP["WATCHDOG"])
                    self._gpio.output(
                        GPIO_PIN_MAP["WATCHDOG"],
                        self._gpio.LOW if current else self._gpio.HIGH
                    )
                except Exception:
                    pass

    def set_safety_led(self, state: bool) -> None:
        """Set safety OK LED."""
        self._set_output("SAFETY_OK", state)

    def set_ml_active_led(self, state: bool) -> None:
        """Set ML active LED."""
        self._set_output("ML_ACTIVE", state)

    def set_gcode_active_led(self, state: bool) -> None:
        """Set G-code active LED."""
        self._set_output("GCODE_ACTIVE", state)

    def read_enable_input(self) -> bool:
        """Read enable switch state."""
        if self.simulation_mode:
            return self._pin_states.get("ENABLE_INPUT", PinState.HIGH) == PinState.HIGH

        try:
            return self._gpio.input(GPIO_PIN_MAP["ENABLE_INPUT"]) == self._gpio.HIGH
        except Exception:
            return False

    def read_homing_sensor(self, axis: int) -> bool:
        """
        Read homing sensor for specified axis.

        Args:
            axis: Axis number (1-6)

        Returns:
            True if sensor is triggered
        """
        pin_name = f"HOME_SENSOR_{axis}"
        if self.simulation_mode:
            return self._pin_states.get(pin_name, PinState.HIGH) == PinState.LOW

        try:
            pin = GPIO_PIN_MAP.get(pin_name)
            if pin:
                return self._gpio.input(pin) == self._gpio.LOW
        except Exception:
            pass
        return False

    def register_estop_callback(self, callback: Callable[[], None]) -> None:
        """Register callback for E-stop events."""
        self._callbacks["estop"] = callback

    def _set_output(self, pin_name: str, state: bool) -> None:
        """Set output pin state."""
        with self._lock:
            if self.simulation_mode:
                self._pin_states[pin_name] = PinState.HIGH if state else PinState.LOW
            else:
                try:
                    pin = GPIO_PIN_MAP.get(pin_name)
                    if pin:
                        self._gpio.output(pin, self._gpio.HIGH if state else self._gpio.LOW)
                except Exception:
                    pass

    def _estop_callback(self, channel) -> None:
        """Internal callback for E-stop interrupt."""
        callback = self._callbacks.get("estop")
        if callback:
            try:
                callback()
            except Exception:
                pass
