"""
Tests for Trajectory Planner
"""

import pytest
import numpy as np
from src.control.trajectory_planner import (
    TrajectoryPlanner,
    TrajectoryLimits,
    TrajectoryPoint
)


class TestTrajectoryPlanner:
    """Test trajectory planner functionality."""

    @pytest.fixture
    def limits(self):
        """Standard trajectory limits."""
        return TrajectoryLimits(
            max_velocity=np.array([2.0, 2.0, 2.0, 3.0, 3.0, 3.0]),
            max_acceleration=np.array([5.0, 5.0, 5.0, 10.0, 10.0, 10.0])
        )

    @pytest.fixture
    def planner(self, limits):
        """Create planner instance."""
        return TrajectoryPlanner(limits, num_joints=6)

    def test_init(self, planner, limits):
        """Test initialization."""
        assert planner.limits == limits
        assert planner.num_joints == 6

    def test_point_to_point_basic(self, planner):
        """Test basic point-to-point planning."""
        start = np.zeros(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        assert len(trajectory) > 0
        assert isinstance(trajectory[0], TrajectoryPoint)

        # First point should be start
        np.testing.assert_array_almost_equal(trajectory[0].position, start)

        # Last point should be end
        np.testing.assert_array_almost_equal(trajectory[-1].position, end, decimal=2)

    def test_point_to_point_with_duration(self, planner):
        """Test point-to-point with specified duration."""
        start = np.zeros(6)
        end = np.ones(6)
        duration = 2.0  # 2 seconds

        trajectory = planner.plan_point_to_point(start, end, duration=duration)

        # Check duration is approximately correct
        assert abs(trajectory[-1].time - duration) < 0.01

    def test_trajectory_continuity(self, planner):
        """Test that trajectory is continuous."""
        start = np.zeros(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        # Check position continuity
        for i in range(1, len(trajectory)):
            # Check small time increment
            dt = trajectory[i].time - trajectory[i-1].time
            assert 0.0005 < dt < 0.0015  # Around 1ms ± tolerance

    def test_smooth_velocity_profile(self, planner):
        """Test that velocity profile is smooth (S-curve)."""
        start = np.zeros(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        # First point velocity should be zero
        np.testing.assert_array_almost_equal(trajectory[0].velocity, np.zeros(6), decimal=2)

        # Last point velocity should be zero
        np.testing.assert_array_almost_equal(trajectory[-1].velocity, np.zeros(6), decimal=1)

        # Middle should have non-zero velocity
        mid = len(trajectory) // 2
        assert np.any(trajectory[mid].velocity != 0)

    def test_smooth_acceleration_profile(self, planner):
        """Test that acceleration profile is smooth."""
        start = np.zeros(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        # First and last accelerations should be zero
        np.testing.assert_array_almost_equal(trajectory[0].acceleration, np.zeros(6), decimal=1)
        np.testing.assert_array_almost_equal(trajectory[-1].acceleration, np.zeros(6), decimal=1)

    def test_waypoints_two_points(self, planner):
        """Test waypoint planning with two points."""
        waypoints = [
            np.zeros(6),
            np.ones(6)
        ]

        trajectory = planner.plan_waypoints(waypoints)

        assert len(trajectory) > 0
        # Should start at first waypoint
        np.testing.assert_array_almost_equal(trajectory[0].position, waypoints[0])
        # Should end at last waypoint
        np.testing.assert_array_almost_equal(trajectory[-1].position, waypoints[1], decimal=2)

    def test_waypoints_multiple_points(self, planner):
        """Test waypoint planning with multiple points."""
        waypoints = [
            np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        ]

        trajectory = planner.plan_waypoints(waypoints)

        assert len(trajectory) > 0
        # Check endpoints
        np.testing.assert_array_almost_equal(trajectory[0].position, waypoints[0])
        np.testing.assert_array_almost_equal(trajectory[-1].position, waypoints[-1], decimal=2)

    def test_waypoints_with_durations(self, planner):
        """Test waypoint planning with specified segment durations."""
        waypoints = [
            np.zeros(6),
            np.ones(6),
            np.ones(6) * 2
        ]
        durations = [1.0, 1.5]  # 1s for first segment, 1.5s for second

        trajectory = planner.plan_waypoints(waypoints, segment_durations=durations)

        assert len(trajectory) > 0
        # Total duration should be approximately sum of durations
        assert abs(trajectory[-1].time - sum(durations)) < 0.1

    def test_waypoints_insufficient_raises_error(self, planner):
        """Test that insufficient waypoints raises error."""
        with pytest.raises(ValueError, match="at least 2 waypoints"):
            planner.plan_waypoints([np.zeros(6)])

    def test_smooth_step_function(self, planner):
        """Test smooth step function properties."""
        # At t=0
        assert planner._smooth_step(0.0) == 0.0
        # At t=1
        assert abs(planner._smooth_step(1.0) - 1.0) < 1e-10
        # At t=0.5, should be around 0.5
        assert 0.4 < planner._smooth_step(0.5) < 0.6

    def test_smooth_step_derivative(self, planner):
        """Test smooth step derivative properties."""
        # At t=0 and t=1, derivative should be 0
        assert abs(planner._smooth_step_derivative(0.0)) < 1e-10
        assert abs(planner._smooth_step_derivative(1.0)) < 1e-10
        # At t=0.5, derivative should be positive and significant
        assert planner._smooth_step_derivative(0.5) > 1.0

    def test_smooth_step_second_derivative(self, planner):
        """Test smooth step second derivative properties."""
        # At t=0 and t=1, second derivative should be 0
        assert abs(planner._smooth_step_second_derivative(0.0)) < 1e-10
        assert abs(planner._smooth_step_second_derivative(1.0)) < 1e-10

    def test_different_joint_distances(self, planner):
        """Test planning with different distances per joint."""
        start = np.zeros(6)
        end = np.array([1.0, 0.5, 0.2, 1.5, 0.8, 0.3])

        trajectory = planner.plan_point_to_point(start, end)

        # Should reach all end positions
        np.testing.assert_array_almost_equal(trajectory[-1].position, end, decimal=2)

    def test_zero_distance_movement(self, planner):
        """Test planning with no movement (start == end)."""
        start = np.ones(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        # Should have minimal trajectory
        assert len(trajectory) > 0
        np.testing.assert_array_almost_equal(trajectory[0].position, start)
        np.testing.assert_array_almost_equal(trajectory[-1].position, end)

    def test_timestamp_monotonic_increase(self, planner):
        """Test that timestamps increase monotonically."""
        start = np.zeros(6)
        end = np.ones(6)

        trajectory = planner.plan_point_to_point(start, end)

        # Check timestamps are increasing
        for i in range(1, len(trajectory)):
            assert trajectory[i].time > trajectory[i-1].time

    def test_negative_movement(self, planner):
        """Test planning with negative movement."""
        start = np.ones(6)
        end = np.zeros(6)

        trajectory = planner.plan_point_to_point(start, end)

        assert len(trajectory) > 0
        np.testing.assert_array_almost_equal(trajectory[0].position, start)
        np.testing.assert_array_almost_equal(trajectory[-1].position, end, decimal=2)
