"""
Action Chunking Transformer (ACT) Model

Transformer-based policy that predicts action sequences (chunks).
Based on the ACT paper: https://arxiv.org/abs/2304.13705
"""

from typing import Dict, Any, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

from .base_model import BasePolicy
from .vision_encoder import VisionEncoder


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for transformer."""

    def __init__(self, d_model: int, max_len: int = 100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]


class ACTPolicy(BasePolicy):
    """
    Action Chunking Transformer policy.

    Predicts sequences of actions (chunks) for temporal consistency.
    Uses a transformer encoder-decoder architecture.

    Architecture:
    - Vision encoder (ResNet) for image features
    - Transformer encoder for observation processing
    - Transformer decoder for action sequence generation
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ACT model.

        Args:
            config: Model configuration
                - action_dim: Action dimension
                - chunk_size: Number of actions to predict
                - hidden_dim: Transformer hidden dimension
                - num_heads: Number of attention heads
                - num_encoder_layers: Encoder layers
                - num_decoder_layers: Decoder layers
        """
        super().__init__(config)

        self.chunk_size = config.get("chunk_size", 10)
        self.hidden_dim = config.get("hidden_dim", 256)
        self.num_heads = config.get("num_heads", 8)
        self.num_encoder_layers = config.get("num_encoder_layers", 4)
        self.num_decoder_layers = config.get("num_decoder_layers", 4)
        self.num_cameras = config.get("num_cameras", 3)
        self.joint_dim = config.get("joint_dim", 6)

        # Vision encoder
        self.vision_encoder = VisionEncoder(
            output_dim=self.hidden_dim,
            pretrained=config.get("pretrained_vision", True)
        )

        # State encoder
        self.state_encoder = nn.Linear(self.joint_dim, self.hidden_dim)

        # Positional encoding
        self.pos_encoder = PositionalEncoding(self.hidden_dim)

        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.hidden_dim,
            nhead=self.num_heads,
            dim_feedforward=self.hidden_dim * 4,
            dropout=0.1,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=self.num_encoder_layers
        )

        # Transformer decoder
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=self.hidden_dim,
            nhead=self.num_heads,
            dim_feedforward=self.hidden_dim * 4,
            dropout=0.1,
            batch_first=True
        )
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=self.num_decoder_layers
        )

        # Action queries (learnable)
        self.action_queries = nn.Parameter(
            torch.randn(1, self.chunk_size, self.hidden_dim)
        )

        # Action head
        self.action_head = nn.Linear(self.hidden_dim, self.action_dim)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass.

        Args:
            observations: Dictionary with "image" and "joint_state"

        Returns:
            Predicted action sequence [B, chunk_size, action_dim]
        """
        batch_size = observations["joint_state"].shape[0]
        tokens = []

        # Encode images
        if "image" in observations:
            images = observations["image"]  # [B, num_cameras, C, H, W]
            for i in range(min(self.num_cameras, images.shape[1])):
                cam_features = self.vision_encoder(images[:, i])  # [B, hidden_dim]
                tokens.append(cam_features.unsqueeze(1))

        # Encode joint state
        state_features = self.state_encoder(observations["joint_state"])  # [B, hidden_dim]
        tokens.append(state_features.unsqueeze(1))

        # Concatenate tokens [B, num_tokens, hidden_dim]
        encoder_input = torch.cat(tokens, dim=1)
        encoder_input = self.pos_encoder(encoder_input)

        # Transformer encoder
        memory = self.transformer_encoder(encoder_input)

        # Prepare action queries [B, chunk_size, hidden_dim]
        queries = self.action_queries.expand(batch_size, -1, -1)
        queries = self.pos_encoder(queries)

        # Transformer decoder
        decoder_output = self.transformer_decoder(queries, memory)

        # Predict actions
        actions = self.action_head(decoder_output)  # [B, chunk_size, action_dim]

        return actions

    def predict(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Predict actions (numpy interface).

        Returns first action from the predicted chunk.

        Args:
            observations: Dictionary of numpy arrays

        Returns:
            First predicted action [action_dim]
        """
        self.eval()
        with torch.no_grad():
            tensor_obs = {}
            for key, value in observations.items():
                tensor_obs[key] = torch.from_numpy(value).float().unsqueeze(0)
                if next(self.parameters()).is_cuda:
                    tensor_obs[key] = tensor_obs[key].cuda()

            action_chunk = self.forward(tensor_obs)
            # Return first action in chunk
            return action_chunk[0, 0].cpu().numpy()

    def predict_chunk(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Predict full action chunk.

        Args:
            observations: Dictionary of numpy arrays

        Returns:
            Action chunk [chunk_size, action_dim]
        """
        self.eval()
        with torch.no_grad():
            tensor_obs = {}
            for key, value in observations.items():
                tensor_obs[key] = torch.from_numpy(value).float().unsqueeze(0)
                if next(self.parameters()).is_cuda:
                    tensor_obs[key] = tensor_obs[key].cuda()

            action_chunk = self.forward(tensor_obs)
            return action_chunk[0].cpu().numpy()

    def compute_loss(
        self,
        observations: Dict[str, torch.Tensor],
        actions: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute loss for action chunk prediction.

        Args:
            observations: Input observations
            actions: Ground truth action sequence [B, chunk_size, action_dim]

        Returns:
            Scalar loss tensor
        """
        predicted = self.forward(observations)
        return F.mse_loss(predicted, actions)
