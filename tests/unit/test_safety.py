"""Unit tests for safety module."""
import pytest
import numpy as np
from src.safety.safety_monitor import SafetyMonitor, SafetyLimits, SafetyState
from src.safety.limit_checker import LimitChecker, JointLimits

class TestSafetyMonitor:
    @pytest.fixture
    def safety_limits(self):
        return SafetyLimits(
            joint_min=np.array([-3.14, -2.09, -2.18, -6.28, -2.09, -6.28]),
            joint_max=np.array([3.14, 2.09, 2.18, 6.28, 2.09, 6.28]),
            velocity_max=np.array([1.96, 1.57, 1.96, 3.49, 3.49, 5.24]),
            acceleration_max=np.array([8.0, 6.0, 8.0, 12.0, 12.0, 16.0]),
            torque_max=np.array([1000, 1000, 500, 300, 300, 100]),
        )

    def test_valid_command(self, safety_limits):
        monitor = SafetyMonitor(safety_limits)
        valid_pos = np.zeros(6)
        is_valid, violations = monitor.validate_command(valid_pos)
        assert is_valid
        assert len(violations) == 0

    def test_invalid_position(self, safety_limits):
        monitor = SafetyMonitor(safety_limits)
        invalid_pos = np.array([5.0, 0, 0, 0, 0, 0])  # Exceeds limit
        is_valid, violations = monitor.validate_command(invalid_pos)
        assert not is_valid
        assert len(violations) > 0

    def test_estop_trigger(self, safety_limits):
        monitor = SafetyMonitor(safety_limits)
        monitor.trigger_estop("Test")
        assert monitor.state == SafetyState.ESTOP

class TestLimitChecker:
    @pytest.fixture
    def joint_limits(self):
        return [
            JointLimits(-3.14, 3.14, 2.0, 8.0, 1000),
            JointLimits(-2.09, 2.09, 1.5, 6.0, 1000),
            JointLimits(-2.18, 2.18, 2.0, 8.0, 500),
            JointLimits(-6.28, 6.28, 3.5, 12.0, 300),
            JointLimits(-2.09, 2.09, 3.5, 12.0, 300),
            JointLimits(-6.28, 6.28, 5.0, 16.0, 100),
        ]

    def test_valid_position(self, joint_limits):
        checker = LimitChecker(joint_limits)
        is_valid, error = checker.check_position(np.zeros(6))
        assert is_valid
        assert error is None

    def test_clamp_position(self, joint_limits):
        checker = LimitChecker(joint_limits)
        out_of_range = np.array([10.0, 10.0, 10.0, 10.0, 10.0, 10.0])
        clamped = checker.clamp_position(out_of_range)
        assert np.all(clamped <= checker.pos_max)
