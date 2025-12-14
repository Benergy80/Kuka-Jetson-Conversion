"""Data Augmentation"""
import numpy as np
from typing import Dict, Tuple

class DataAugmentation:
    """Data augmentation for robot demonstrations."""

    def __init__(self, config: Dict = None):
        self.config = config or {}

    def augment_image(self, image: np.ndarray) -> np.ndarray:
        """Apply augmentations to image."""
        if self.config.get("random_brightness", False):
            factor = np.random.uniform(0.8, 1.2)
            image = np.clip(image * factor, 0, 255).astype(np.uint8)
        if self.config.get("random_crop", False):
            # Implement random crop
            pass
        return image

    def augment_trajectory(self, actions: np.ndarray) -> np.ndarray:
        """Apply augmentations to trajectory."""
        if self.config.get("add_noise", False):
            noise_std = self.config.get("noise_std", 0.01)
            actions = actions + np.random.normal(0, noise_std, actions.shape)
        return actions

    def __call__(self, obs: Dict[str, np.ndarray], actions: np.ndarray) -> Tuple:
        """Apply all augmentations."""
        aug_obs = {}
        for key, value in obs.items():
            if "image" in key:
                aug_obs[key] = self.augment_image(value)
            else:
                aug_obs[key] = value
        aug_actions = self.augment_trajectory(actions)
        return aug_obs, aug_actions
