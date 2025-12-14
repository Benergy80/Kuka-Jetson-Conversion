"""Domain Randomization for Sim-to-Real Transfer"""
import numpy as np
from typing import Dict

class DomainRandomizer:
    """Applies domain randomization for sim-to-real transfer."""

    def __init__(self, config: Dict = None):
        self.config = config or {
            "mass_range": (0.8, 1.2),
            "friction_range": (0.5, 1.5),
            "camera_noise_std": 0.02,
            "joint_noise_std": 0.01,
        }

    def randomize_dynamics(self, simulator) -> Dict:
        """Randomize physical parameters."""
        params = {}
        params["mass_scale"] = np.random.uniform(*self.config["mass_range"])
        params["friction_scale"] = np.random.uniform(*self.config["friction_range"])
        # Apply to simulator...
        return params

    def randomize_observation(self, obs: Dict) -> Dict:
        """Add noise to observations."""
        randomized = {}
        for key, value in obs.items():
            if "image" in key:
                noise = np.random.normal(0, self.config["camera_noise_std"], value.shape)
                randomized[key] = np.clip(value + noise * 255, 0, 255).astype(np.uint8)
            elif "joint" in key:
                noise = np.random.normal(0, self.config["joint_noise_std"], value.shape)
                randomized[key] = value + noise
            else:
                randomized[key] = value
        return randomized
