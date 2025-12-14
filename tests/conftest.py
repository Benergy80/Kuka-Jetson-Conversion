"""Pytest configuration and fixtures."""
import pytest
import numpy as np
import torch

@pytest.fixture
def sample_joint_positions():
    """Sample joint positions."""
    return np.array([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])

@pytest.fixture
def sample_observation():
    """Sample observation dictionary."""
    return {
        "joint_state": np.random.randn(6).astype(np.float32),
        "image": np.random.randint(0, 255, (3, 3, 224, 224), dtype=np.uint8),
    }

@pytest.fixture
def device():
    """Get available device."""
    return "cuda" if torch.cuda.is_available() else "cpu"
