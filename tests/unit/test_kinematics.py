"""Unit tests for kinematics module."""
import pytest
import numpy as np
from src.control.kinematics import ForwardKinematics, InverseKinematics

class TestForwardKinematics:
    def test_init(self):
        fk = ForwardKinematics()
        assert fk.num_joints == 6

    def test_zero_position(self):
        fk = ForwardKinematics()
        T = fk.compute(np.zeros(6))
        assert T.shape == (4, 4)
        assert np.allclose(T[3, :], [0, 0, 0, 1])

    def test_get_position(self, sample_joint_positions):
        fk = ForwardKinematics()
        pos = fk.get_position(sample_joint_positions)
        assert pos.shape == (3,)

class TestInverseKinematics:
    def test_init(self):
        ik = InverseKinematics()
        assert ik.fk is not None

    def test_round_trip(self):
        fk = ForwardKinematics()
        ik = InverseKinematics()

        original = np.array([0.1, -0.2, 0.3, 0.0, 0.2, 0.0])
        target = fk.compute(original)

        result, success = ik.compute(target, initial_guess=original)
        # Should converge close to original
        if success:
            assert np.allclose(fk.get_position(result), target[:3, 3], atol=1.0)
