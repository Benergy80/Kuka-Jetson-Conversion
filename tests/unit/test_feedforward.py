"""
Tests for Feedforward Compensator
"""

import pytest
import numpy as np
from src.control.feedforward import FeedforwardCompensator, DynamicsParams


class TestFeedforwardCompensator:
    """Test feedforward compensation."""

    @pytest.fixture
    def params(self):
        """Standard dynamics parameters."""
        return DynamicsParams(
            inertia=np.array([1.0, 2.0, 1.5, 0.5, 0.5, 0.3]),
            friction_coulomb=np.array([0.1, 0.15, 0.1, 0.05, 0.05, 0.03]),
            friction_viscous=np.array([0.01, 0.02, 0.015, 0.005, 0.005, 0.003]),
            gravity_compensation=True
        )

    @pytest.fixture
    def compensator(self, params):
        """Create compensator instance."""
        return FeedforwardCompensator(params, num_joints=6)

    def test_init(self, compensator, params):
        """Test initialization."""
        assert compensator.params == params
        assert compensator.num_joints == 6

    def test_inertia_compensation(self):
        """Test inertia compensation (τ = J * α)."""
        params = DynamicsParams(
            inertia=np.ones(6) * 2.0,
            friction_coulomb=np.zeros(6),
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = np.zeros(6)
        acceleration = np.ones(6) * 5.0  # 5 rad/s²

        torque = compensator.compute(position, velocity, acceleration)

        # τ = J * α = 2.0 * 5.0 = 10.0 for all joints
        expected = np.ones(6) * 10.0
        np.testing.assert_array_almost_equal(torque, expected)

    def test_coulomb_friction_positive_velocity(self):
        """Test Coulomb friction with positive velocity."""
        params = DynamicsParams(
            inertia=np.zeros(6),
            friction_coulomb=np.ones(6) * 0.5,
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = np.ones(6)  # Positive velocity
        acceleration = np.zeros(6)

        torque = compensator.compute(position, velocity, acceleration)

        # Coulomb friction should be +0.5 for positive velocity
        expected = np.ones(6) * 0.5
        np.testing.assert_array_almost_equal(torque, expected)

    def test_coulomb_friction_negative_velocity(self):
        """Test Coulomb friction with negative velocity."""
        params = DynamicsParams(
            inertia=np.zeros(6),
            friction_coulomb=np.ones(6) * 0.5,
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = -np.ones(6)  # Negative velocity
        acceleration = np.zeros(6)

        torque = compensator.compute(position, velocity, acceleration)

        # Coulomb friction should be -0.5 for negative velocity
        expected = -np.ones(6) * 0.5
        np.testing.assert_array_almost_equal(torque, expected)

    def test_viscous_friction(self):
        """Test viscous friction (linear with velocity)."""
        params = DynamicsParams(
            inertia=np.zeros(6),
            friction_coulomb=np.zeros(6),
            friction_viscous=np.ones(6) * 0.1,
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = np.ones(6) * 10.0
        acceleration = np.zeros(6)

        torque = compensator.compute(position, velocity, acceleration)

        # Viscous friction: τ = b * v = 0.1 * 10.0 = 1.0
        expected = np.ones(6) * 1.0
        np.testing.assert_array_almost_equal(torque, expected)

    def test_gravity_compensation_enabled(self, compensator):
        """Test gravity compensation is applied when enabled."""
        position = np.zeros(6)
        velocity = np.zeros(6)
        acceleration = np.zeros(6)

        torque = compensator.compute(position, velocity, acceleration)

        # With gravity enabled, joint 2 and 3 should have non-zero torque
        assert torque[1] != 0.0  # Joint 2
        assert torque[2] != 0.0  # Joint 3

    def test_gravity_compensation_disabled(self):
        """Test gravity compensation can be disabled."""
        params = DynamicsParams(
            inertia=np.zeros(6),
            friction_coulomb=np.zeros(6),
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = np.zeros(6)
        acceleration = np.zeros(6)

        torque = compensator.compute(position, velocity, acceleration)

        # All torques should be zero
        np.testing.assert_array_almost_equal(torque, np.zeros(6))

    def test_combined_compensation(self, compensator):
        """Test combined inertia + friction + gravity."""
        position = np.array([0.0, np.pi/4, -np.pi/4, 0.0, 0.0, 0.0])
        velocity = np.ones(6) * 2.0
        acceleration = np.ones(6) * 1.0

        torque = compensator.compute(position, velocity, acceleration)

        # Should have contributions from all components
        assert torque.shape == (6,)
        # All joints should have non-zero torque (from friction at minimum)
        assert np.all(torque != 0.0)

    def test_gravity_changes_with_position(self, compensator):
        """Test that gravity torque changes with position."""
        velocity = np.zeros(6)
        acceleration = np.zeros(6)

        # Position 1: Joint 2 at 0 rad
        pos1 = np.zeros(6)
        torque1 = compensator.compute(pos1, velocity, acceleration)

        # Position 2: Joint 2 at π/2 rad
        pos2 = np.array([0.0, np.pi/2, 0.0, 0.0, 0.0, 0.0])
        torque2 = compensator.compute(pos2, velocity, acceleration)

        # Gravity torque on joint 2 should be different
        assert torque1[1] != torque2[1]

    def test_zero_everything(self):
        """Test with all zeros."""
        params = DynamicsParams(
            inertia=np.zeros(6),
            friction_coulomb=np.zeros(6),
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        torque = compensator.compute(np.zeros(6), np.zeros(6), np.zeros(6))

        # Should get all zeros
        np.testing.assert_array_almost_equal(torque, np.zeros(6))

    def test_different_joint_parameters(self):
        """Test that different joints use different parameters."""
        params = DynamicsParams(
            inertia=np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
            friction_coulomb=np.zeros(6),
            friction_viscous=np.zeros(6),
            gravity_compensation=False
        )
        compensator = FeedforwardCompensator(params)

        position = np.zeros(6)
        velocity = np.zeros(6)
        acceleration = np.ones(6)  # Same acceleration for all

        torque = compensator.compute(position, velocity, acceleration)

        # Torques should be different due to different inertias
        expected = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        np.testing.assert_array_almost_equal(torque, expected)
