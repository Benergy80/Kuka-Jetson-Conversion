"""
Limit Checker

Validates joint limits, velocity limits, and acceleration limits.
"""

from typing import Optional, Tuple, List
from dataclasses import dataclass
import numpy as np


@dataclass
class JointLimits:
    """Limits for a single joint."""
    position_min: float  # rad
    position_max: float  # rad
    velocity_max: float  # rad/s
    acceleration_max: float  # rad/s²
    torque_max: float  # Nm
    jerk_max: float = 1000.0  # rad/s³


class LimitChecker:
    """
    Joint limit validation.

    Checks:
    - Position limits (hard stops)
    - Velocity limits
    - Acceleration limits
    - Jerk limits (for smoothness)
    - Torque limits
    """

    def __init__(self, joint_limits: List[JointLimits]):
        """
        Initialize limit checker.

        Args:
            joint_limits: List of limits for each joint
        """
        self.joint_limits = joint_limits
        self.num_joints = len(joint_limits)

        # Convert to numpy arrays for fast checking
        self.pos_min = np.array([j.position_min for j in joint_limits])
        self.pos_max = np.array([j.position_max for j in joint_limits])
        self.vel_max = np.array([j.velocity_max for j in joint_limits])
        self.acc_max = np.array([j.acceleration_max for j in joint_limits])
        self.torque_max = np.array([j.torque_max for j in joint_limits])

    def check_position(self, position: np.ndarray) -> Tuple[bool, Optional[str]]:
        """
        Check if position is within limits.

        Args:
            position: Joint positions (rad)

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(position) != self.num_joints:
            return False, f"Expected {self.num_joints} joints, got {len(position)}"

        violations = []

        for i, (pos, min_val, max_val) in enumerate(
            zip(position, self.pos_min, self.pos_max)
        ):
            if pos < min_val:
                violations.append(
                    f"Joint {i}: {np.degrees(pos):.1f}° < min {np.degrees(min_val):.1f}°"
                )
            elif pos > max_val:
                violations.append(
                    f"Joint {i}: {np.degrees(pos):.1f}° > max {np.degrees(max_val):.1f}°"
                )

        if violations:
            return False, "; ".join(violations)
        return True, None

    def check_velocity(self, velocity: np.ndarray) -> Tuple[bool, Optional[str]]:
        """
        Check if velocity is within limits.

        Args:
            velocity: Joint velocities (rad/s)

        Returns:
            Tuple of (is_valid, error_message)
        """
        violations = []

        for i, (vel, max_vel) in enumerate(zip(velocity, self.vel_max)):
            if abs(vel) > max_vel:
                violations.append(
                    f"Joint {i}: {np.degrees(vel):.1f}°/s > max {np.degrees(max_vel):.1f}°/s"
                )

        if violations:
            return False, "; ".join(violations)
        return True, None

    def check_acceleration(self, acceleration: np.ndarray) -> Tuple[bool, Optional[str]]:
        """Check if acceleration is within limits."""
        violations = []

        for i, (acc, max_acc) in enumerate(zip(acceleration, self.acc_max)):
            if abs(acc) > max_acc:
                violations.append(
                    f"Joint {i}: {np.degrees(acc):.1f}°/s² > max {np.degrees(max_acc):.1f}°/s²"
                )

        if violations:
            return False, "; ".join(violations)
        return True, None

    def check_torque(self, torque: np.ndarray) -> Tuple[bool, Optional[str]]:
        """Check if torque is within limits."""
        violations = []

        for i, (t, max_t) in enumerate(zip(torque, self.torque_max)):
            if abs(t) > max_t:
                violations.append(
                    f"Joint {i}: {t:.1f} Nm > max {max_t:.1f} Nm"
                )

        if violations:
            return False, "; ".join(violations)
        return True, None

    def clamp_position(self, position: np.ndarray) -> np.ndarray:
        """Clamp position to within limits."""
        return np.clip(position, self.pos_min, self.pos_max)

    def clamp_velocity(self, velocity: np.ndarray) -> np.ndarray:
        """Clamp velocity to within limits."""
        return np.clip(velocity, -self.vel_max, self.vel_max)

    def scale_velocity(self, velocity: np.ndarray) -> np.ndarray:
        """
        Scale velocity to stay within all limits.

        Maintains direction but reduces magnitude if any joint exceeds limit.
        """
        max_ratio = np.max(np.abs(velocity) / self.vel_max)
        if max_ratio > 1.0:
            return velocity / max_ratio
        return velocity

    def get_margin(self, position: np.ndarray) -> np.ndarray:
        """
        Get margin to nearest limit for each joint.

        Returns:
            Array of minimum distances to limit (positive = safe)
        """
        margin_min = position - self.pos_min
        margin_max = self.pos_max - position
        return np.minimum(margin_min, margin_max)
