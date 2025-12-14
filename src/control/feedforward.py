"""
Feedforward Compensation

Implements feedforward compensation for improved trajectory tracking.
"""

import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class DynamicsParams:
    """Dynamic parameters for feedforward compensation."""
    inertia: np.ndarray  # Joint inertias (kg·m²)
    friction_coulomb: np.ndarray  # Coulomb friction (Nm)
    friction_viscous: np.ndarray  # Viscous friction (Nm·s/rad)
    gravity_compensation: bool = True


class FeedforwardCompensator:
    """
    Feedforward compensation for improved tracking.

    Compensates for:
    - Inertia (acceleration feedforward)
    - Friction (velocity feedforward)
    - Gravity (position-dependent)
    """

    def __init__(self, params: DynamicsParams, num_joints: int = 6):
        """
        Initialize feedforward compensator.

        Args:
            params: Dynamic parameters
            num_joints: Number of robot joints
        """
        self.params = params
        self.num_joints = num_joints

    def compute(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray
    ) -> np.ndarray:
        """
        Compute feedforward torque.

        Args:
            position: Joint positions (rad)
            velocity: Joint velocities (rad/s)
            acceleration: Joint accelerations (rad/s²)

        Returns:
            Feedforward torque for each joint (Nm)
        """
        torque = np.zeros(self.num_joints)

        # Inertia compensation (τ = J * α)
        torque += self.params.inertia * acceleration

        # Friction compensation
        # Coulomb friction (sign-based)
        torque += self.params.friction_coulomb * np.sign(velocity)
        # Viscous friction (linear with velocity)
        torque += self.params.friction_viscous * velocity

        # Gravity compensation
        if self.params.gravity_compensation:
            torque += self._compute_gravity_torque(position)

        return torque

    def _compute_gravity_torque(self, position: np.ndarray) -> np.ndarray:
        """
        Compute gravity compensation torque.

        This is a simplified model. For accurate compensation,
        use the full robot dynamics model.

        Args:
            position: Joint positions (rad)

        Returns:
            Gravity compensation torque (Nm)
        """
        # Simplified gravity model (should be replaced with actual model)
        # This assumes a vertical robot with joints 2 and 3 affected by gravity
        g = 9.81  # m/s²

        gravity_torque = np.zeros(self.num_joints)

        # Joint 2 gravity compensation (simplified)
        # τ₂ = m₂ * g * L₂ * cos(θ₂)
        # Using placeholder values - need actual link masses and lengths
        gravity_torque[1] = 50.0 * np.cos(position[1])  # Nm

        # Joint 3 gravity compensation (simplified)
        gravity_torque[2] = 30.0 * np.cos(position[1] + position[2])  # Nm

        return gravity_torque
