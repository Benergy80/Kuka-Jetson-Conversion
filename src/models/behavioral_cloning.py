"""
Behavioral Cloning Model

Simple imitation learning model that directly predicts actions from observations.
"""

from typing import Dict, Any
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from .base_model import BasePolicy
from .vision_encoder import VisionEncoder


class BehavioralCloning(BasePolicy):
    """
    Behavioral Cloning policy.

    Architecture:
    - Vision encoder (ResNet-18) for image features
    - MLP for state features
    - Combined MLP for action prediction
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize BC model.

        Args:
            config: Model configuration
                - action_dim: Number of action dimensions
                - hidden_dim: Hidden layer size
                - use_vision: Whether to use camera images
                - num_cameras: Number of cameras
        """
        super().__init__(config)

        self.use_vision = config.get("use_vision", True)
        self.hidden_dim = config.get("hidden_dim", 256)
        self.num_cameras = config.get("num_cameras", 3)
        self.joint_dim = config.get("joint_dim", 6)

        # Vision encoder
        if self.use_vision:
            self.vision_encoder = VisionEncoder(
                output_dim=self.hidden_dim,
                pretrained=config.get("pretrained_vision", True)
            )
            vision_features = self.hidden_dim * self.num_cameras
        else:
            vision_features = 0

        # State encoder
        self.state_encoder = nn.Sequential(
            nn.Linear(self.joint_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU(),
        )

        # Combined policy network
        combined_dim = vision_features + self.hidden_dim
        self.policy_net = nn.Sequential(
            nn.Linear(combined_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.action_dim),
        )

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass.

        Args:
            observations: Dictionary with "image" and "joint_state" tensors

        Returns:
            Predicted actions [B, action_dim]
        """
        features = []

        # Encode images
        if self.use_vision and "image" in observations:
            images = observations["image"]  # [B, num_cameras, C, H, W]
            batch_size = images.shape[0]

            # Process each camera
            for i in range(self.num_cameras):
                cam_features = self.vision_encoder(images[:, i])
                features.append(cam_features)

        # Encode joint state
        if "joint_state" in observations:
            state_features = self.state_encoder(observations["joint_state"])
            features.append(state_features)

        # Concatenate and predict
        combined = torch.cat(features, dim=-1)
        actions = self.policy_net(combined)

        return actions

    def predict(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Predict actions (numpy interface for deployment).

        Args:
            observations: Dictionary of numpy observation arrays

        Returns:
            Predicted actions as numpy array
        """
        self.eval()
        with torch.no_grad():
            # Convert to tensors
            tensor_obs = {}
            for key, value in observations.items():
                tensor_obs[key] = torch.from_numpy(value).float().unsqueeze(0)
                if next(self.parameters()).is_cuda:
                    tensor_obs[key] = tensor_obs[key].cuda()

            # Forward pass
            actions = self.forward(tensor_obs)

            return actions.squeeze(0).cpu().numpy()

    def compute_loss(
        self,
        observations: Dict[str, torch.Tensor],
        actions: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute MSE loss between predicted and target actions.

        Args:
            observations: Input observations
            actions: Ground truth actions [B, action_dim]

        Returns:
            Scalar loss tensor
        """
        predicted = self.forward(observations)
        return F.mse_loss(predicted, actions)
