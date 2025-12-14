"""
Base Policy Model

Abstract base class for all policy models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import torch
import torch.nn as nn
import numpy as np


class BasePolicy(nn.Module, ABC):
    """
    Abstract base class for robot control policies.

    All policy models should inherit from this class and implement
    the required methods for training and inference.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize base policy.

        Args:
            config: Model configuration dictionary
        """
        super().__init__()
        self.config = config
        self.action_dim = config.get("action_dim", 6)
        self.observation_dim = config.get("observation_dim", 512)

    @abstractmethod
    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass of the model.

        Args:
            observations: Dictionary containing observation tensors
                - "image": Camera images [B, C, H, W]
                - "joint_state": Joint positions [B, num_joints]
                - "force_torque": Force/torque readings [B, 6]

        Returns:
            Predicted actions [B, action_dim] or [B, chunk_size, action_dim]
        """
        pass

    @abstractmethod
    def predict(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Predict actions for deployment (numpy interface).

        Args:
            observations: Dictionary of numpy arrays

        Returns:
            Predicted actions as numpy array
        """
        pass

    @abstractmethod
    def compute_loss(
        self,
        observations: Dict[str, torch.Tensor],
        actions: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute training loss.

        Args:
            observations: Input observations
            actions: Ground truth actions

        Returns:
            Scalar loss tensor
        """
        pass

    def save(self, path: str) -> None:
        """Save model checkpoint."""
        torch.save({
            "config": self.config,
            "state_dict": self.state_dict(),
        }, path)

    @classmethod
    def load(cls, path: str, device: str = "cuda") -> "BasePolicy":
        """Load model from checkpoint."""
        checkpoint = torch.load(path, map_location=device)
        model = cls(checkpoint["config"])
        model.load_state_dict(checkpoint["state_dict"])
        model.to(device)
        return model

    def get_num_params(self) -> int:
        """Get total number of parameters."""
        return sum(p.numel() for p in self.parameters())

    def get_trainable_params(self) -> int:
        """Get number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
