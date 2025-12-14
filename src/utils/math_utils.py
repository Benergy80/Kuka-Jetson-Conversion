"""Math Utilities"""
import numpy as np

def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi]."""
    while angle > np.pi:
        angle -= 2 * np.pi
    while angle < -np.pi:
        angle += 2 * np.pi
    return angle

def rotation_matrix(axis: str, angle: float) -> np.ndarray:
    """Create rotation matrix around specified axis."""
    c, s = np.cos(angle), np.sin(angle)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    elif axis == "z":
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    raise ValueError(f"Invalid axis: {axis}")

def skew_symmetric(v: np.ndarray) -> np.ndarray:
    """Create skew-symmetric matrix from 3D vector."""
    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])

def interpolate_poses(pose1: np.ndarray, pose2: np.ndarray, t: float) -> np.ndarray:
    """Linear interpolation between two poses (position only)."""
    return pose1 + t * (pose2 - pose1)
