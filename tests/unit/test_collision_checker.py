"""
Tests for Collision Checker
"""

import pytest
import numpy as np
from src.safety.collision_checker import CollisionChecker, BoundingBox, Sphere


class TestCollisionChecker:
    """Test collision detection."""

    @pytest.fixture
    def checker(self):
        """Create collision checker with standard workspace."""
        return CollisionChecker(
            workspace_min=np.array([-1000.0, -1000.0, 0.0]),
            workspace_max=np.array([1000.0, 1000.0, 2000.0])
        )

    def test_init(self, checker):
        """Test initialization."""
        np.testing.assert_array_equal(
            checker.workspace_min,
            np.array([-1000.0, -1000.0, 0.0])
        )
        np.testing.assert_array_equal(
            checker.workspace_max,
            np.array([1000.0, 1000.0, 2000.0])
        )
        assert len(checker.obstacles_boxes) == 0
        assert len(checker.obstacles_spheres) == 0

    def test_add_box_obstacle(self, checker):
        """Test adding box obstacle."""
        box = BoundingBox(
            min_point=np.array([0.0, 0.0, 0.0]),
            max_point=np.array([100.0, 100.0, 100.0]),
            name="test_box"
        )

        checker.add_box_obstacle(box)

        assert len(checker.obstacles_boxes) == 1
        assert checker.obstacles_boxes[0] == box

    def test_add_sphere_obstacle(self, checker):
        """Test adding sphere obstacle."""
        sphere = Sphere(
            center=np.array([500.0, 500.0, 1000.0]),
            radius=100.0,
            name="test_sphere"
        )

        checker.add_sphere_obstacle(sphere)

        assert len(checker.obstacles_spheres) == 1
        assert checker.obstacles_spheres[0] == sphere

    def test_clear_obstacles(self, checker):
        """Test clearing all obstacles."""
        checker.add_box_obstacle(BoundingBox(np.zeros(3), np.ones(3)))
        checker.add_sphere_obstacle(Sphere(np.zeros(3), 50.0))

        checker.clear_obstacles()

        assert len(checker.obstacles_boxes) == 0
        assert len(checker.obstacles_spheres) == 0

    def test_check_position_safe(self, checker):
        """Test checking a safe position."""
        position = np.array([0.0, 0.0, 1000.0])  # Center of workspace

        is_safe, description = checker.check_position(position)

        assert is_safe
        assert description is None

    def test_check_position_min_boundary_violation(self, checker):
        """Test workspace minimum boundary violation."""
        position = np.array([-1100.0, 0.0, 1000.0])  # Beyond min x

        is_safe, description = checker.check_position(position, tool_radius=50.0)

        assert not is_safe
        assert "minimum" in description.lower()

    def test_check_position_max_boundary_violation(self, checker):
        """Test workspace maximum boundary violation."""
        position = np.array([0.0, 0.0, 2100.0])  # Beyond max z

        is_safe, description = checker.check_position(position, tool_radius=50.0)

        assert not is_safe
        assert "maximum" in description.lower()

    def test_check_position_box_collision(self, checker):
        """Test collision with box obstacle."""
        box = BoundingBox(
            min_point=np.array([400.0, 400.0, 900.0]),
            max_point=np.array([600.0, 600.0, 1100.0]),
            name="test_box"
        )
        checker.add_box_obstacle(box)

        # Position inside box
        position = np.array([500.0, 500.0, 1000.0])

        is_safe, description = checker.check_position(position, tool_radius=10.0)

        assert not is_safe
        assert "test_box" in description

    def test_check_position_sphere_collision(self, checker):
        """Test collision with sphere obstacle."""
        sphere = Sphere(
            center=np.array([0.0, 0.0, 1000.0]),
            radius=200.0,
            name="test_sphere"
        )
        checker.add_sphere_obstacle(sphere)

        # Position near sphere center
        position = np.array([50.0, 50.0, 1000.0])

        is_safe, description = checker.check_position(position, tool_radius=50.0)

        assert not is_safe
        assert "test_sphere" in description

    def test_check_position_near_sphere_safe(self, checker):
        """Test position near but not colliding with sphere."""
        sphere = Sphere(
            center=np.array([0.0, 0.0, 1000.0]),
            radius=100.0,
            name="test_sphere"
        )
        checker.add_sphere_obstacle(sphere)

        # Position outside sphere + tool radius
        position = np.array([300.0, 0.0, 1000.0])

        is_safe, description = checker.check_position(position, tool_radius=50.0)

        assert is_safe

    def test_check_trajectory_all_safe(self, checker):
        """Test checking a safe trajectory."""
        positions = [
            np.array([0.0, 0.0, 1000.0]),
            np.array([100.0, 0.0, 1000.0]),
            np.array([200.0, 0.0, 1000.0])
        ]

        is_safe, index, description = checker.check_trajectory(positions)

        assert is_safe
        assert index is None
        assert description is None

    def test_check_trajectory_collision(self, checker):
        """Test trajectory with collision."""
        # Add obstacle in the middle of trajectory
        box = BoundingBox(
            min_point=np.array([90.0, -50.0, 950.0]),
            max_point=np.array([110.0, 50.0, 1050.0]),
            name="obstacle"
        )
        checker.add_box_obstacle(box)

        positions = [
            np.array([0.0, 0.0, 1000.0]),    # Safe
            np.array([100.0, 0.0, 1000.0]),  # Collision
            np.array([200.0, 0.0, 1000.0])   # Safe
        ]

        is_safe, index, description = checker.check_trajectory(positions, tool_radius=10.0)

        assert not is_safe
        assert index == 1  # Second point
        assert "obstacle" in description

    def test_sphere_box_collision_detection(self, checker):
        """Test sphere-box collision algorithm."""
        box = BoundingBox(
            min_point=np.array([0.0, 0.0, 0.0]),
            max_point=np.array([100.0, 100.0, 100.0])
        )

        # Sphere center inside box
        assert checker._check_sphere_box_collision(
            np.array([50.0, 50.0, 50.0]),
            10.0,
            box
        )

        # Sphere touching box edge
        assert checker._check_sphere_box_collision(
            np.array([110.0, 50.0, 50.0]),
            15.0,  # radius reaches box
            box
        )

        # Sphere far from box
        assert not checker._check_sphere_box_collision(
            np.array([200.0, 200.0, 200.0]),
            10.0,
            box
        )

    def test_get_distance_to_boundary(self, checker):
        """Test distance to workspace boundary."""
        # Center of workspace
        position = np.array([0.0, 0.0, 1000.0])
        distance = checker.get_distance_to_boundary(position)

        # Should be 1000mm to nearest boundary (min x, min y, or max x, max y)
        assert distance == 1000.0

    def test_tool_radius_consideration(self, checker):
        """Test that tool radius is considered in checks."""
        # Position near workspace boundary
        position = np.array([950.0, 0.0, 1000.0])  # 50mm from max x

        # With large tool radius (100mm), should collide (50 < 100)
        is_safe_large, _ = checker.check_position(position, tool_radius=100.0)
        assert not is_safe_large

        # With small tool radius (30mm), should be safe (50 > 30)
        is_safe_small, _ = checker.check_position(position, tool_radius=30.0)
        assert is_safe_small

    def test_multiple_obstacles(self, checker):
        """Test with multiple obstacles."""
        # Add multiple obstacles
        checker.add_box_obstacle(BoundingBox(
            np.array([100.0, 100.0, 900.0]),
            np.array([200.0, 200.0, 1000.0]),
            "box1"
        ))
        checker.add_box_obstacle(BoundingBox(
            np.array([-200.0, -200.0, 900.0]),
            np.array([-100.0, -100.0, 1000.0]),
            "box2"
        ))
        checker.add_sphere_obstacle(Sphere(
            np.array([0.0, 500.0, 1000.0]),
            100.0,
            "sphere1"
        ))

        # Check collisions with different obstacles
        pos1 = np.array([150.0, 150.0, 950.0])
        is_safe1, desc1 = checker.check_position(pos1, 10.0)
        assert not is_safe1
        assert "box1" in desc1

        pos2 = np.array([0.0, 500.0, 1000.0])
        is_safe2, desc2 = checker.check_position(pos2, 10.0)
        assert not is_safe2
        assert "sphere1" in desc2
