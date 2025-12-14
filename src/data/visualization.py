"""Data Visualization"""
import numpy as np
from typing import List, Optional

class DataVisualizer:
    """Visualization tools for robot data."""

    def __init__(self):
        self._fig = None

    def plot_trajectory(self, positions: np.ndarray, title: str = "Joint Trajectory"):
        """Plot joint trajectory over time."""
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 6))
            for i in range(positions.shape[1]):
                ax.plot(positions[:, i], label=f"Joint {i+1}")
            ax.set_xlabel("Timestep")
            ax.set_ylabel("Position (rad)")
            ax.set_title(title)
            ax.legend()
            return fig
        except ImportError:
            print("matplotlib not available")
            return None

    def plot_3d_path(self, positions: np.ndarray):
        """Plot 3D end-effector path."""
        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(positions[:, 0], positions[:, 1], positions[:, 2])
            ax.set_xlabel("X (mm)")
            ax.set_ylabel("Y (mm)")
            ax.set_zlabel("Z (mm)")
            return fig
        except ImportError:
            return None
