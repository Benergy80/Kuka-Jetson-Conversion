"""Visualization Utilities"""
import numpy as np
from typing import Optional

def plot_trajectory(positions: np.ndarray, title: str = "Trajectory"):
    """Plot joint trajectory."""
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        for i in range(positions.shape[1]):
            ax.plot(positions[:, i], label=f"Joint {i+1}")
        ax.set_xlabel("Time step")
        ax.set_ylabel("Position (rad)")
        ax.set_title(title)
        ax.legend()
        return fig
    except ImportError:
        return None

def visualize_robot(joint_angles: np.ndarray, ax=None):
    """Simple 2D visualization of robot arm."""
    try:
        import matplotlib.pyplot as plt
        if ax is None:
            fig, ax = plt.subplots()
        # Simplified 2D stick figure
        link_lengths = [0.5, 0.5, 0.3, 0.2, 0.1, 0.1]
        x, y = 0, 0
        positions = [(x, y)]
        angle = 0
        for i, (q, l) in enumerate(zip(joint_angles, link_lengths)):
            angle += q
            x += l * np.cos(angle)
            y += l * np.sin(angle)
            positions.append((x, y))
        xs, ys = zip(*positions)
        ax.plot(xs, ys, 'bo-', linewidth=2, markersize=8)
        ax.set_aspect('equal')
        return ax
    except ImportError:
        return None
