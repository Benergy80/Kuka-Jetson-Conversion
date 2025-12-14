"""
PID Controller

Implementation of PID control with feedforward for each joint.
"""

import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class PIDGains:
    """PID gains for a single joint."""
    kp: float  # Proportional gain
    ki: float  # Integral gain
    kd: float  # Derivative gain
    kff_vel: float = 0.0  # Velocity feedforward gain
    kff_acc: float = 0.0  # Acceleration feedforward gain
    integral_limit: float = 100.0  # Anti-windup limit
    output_limit: float = 1000.0  # Output saturation


class PIDController:
    """
    PID controller with feedforward compensation.

    Features:
    - Per-joint PID control
    - Velocity and acceleration feedforward
    - Anti-windup with integral clamping
    - Output saturation
    """

    def __init__(self, gains: PIDGains):
        """
        Initialize PID controller.

        Args:
            gains: PID gains and limits
        """
        self.gains = gains
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time: Optional[float] = None

    def reset(self) -> None:
        """Reset controller state."""
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time = None

    def compute(
        self,
        target: float,
        actual: float,
        dt: float,
        target_velocity: float = 0.0,
        target_acceleration: float = 0.0
    ) -> float:
        """
        Compute PID output.

        Args:
            target: Target position
            actual: Actual position
            dt: Time step (s)
            target_velocity: Target velocity for feedforward
            target_acceleration: Target acceleration for feedforward

        Returns:
            Control output (torque command)
        """
        error = target - actual

        # Proportional term
        p_term = self.gains.kp * error

        # Integral term with anti-windup
        self._integral += error * dt
        self._integral = np.clip(
            self._integral,
            -self.gains.integral_limit,
            self.gains.integral_limit
        )
        i_term = self.gains.ki * self._integral

        # Derivative term
        d_error = (error - self._prev_error) / dt if dt > 0 else 0.0
        d_term = self.gains.kd * d_error

        # Feedforward terms
        ff_vel = self.gains.kff_vel * target_velocity
        ff_acc = self.gains.kff_acc * target_acceleration

        # Total output with saturation
        output = p_term + i_term + d_term + ff_vel + ff_acc
        output = np.clip(output, -self.gains.output_limit, self.gains.output_limit)

        # Store for next iteration
        self._prev_error = error

        return output


class MultiJointPIDController:
    """PID controller for multiple joints."""

    def __init__(self, gains_list: list):
        """
        Initialize multi-joint PID controller.

        Args:
            gains_list: List of PIDGains for each joint
        """
        self.controllers = [PIDController(gains) for gains in gains_list]
        self.num_joints = len(self.controllers)

    def reset(self) -> None:
        """Reset all controllers."""
        for controller in self.controllers:
            controller.reset()

    def compute(
        self,
        targets: np.ndarray,
        actuals: np.ndarray,
        dt: float,
        target_velocities: Optional[np.ndarray] = None,
        target_accelerations: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Compute PID outputs for all joints.

        Args:
            targets: Target positions for all joints
            actuals: Actual positions for all joints
            dt: Time step (s)
            target_velocities: Target velocities (optional)
            target_accelerations: Target accelerations (optional)

        Returns:
            Control outputs for all joints
        """
        if target_velocities is None:
            target_velocities = np.zeros(self.num_joints)
        if target_accelerations is None:
            target_accelerations = np.zeros(self.num_joints)

        outputs = np.zeros(self.num_joints)
        for i, controller in enumerate(self.controllers):
            outputs[i] = controller.compute(
                targets[i],
                actuals[i],
                dt,
                target_velocities[i],
                target_accelerations[i]
            )

        return outputs
