"""
Diffusion Policy Model

Generates actions through iterative denoising process.
Based on Diffusion Policy paper: https://arxiv.org/abs/2303.04137
"""

from typing import Dict, Any, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

from .base_model import BasePolicy
from .vision_encoder import VisionEncoder


class SinusoidalTimeEmbedding(nn.Module):
    """Sinusoidal embedding for diffusion timestep."""

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        device = t.device
        half_dim = self.dim // 2
        embeddings = math.log(10000) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim, device=device) * -embeddings)
        embeddings = t[:, None] * embeddings[None, :]
        embeddings = torch.cat([embeddings.sin(), embeddings.cos()], dim=-1)
        return embeddings


class DenoisingUNet(nn.Module):
    """
    U-Net style denoising network for diffusion.

    Takes noisy actions and observation features, outputs predicted noise.
    """

    def __init__(
        self,
        action_dim: int,
        cond_dim: int,
        hidden_dim: int = 256,
        chunk_size: int = 10
    ):
        super().__init__()
        self.action_dim = action_dim
        self.chunk_size = chunk_size

        # Time embedding
        self.time_embed = nn.Sequential(
            SinusoidalTimeEmbedding(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # Input projection
        self.input_proj = nn.Linear(action_dim, hidden_dim)

        # Condition projection
        self.cond_proj = nn.Linear(cond_dim, hidden_dim)

        # U-Net blocks (simplified)
        self.down1 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        self.mid = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        self.up1 = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # Output projection
        self.output_proj = nn.Linear(hidden_dim, action_dim)

    def forward(
        self,
        noisy_actions: torch.Tensor,
        timestep: torch.Tensor,
        condition: torch.Tensor
    ) -> torch.Tensor:
        """
        Forward pass of denoising network.

        Args:
            noisy_actions: Noisy actions [B, chunk_size, action_dim]
            timestep: Diffusion timestep [B]
            condition: Observation features [B, cond_dim]

        Returns:
            Predicted noise [B, chunk_size, action_dim]
        """
        batch_size = noisy_actions.shape[0]

        # Embed time
        t_emb = self.time_embed(timestep)  # [B, hidden_dim]

        # Project condition
        cond = self.cond_proj(condition)  # [B, hidden_dim]

        # Project input
        x = self.input_proj(noisy_actions)  # [B, chunk_size, hidden_dim]

        # Add time and condition (broadcast across chunk)
        x = x + t_emb.unsqueeze(1) + cond.unsqueeze(1)

        # U-Net pass
        down = self.down1(x)
        mid = self.mid(down)
        up = self.up1(torch.cat([mid, down], dim=-1))

        # Output projection
        noise_pred = self.output_proj(up)

        return noise_pred


class DiffusionPolicy(BasePolicy):
    """
    Diffusion Policy for action generation.

    Uses DDPM-style diffusion to generate action sequences
    conditioned on observations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Diffusion Policy.

        Args:
            config: Model configuration
                - action_dim: Action dimension
                - chunk_size: Action sequence length
                - num_diffusion_steps: Number of denoising steps
                - hidden_dim: Hidden dimension
        """
        super().__init__(config)

        self.chunk_size = config.get("chunk_size", 10)
        self.hidden_dim = config.get("hidden_dim", 256)
        self.num_diffusion_steps = config.get("num_diffusion_steps", 100)
        self.num_cameras = config.get("num_cameras", 3)
        self.joint_dim = config.get("joint_dim", 6)

        # Vision encoder
        self.vision_encoder = VisionEncoder(
            output_dim=self.hidden_dim,
            pretrained=config.get("pretrained_vision", True)
        )

        # State encoder
        self.state_encoder = nn.Linear(self.joint_dim, self.hidden_dim)

        # Condition dimension
        cond_dim = self.hidden_dim * (self.num_cameras + 1)

        # Denoising network
        self.denoiser = DenoisingUNet(
            action_dim=self.action_dim,
            cond_dim=cond_dim,
            hidden_dim=self.hidden_dim,
            chunk_size=self.chunk_size
        )

        # Diffusion schedule
        self._setup_diffusion_schedule()

    def _setup_diffusion_schedule(self):
        """Set up DDPM noise schedule."""
        # Linear beta schedule
        beta_start = 0.0001
        beta_end = 0.02
        betas = torch.linspace(beta_start, beta_end, self.num_diffusion_steps)

        alphas = 1.0 - betas
        alphas_cumprod = torch.cumprod(alphas, dim=0)

        self.register_buffer("betas", betas)
        self.register_buffer("alphas", alphas)
        self.register_buffer("alphas_cumprod", alphas_cumprod)
        self.register_buffer("sqrt_alphas_cumprod", torch.sqrt(alphas_cumprod))
        self.register_buffer("sqrt_one_minus_alphas_cumprod", torch.sqrt(1.0 - alphas_cumprod))

    def _encode_observations(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Encode observations into condition features."""
        features = []

        # Encode images
        if "image" in observations:
            images = observations["image"]
            for i in range(min(self.num_cameras, images.shape[1])):
                cam_features = self.vision_encoder(images[:, i])
                features.append(cam_features)

        # Encode state
        state_features = self.state_encoder(observations["joint_state"])
        features.append(state_features)

        return torch.cat(features, dim=-1)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass - generate actions via denoising.

        Args:
            observations: Input observations

        Returns:
            Generated action sequence [B, chunk_size, action_dim]
        """
        batch_size = observations["joint_state"].shape[0]
        device = observations["joint_state"].device

        # Encode observations
        condition = self._encode_observations(observations)

        # Start from pure noise
        x = torch.randn(batch_size, self.chunk_size, self.action_dim, device=device)

        # Iterative denoising
        for t in reversed(range(self.num_diffusion_steps)):
            t_tensor = torch.full((batch_size,), t, device=device, dtype=torch.long)

            # Predict noise
            noise_pred = self.denoiser(x, t_tensor.float(), condition)

            # DDPM update step
            alpha = self.alphas[t]
            alpha_cumprod = self.alphas_cumprod[t]
            beta = self.betas[t]

            if t > 0:
                noise = torch.randn_like(x)
            else:
                noise = 0

            x = (1 / torch.sqrt(alpha)) * (
                x - (beta / torch.sqrt(1 - alpha_cumprod)) * noise_pred
            ) + torch.sqrt(beta) * noise

        return x

    def predict(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """Predict single action."""
        self.eval()
        with torch.no_grad():
            tensor_obs = {}
            for key, value in observations.items():
                tensor_obs[key] = torch.from_numpy(value).float().unsqueeze(0)
                if next(self.parameters()).is_cuda:
                    tensor_obs[key] = tensor_obs[key].cuda()

            action_chunk = self.forward(tensor_obs)
            return action_chunk[0, 0].cpu().numpy()

    def compute_loss(
        self,
        observations: Dict[str, torch.Tensor],
        actions: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute diffusion training loss.

        Args:
            observations: Input observations
            actions: Ground truth actions [B, chunk_size, action_dim]

        Returns:
            Scalar loss (noise prediction MSE)
        """
        batch_size = actions.shape[0]
        device = actions.device

        # Encode observations
        condition = self._encode_observations(observations)

        # Sample random timesteps
        t = torch.randint(0, self.num_diffusion_steps, (batch_size,), device=device)

        # Sample noise
        noise = torch.randn_like(actions)

        # Add noise to actions
        sqrt_alpha_cumprod = self.sqrt_alphas_cumprod[t].view(-1, 1, 1)
        sqrt_one_minus_alpha_cumprod = self.sqrt_one_minus_alphas_cumprod[t].view(-1, 1, 1)
        noisy_actions = sqrt_alpha_cumprod * actions + sqrt_one_minus_alpha_cumprod * noise

        # Predict noise
        noise_pred = self.denoiser(noisy_actions, t.float(), condition)

        # MSE loss
        return F.mse_loss(noise_pred, noise)
