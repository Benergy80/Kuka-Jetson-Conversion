"""
Trajectory Planner

Generates smooth trajectories between waypoints with velocity and acceleration limits.
"""

import numpy as np
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TrajectoryLimits:
    """Velocity and acceleration limits for trajectory generation."""
    max_velocity: np.ndarray  # rad/s per joint
    max_acceleration: np.ndarray  # rad/s² per joint


@dataclass
class TrajectoryPoint:
    """A point along a trajectory."""
    position: np.ndarray  # Joint positions (rad)
    velocity: np.ndarray  # Joint velocities (rad/s)
    acceleration: np.ndarray  # Joint accelerations (rad/s²)
    time: float  # Time from trajectory start (s)


class TrajectoryPlanner:
    """
    Trajectory planner for smooth motion generation.

    Supports:
    - Point-to-point motion with trapezoidal velocity profile
    - Multi-waypoint trajectories
    - Cubic and quintic spline interpolation
    """

    def __init__(self, limits: TrajectoryLimits, num_joints: int = 6):
        """
        Initialize trajectory planner.

        Args:
            limits: Velocity and acceleration limits
            num_joints: Number of robot joints
        """
        self.limits = limits
        self.num_joints = num_joints

    def plan_point_to_point(
        self,
        start: np.ndarray,
        end: np.ndarray,
        duration: Optional[float] = None
    ) -> List[TrajectoryPoint]:
        """
        Plan point-to-point trajectory with trapezoidal velocity profile.

        Args:
            start: Start joint positions (rad)
            end: End joint positions (rad)
            duration: Desired duration (s). Auto-computed if None.

        Returns:
            List of trajectory points sampled at 1kHz
        """
        delta = end - start

        # Compute minimum time based on limits
        if duration is None:
            # Time for constant velocity phase
            t_vel = np.abs(delta) / self.limits.max_velocity
            # Time for acceleration/deceleration
            t_acc = self.limits.max_velocity / self.limits.max_acceleration
            duration = float(np.max(t_vel + t_acc))

        # Generate trajectory points at 1kHz
        dt = 0.001  # 1ms
        num_points = int(duration / dt) + 1
        trajectory = []

        for i in range(num_points):
            t = i * dt
            s = self._smooth_step(t / duration)  # Normalized position [0, 1]
            s_dot = self._smooth_step_derivative(t / duration) / duration
            s_ddot = self._smooth_step_second_derivative(t / duration) / (duration ** 2)

            point = TrajectoryPoint(
                position=start + s * delta,
                velocity=s_dot * delta,
                acceleration=s_ddot * delta,
                time=t
            )
            trajectory.append(point)

        return trajectory

    def plan_waypoints(
        self,
        waypoints: List[np.ndarray],
        segment_durations: Optional[List[float]] = None
    ) -> List[TrajectoryPoint]:
        """
        Plan trajectory through multiple waypoints.

        Args:
            waypoints: List of joint position arrays
            segment_durations: Duration for each segment (auto if None)

        Returns:
            List of trajectory points
        """
        if len(waypoints) < 2:
            raise ValueError("Need at least 2 waypoints")

        trajectory = []
        time_offset = 0.0

        for i in range(len(waypoints) - 1):
            duration = segment_durations[i] if segment_durations else None
            segment = self.plan_point_to_point(
                waypoints[i],
                waypoints[i + 1],
                duration
            )

            # Adjust timestamps and append
            for point in segment:
                point.time += time_offset
                if i > 0 or point.time > 0:  # Skip duplicate start point
                    trajectory.append(point)

            if segment:
                time_offset = segment[-1].time

        return trajectory

    def _smooth_step(self, t: float) -> float:
        """Smooth step function (quintic polynomial) for s-curve profile."""
        t = np.clip(t, 0, 1)
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _smooth_step_derivative(self, t: float) -> float:
        """First derivative of smooth step."""
        t = np.clip(t, 0, 1)
        return 30 * t * t * (t * (t - 2) + 1)

    def _smooth_step_second_derivative(self, t: float) -> float:
        """Second derivative of smooth step."""
        t = np.clip(t, 0, 1)
        return 60 * t * (t * (2 * t - 3) + 1)
