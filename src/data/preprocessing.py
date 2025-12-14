"""Data Preprocessing"""
import numpy as np
from typing import Dict, Tuple

class Preprocessor:
    """Preprocesses observations and actions for ML training."""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.obs_mean: Dict[str, np.ndarray] = {}
        self.obs_std: Dict[str, np.ndarray] = {}
        self.action_mean: np.ndarray = None
        self.action_std: np.ndarray = None

    def fit(self, observations: Dict[str, np.ndarray], actions: np.ndarray) -> None:
        """Compute normalization statistics."""
        for key, obs in observations.items():
            self.obs_mean[key] = obs.mean(axis=0)
            self.obs_std[key] = obs.std(axis=0) + 1e-8
        self.action_mean = actions.mean(axis=0)
        self.action_std = actions.std(axis=0) + 1e-8

    def normalize_obs(self, observations: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Normalize observations."""
        return {key: (obs - self.obs_mean.get(key, 0)) / self.obs_std.get(key, 1)
                for key, obs in observations.items()}

    def normalize_actions(self, actions: np.ndarray) -> np.ndarray:
        """Normalize actions."""
        if self.action_mean is None:
            return actions
        return (actions - self.action_mean) / self.action_std

    def denormalize_actions(self, actions: np.ndarray) -> np.ndarray:
        """Denormalize actions."""
        if self.action_mean is None:
            return actions
        return actions * self.action_std + self.action_mean
