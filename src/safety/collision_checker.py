"""
Collision Checker

Checks for potential collisions with workspace boundaries and obstacles.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class BoundingBox:
    """Axis-aligned bounding box for collision checking."""
    min_point: np.ndarray  # [x_min, y_min, z_min] (mm)
    max_point: np.ndarray  # [x_max, y_max, z_max] (mm)
    name: str = "obstacle"


@dataclass
class Sphere:
    """Sphere for collision checking."""
    center: np.ndarray  # [x, y, z] (mm)
    radius: float  # mm
    name: str = "obstacle"


class CollisionChecker:
    """
    Collision detection for robot workspace.

    Checks end-effector position against:
    - Workspace boundaries
    - Static obstacles (bounding boxes, spheres)
    - Self-collision (simplified)
    """

    def __init__(
        self,
        workspace_min: np.ndarray,
        workspace_max: np.ndarray
    ):
        """
        Initialize collision checker.

        Args:
            workspace_min: Minimum workspace bounds [x, y, z] (mm)
            workspace_max: Maximum workspace bounds [x, y, z] (mm)
        """
        self.workspace_min = workspace_min
        self.workspace_max = workspace_max
        self.obstacles_boxes: List[BoundingBox] = []
        self.obstacles_spheres: List[Sphere] = []

    def add_box_obstacle(self, obstacle: BoundingBox) -> None:
        """Add a bounding box obstacle."""
        self.obstacles_boxes.append(obstacle)

    def add_sphere_obstacle(self, obstacle: Sphere) -> None:
        """Add a sphere obstacle."""
        self.obstacles_spheres.append(obstacle)

    def clear_obstacles(self) -> None:
        """Remove all obstacles."""
        self.obstacles_boxes.clear()
        self.obstacles_spheres.clear()

    def check_position(
        self,
        position: np.ndarray,
        tool_radius: float = 50.0
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if position is collision-free.

        Args:
            position: End-effector position [x, y, z] (mm)
            tool_radius: Tool collision sphere radius (mm)

        Returns:
            Tuple of (is_safe, collision_description)
        """
        # Check workspace bounds
        if np.any(position < self.workspace_min + tool_radius):
            violated = ["x", "y", "z"][np.argmin(position - self.workspace_min)]
            return False, f"Workspace minimum violated ({violated})"

        if np.any(position > self.workspace_max - tool_radius):
            violated = ["x", "y", "z"][np.argmax(position - self.workspace_max)]
            return False, f"Workspace maximum violated ({violated})"

        # Check box obstacles
        for box in self.obstacles_boxes:
            if self._check_sphere_box_collision(position, tool_radius, box):
                return False, f"Collision with {box.name}"

        # Check sphere obstacles
        for sphere in self.obstacles_spheres:
            distance = np.linalg.norm(position - sphere.center)
            if distance < tool_radius + sphere.radius:
                return False, f"Collision with {sphere.name}"

        return True, None

    def check_trajectory(
        self,
        positions: List[np.ndarray],
        tool_radius: float = 50.0
    ) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Check if entire trajectory is collision-free.

        Args:
            positions: List of positions along trajectory
            tool_radius: Tool collision sphere radius

        Returns:
            Tuple of (is_safe, collision_index, description)
        """
        for i, pos in enumerate(positions):
            is_safe, description = self.check_position(pos, tool_radius)
            if not is_safe:
                return False, i, description

        return True, None, None

    def _check_sphere_box_collision(
        self,
        sphere_center: np.ndarray,
        sphere_radius: float,
        box: BoundingBox
    ) -> bool:
        """Check collision between sphere and axis-aligned box."""
        # Find closest point on box to sphere center
        closest = np.clip(sphere_center, box.min_point, box.max_point)

        # Check distance to closest point
        distance = np.linalg.norm(sphere_center - closest)
        return distance < sphere_radius

    def get_distance_to_boundary(self, position: np.ndarray) -> float:
        """Get minimum distance to workspace boundary."""
        dist_min = np.min(position - self.workspace_min)
        dist_max = np.min(self.workspace_max - position)
        return min(dist_min, dist_max)
