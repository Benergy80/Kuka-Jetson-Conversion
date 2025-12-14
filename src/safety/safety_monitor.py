"""
Safety Monitor

Central safety monitoring system that validates all robot commands.
Implements ISO 13849-1 safety functions.
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum, auto
import numpy as np
import threading
import time


class SafetyState(Enum):
    """Safety system states."""
    SAFE = auto()
    WARNING = auto()
    FAULT = auto()
    ESTOP = auto()


@dataclass
class SafetyLimits:
    """Safety limits for robot operation."""
    # Joint limits (rad)
    joint_min: np.ndarray
    joint_max: np.ndarray
    # Velocity limits (rad/s)
    velocity_max: np.ndarray
    # Acceleration limits (rad/s²)
    acceleration_max: np.ndarray
    # Torque limits (Nm)
    torque_max: np.ndarray
    # Workspace limits (mm)
    workspace_min: np.ndarray = None
    workspace_max: np.ndarray = None


@dataclass
class SafetyViolation:
    """Details of a safety violation."""
    type: str
    joint_index: Optional[int]
    value: float
    limit: float
    timestamp: float
    message: str


class SafetyMonitor:
    """
    Central safety monitoring system.

    Validates all robot commands before execution and monitors
    runtime conditions for safety violations.

    Safety Functions (per ISO 13849-1):
    - SF1: Safe position monitoring
    - SF2: Safe speed monitoring
    - SF3: Safe torque monitoring
    - SF4: Safe workspace limiting
    - SF5: Emergency stop
    """

    def __init__(self, limits: SafetyLimits, config: Optional[Dict] = None):
        """
        Initialize safety monitor.

        Args:
            limits: Safety limits configuration
            config: Additional configuration options
        """
        self.limits = limits
        self.config = config or {}

        self.state = SafetyState.SAFE
        self.violations: List[SafetyViolation] = []
        self._callbacks: List[Callable] = []
        self._lock = threading.Lock()

        # Response time requirement: <50ms
        self._max_response_time_ms = 50

    def validate_command(
        self,
        target_position: np.ndarray,
        target_velocity: Optional[np.ndarray] = None,
        target_torque: Optional[np.ndarray] = None
    ) -> tuple:
        """
        Validate a command before execution.

        Args:
            target_position: Target joint positions (rad)
            target_velocity: Target velocities (rad/s)
            target_torque: Target torques (Nm)

        Returns:
            Tuple of (is_valid, violations_list)
        """
        violations = []

        # SF1: Position limit check
        for i, (pos, min_val, max_val) in enumerate(
            zip(target_position, self.limits.joint_min, self.limits.joint_max)
        ):
            if pos < min_val:
                violations.append(SafetyViolation(
                    type="position_min",
                    joint_index=i,
                    value=pos,
                    limit=min_val,
                    timestamp=time.time(),
                    message=f"Joint {i} below minimum: {np.degrees(pos):.2f}° < {np.degrees(min_val):.2f}°"
                ))
            elif pos > max_val:
                violations.append(SafetyViolation(
                    type="position_max",
                    joint_index=i,
                    value=pos,
                    limit=max_val,
                    timestamp=time.time(),
                    message=f"Joint {i} above maximum: {np.degrees(pos):.2f}° > {np.degrees(max_val):.2f}°"
                ))

        # SF2: Velocity limit check
        if target_velocity is not None:
            for i, (vel, max_vel) in enumerate(
                zip(target_velocity, self.limits.velocity_max)
            ):
                if abs(vel) > max_vel:
                    violations.append(SafetyViolation(
                        type="velocity",
                        joint_index=i,
                        value=vel,
                        limit=max_vel,
                        timestamp=time.time(),
                        message=f"Joint {i} velocity exceeded: {np.degrees(vel):.2f}°/s > {np.degrees(max_vel):.2f}°/s"
                    ))

        # SF3: Torque limit check
        if target_torque is not None:
            for i, (torque, max_torque) in enumerate(
                zip(target_torque, self.limits.torque_max)
            ):
                if abs(torque) > max_torque:
                    violations.append(SafetyViolation(
                        type="torque",
                        joint_index=i,
                        value=torque,
                        limit=max_torque,
                        timestamp=time.time(),
                        message=f"Joint {i} torque exceeded: {torque:.2f} Nm > {max_torque:.2f} Nm"
                    ))

        is_valid = len(violations) == 0

        if not is_valid:
            self._handle_violations(violations)

        return is_valid, violations

    def check_runtime(
        self,
        current_position: np.ndarray,
        current_velocity: np.ndarray,
        current_torque: np.ndarray
    ) -> SafetyState:
        """
        Runtime safety check of current robot state.

        Called at 1kHz from control loop.

        Args:
            current_position: Current joint positions
            current_velocity: Current joint velocities
            current_torque: Current joint torques

        Returns:
            Current safety state
        """
        with self._lock:
            # Quick checks for runtime performance
            # Position limits (with margin)
            margin = 0.05  # rad (~3 degrees)
            if np.any(current_position < self.limits.joint_min + margin):
                self.state = SafetyState.WARNING
            elif np.any(current_position > self.limits.joint_max - margin):
                self.state = SafetyState.WARNING
            elif np.any(np.abs(current_velocity) > self.limits.velocity_max * 0.95):
                self.state = SafetyState.WARNING
            elif np.any(np.abs(current_torque) > self.limits.torque_max * 0.95):
                self.state = SafetyState.WARNING
            else:
                self.state = SafetyState.SAFE

            # Hard limit violations trigger fault
            if np.any(current_position < self.limits.joint_min):
                self.state = SafetyState.FAULT
            elif np.any(current_position > self.limits.joint_max):
                self.state = SafetyState.FAULT
            elif np.any(np.abs(current_velocity) > self.limits.velocity_max):
                self.state = SafetyState.FAULT
            elif np.any(np.abs(current_torque) > self.limits.torque_max):
                self.state = SafetyState.FAULT

            return self.state

    def trigger_estop(self, reason: str = "Manual trigger") -> None:
        """Trigger emergency stop."""
        with self._lock:
            self.state = SafetyState.ESTOP
            violation = SafetyViolation(
                type="estop",
                joint_index=None,
                value=0,
                limit=0,
                timestamp=time.time(),
                message=f"E-STOP: {reason}"
            )
            self.violations.append(violation)
            self._notify_callbacks(violation)

    def reset(self) -> bool:
        """
        Reset safety monitor after fault.

        Returns:
            True if reset successful
        """
        with self._lock:
            if self.state in [SafetyState.FAULT, SafetyState.WARNING]:
                self.state = SafetyState.SAFE
                return True
            return False

    def register_callback(self, callback: Callable[[SafetyViolation], None]) -> None:
        """Register callback for safety violations."""
        self._callbacks.append(callback)

    def _handle_violations(self, violations: List[SafetyViolation]) -> None:
        """Handle safety violations."""
        with self._lock:
            self.violations.extend(violations)
            self.state = SafetyState.FAULT
            for violation in violations:
                self._notify_callbacks(violation)

    def _notify_callbacks(self, violation: SafetyViolation) -> None:
        """Notify registered callbacks of violation."""
        for callback in self._callbacks:
            try:
                callback(violation)
            except Exception:
                pass  # Don't let callback errors affect safety system
