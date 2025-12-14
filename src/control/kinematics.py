"""
Robot Kinematics

Forward and inverse kinematics for Kuka robot arm using DH parameters.
"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class DHParameters:
    """Denavit-Hartenberg parameters for a joint."""
    a: float  # Link length (mm)
    d: float  # Link offset (mm)
    alpha: float  # Link twist (rad)
    theta_offset: float = 0.0  # Joint angle offset (rad)


# Default DH parameters for Kuka KR150/180/210 (to be calibrated)
DEFAULT_DH_PARAMS = [
    DHParameters(a=350, d=750, alpha=-np.pi/2),  # Joint 1
    DHParameters(a=1250, d=0, alpha=0),           # Joint 2
    DHParameters(a=55, d=0, alpha=-np.pi/2),      # Joint 3
    DHParameters(a=0, d=1100, alpha=np.pi/2),     # Joint 4
    DHParameters(a=0, d=0, alpha=-np.pi/2),       # Joint 5
    DHParameters(a=0, d=230, alpha=0),            # Joint 6 (flange)
]


def dh_matrix(theta: float, dh: DHParameters) -> np.ndarray:
    """
    Compute transformation matrix from DH parameters.

    Args:
        theta: Joint angle (rad)
        dh: DH parameters for the joint

    Returns:
        4x4 homogeneous transformation matrix
    """
    theta = theta + dh.theta_offset
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(dh.alpha), np.sin(dh.alpha)

    return np.array([
        [ct, -st*ca,  st*sa, dh.a*ct],
        [st,  ct*ca, -ct*sa, dh.a*st],
        [0,   sa,     ca,    dh.d],
        [0,   0,      0,     1]
    ])


class ForwardKinematics:
    """
    Forward kinematics solver.

    Computes end-effector pose from joint angles.
    """

    def __init__(self, dh_params: Optional[list] = None):
        """
        Initialize forward kinematics solver.

        Args:
            dh_params: List of DHParameters for each joint.
                      Uses default Kuka params if None.
        """
        self.dh_params = dh_params or DEFAULT_DH_PARAMS
        self.num_joints = len(self.dh_params)

    def compute(self, joint_angles: np.ndarray) -> np.ndarray:
        """
        Compute forward kinematics.

        Args:
            joint_angles: Joint angles (rad), shape (num_joints,)

        Returns:
            4x4 homogeneous transformation matrix (base to end-effector)
        """
        if len(joint_angles) != self.num_joints:
            raise ValueError(f"Expected {self.num_joints} joints, got {len(joint_angles)}")

        T = np.eye(4)
        for i, (theta, dh) in enumerate(zip(joint_angles, self.dh_params)):
            T = T @ dh_matrix(theta, dh)
        return T

    def get_position(self, joint_angles: np.ndarray) -> np.ndarray:
        """Get end-effector position (x, y, z) in mm."""
        T = self.compute(joint_angles)
        return T[:3, 3]

    def get_orientation(self, joint_angles: np.ndarray) -> np.ndarray:
        """Get end-effector orientation as rotation matrix."""
        T = self.compute(joint_angles)
        return T[:3, :3]


class InverseKinematics:
    """
    Inverse kinematics solver using numerical methods.

    Computes joint angles from desired end-effector pose.
    """

    def __init__(
        self,
        dh_params: Optional[list] = None,
        max_iterations: int = 100,
        tolerance: float = 1e-6,
        learning_rate: float = 0.1
    ):
        """
        Initialize inverse kinematics solver.

        Args:
            dh_params: DH parameters (uses default if None)
            max_iterations: Maximum iterations for convergence
            tolerance: Position error tolerance (mm)
            learning_rate: Step size for Jacobian pseudo-inverse method
        """
        self.fk = ForwardKinematics(dh_params)
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.learning_rate = learning_rate

    def compute(
        self,
        target_pose: np.ndarray,
        initial_guess: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, bool]:
        """
        Compute inverse kinematics using Jacobian pseudo-inverse.

        Args:
            target_pose: 4x4 target transformation matrix
            initial_guess: Initial joint angles (uses zeros if None)

        Returns:
            Tuple of (joint_angles, success)
        """
        if initial_guess is None:
            initial_guess = np.zeros(self.fk.num_joints)

        joint_angles = initial_guess.copy()
        target_position = target_pose[:3, 3]

        for iteration in range(self.max_iterations):
            current_pose = self.fk.compute(joint_angles)
            current_position = current_pose[:3, 3]

            error = target_position - current_position
            error_norm = np.linalg.norm(error)

            if error_norm < self.tolerance:
                return joint_angles, True

            # Compute Jacobian numerically
            J = self._compute_jacobian(joint_angles)

            # Pseudo-inverse update
            J_pinv = np.linalg.pinv(J)
            delta_q = self.learning_rate * J_pinv @ error
            joint_angles += delta_q

        return joint_angles, False

    def _compute_jacobian(self, joint_angles: np.ndarray, delta: float = 1e-6) -> np.ndarray:
        """Compute Jacobian numerically using finite differences."""
        n = len(joint_angles)
        J = np.zeros((3, n))

        base_pos = self.fk.get_position(joint_angles)

        for i in range(n):
            perturbed = joint_angles.copy()
            perturbed[i] += delta
            perturbed_pos = self.fk.get_position(perturbed)
            J[:, i] = (perturbed_pos - base_pos) / delta

        return J
