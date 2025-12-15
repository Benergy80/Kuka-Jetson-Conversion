"""
Tests for PID Controller
"""

import pytest
import numpy as np
from src.control.pid_controller import PIDController, PIDGains, MultiJointPIDController


class TestPIDController:
    """Test PID controller functionality."""

    @pytest.fixture
    def gains(self):
        """Standard PID gains for testing."""
        return PIDGains(
            kp=10.0,
            ki=1.0,
            kd=0.5,
            kff_vel=0.1,
            kff_acc=0.01,
            integral_limit=50.0,
            output_limit=100.0
        )

    @pytest.fixture
    def controller(self, gains):
        """Create PID controller instance."""
        return PIDController(gains)

    def test_init(self, controller, gains):
        """Test initialization."""
        assert controller.gains == gains
        assert controller._integral == 0.0
        assert controller._prev_error == 0.0
        assert controller._prev_time is None

    def test_reset(self, controller):
        """Test controller reset."""
        # Run controller to set internal state
        controller.compute(1.0, 0.0, 0.01)
        assert controller._integral != 0.0
        assert controller._prev_error != 0.0

        # Reset and verify
        controller.reset()
        assert controller._integral == 0.0
        assert controller._prev_error == 0.0
        assert controller._prev_time is None

    def test_proportional_only(self):
        """Test proportional-only control."""
        gains = PIDGains(kp=2.0, ki=0.0, kd=0.0)
        controller = PIDController(gains)

        output = controller.compute(target=1.0, actual=0.5, dt=0.01)
        expected = 2.0 * (1.0 - 0.5)  # kp * error
        assert abs(output - expected) < 1e-6

    def test_integral_accumulation(self, controller):
        """Test integral term accumulation."""
        # Run multiple steps with constant error
        for _ in range(10):
            output = controller.compute(target=1.0, actual=0.0, dt=0.01)

        # Integral should have accumulated
        assert controller._integral > 0.0
        assert abs(controller._integral - 10 * 0.01) < 1e-6  # 10 steps * dt

    def test_integral_anti_windup(self):
        """Test integral anti-windup limiting."""
        gains = PIDGains(kp=1.0, ki=10.0, kd=0.0, integral_limit=5.0)
        controller = PIDController(gains)

        # Run many steps to saturate integral
        for _ in range(100):
            controller.compute(target=10.0, actual=0.0, dt=0.01)

        # Integral should be clamped
        assert controller._integral <= gains.integral_limit

    def test_derivative_term(self, controller):
        """Test derivative term computation."""
        # First step
        controller.compute(target=1.0, actual=0.0, dt=0.01)

        # Second step with changed error
        output = controller.compute(target=1.0, actual=0.5, dt=0.01)

        # D term should be active (error decreased)
        assert controller._prev_error != 0.0

    def test_feedforward_velocity(self):
        """Test velocity feedforward."""
        gains = PIDGains(kp=0.0, ki=0.0, kd=0.0, kff_vel=2.0)
        controller = PIDController(gains)

        output = controller.compute(
            target=0.0,
            actual=0.0,
            dt=0.01,
            target_velocity=5.0
        )

        expected = 2.0 * 5.0  # kff_vel * target_vel
        assert abs(output - expected) < 1e-6

    def test_feedforward_acceleration(self):
        """Test acceleration feedforward."""
        gains = PIDGains(kp=0.0, ki=0.0, kd=0.0, kff_acc=0.5)
        controller = PIDController(gains)

        output = controller.compute(
            target=0.0,
            actual=0.0,
            dt=0.01,
            target_acceleration=10.0
        )

        expected = 0.5 * 10.0  # kff_acc * target_acc
        assert abs(output - expected) < 1e-6

    def test_output_saturation(self):
        """Test output limiting."""
        gains = PIDGains(kp=100.0, ki=0.0, kd=0.0, output_limit=50.0)
        controller = PIDController(gains)

        output = controller.compute(target=10.0, actual=0.0, dt=0.01)

        # Output should be saturated at limit
        assert output == gains.output_limit

    def test_negative_output_saturation(self):
        """Test negative output limiting."""
        gains = PIDGains(kp=100.0, ki=0.0, kd=0.0, output_limit=50.0)
        controller = PIDController(gains)

        output = controller.compute(target=0.0, actual=10.0, dt=0.01)

        # Output should be saturated at negative limit
        assert output == -gains.output_limit

    def test_zero_dt_handling(self, controller):
        """Test behavior with zero time step."""
        output = controller.compute(target=1.0, actual=0.0, dt=0.0)
        # Should not crash and derivative should be 0
        assert not np.isnan(output)
        assert not np.isinf(output)


class TestMultiJointPIDController:
    """Test multi-joint PID controller."""

    @pytest.fixture
    def gains_list(self):
        """Create gains for 3 joints."""
        return [
            PIDGains(kp=10.0, ki=1.0, kd=0.5),
            PIDGains(kp=20.0, ki=2.0, kd=1.0),
            PIDGains(kp=15.0, ki=1.5, kd=0.75)
        ]

    @pytest.fixture
    def multi_controller(self, gains_list):
        """Create multi-joint controller."""
        return MultiJointPIDController(gains_list)

    def test_init(self, multi_controller, gains_list):
        """Test initialization."""
        assert multi_controller.num_joints == len(gains_list)
        assert len(multi_controller.controllers) == len(gains_list)

    def test_reset_all(self, multi_controller):
        """Test resetting all controllers."""
        # Run controllers
        targets = np.array([1.0, 2.0, 3.0])
        actuals = np.zeros(3)
        multi_controller.compute(targets, actuals, 0.01)

        # Reset all
        multi_controller.reset()

        # Verify all are reset
        for controller in multi_controller.controllers:
            assert controller._integral == 0.0
            assert controller._prev_error == 0.0

    def test_compute_all_joints(self, multi_controller):
        """Test computing control for all joints."""
        targets = np.array([1.0, 2.0, 3.0])
        actuals = np.array([0.5, 1.5, 2.5])
        outputs = multi_controller.compute(targets, actuals, 0.01)

        assert outputs.shape == (3,)
        assert np.all(outputs > 0)  # All errors are positive

    def test_with_feedforward(self, multi_controller):
        """Test with velocity and acceleration feedforward."""
        targets = np.zeros(3)
        actuals = np.zeros(3)
        velocities = np.array([1.0, 2.0, 3.0])
        accelerations = np.array([0.5, 1.0, 1.5])

        outputs = multi_controller.compute(
            targets,
            actuals,
            0.01,
            target_velocities=velocities,
            target_accelerations=accelerations
        )

        assert outputs.shape == (3,)

    def test_default_feedforward(self, multi_controller):
        """Test default None feedforward values."""
        targets = np.array([1.0, 2.0, 3.0])
        actuals = np.zeros(3)

        # Should not crash with None feedforward
        outputs = multi_controller.compute(targets, actuals, 0.01)
        assert outputs.shape == (3,)

    def test_independent_joint_control(self, multi_controller):
        """Test that joints are controlled independently."""
        # Only joint 1 has error
        targets = np.array([0.0, 1.0, 0.0])
        actuals = np.zeros(3)

        outputs = multi_controller.compute(targets, actuals, 0.01)

        # Only joint 1 should have non-zero output (mostly)
        assert outputs[1] > 0
        # Joints 0 and 2 should have minimal output
        assert abs(outputs[0]) < 1e-10
        assert abs(outputs[2]) < 1e-10
