"""
Vision Encoder

CNN-based encoder for processing camera images.
"""

from typing import Optional
import torch
import torch.nn as nn
import torchvision.models as models


class VisionEncoder(nn.Module):
    """
    Vision encoder using ResNet backbone.

    Encodes camera images into feature vectors for policy input.
    """

    def __init__(
        self,
        output_dim: int = 256,
        pretrained: bool = True,
        backbone: str = "resnet18"
    ):
        """
        Initialize vision encoder.

        Args:
            output_dim: Output feature dimension
            pretrained: Use ImageNet pretrained weights
            backbone: Backbone architecture (resnet18, resnet34, resnet50)
        """
        super().__init__()

        # Load backbone
        if backbone == "resnet18":
            self.backbone = models.resnet18(pretrained=pretrained)
            backbone_dim = 512
        elif backbone == "resnet34":
            self.backbone = models.resnet34(pretrained=pretrained)
            backbone_dim = 512
        elif backbone == "resnet50":
            self.backbone = models.resnet50(pretrained=pretrained)
            backbone_dim = 2048
        else:
            raise ValueError(f"Unknown backbone: {backbone}")

        # Remove classification head
        self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])

        # Projection head
        self.projection = nn.Sequential(
            nn.Flatten(),
            nn.Linear(backbone_dim, output_dim),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode image to feature vector.

        Args:
            x: Input image [B, C, H, W] (expects normalized RGB)

        Returns:
            Feature vector [B, output_dim]
        """
        features = self.backbone(x)
        return self.projection(features)


class MultiViewEncoder(nn.Module):
    """
    Multi-view vision encoder for multiple cameras.

    Processes multiple camera views and fuses features.
    """

    def __init__(
        self,
        num_cameras: int = 3,
        output_dim: int = 256,
        pretrained: bool = True,
        share_weights: bool = True
    ):
        """
        Initialize multi-view encoder.

        Args:
            num_cameras: Number of camera views
            output_dim: Output dimension per camera
            pretrained: Use pretrained backbone
            share_weights: Share encoder weights across cameras
        """
        super().__init__()

        self.num_cameras = num_cameras
        self.share_weights = share_weights

        if share_weights:
            self.encoder = VisionEncoder(output_dim, pretrained)
        else:
            self.encoders = nn.ModuleList([
                VisionEncoder(output_dim, pretrained)
                for _ in range(num_cameras)
            ])

        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(output_dim * num_cameras, output_dim * 2),
            nn.ReLU(),
            nn.Linear(output_dim * 2, output_dim),
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """
        Encode multiple camera views.

        Args:
            images: Input images [B, num_cameras, C, H, W]

        Returns:
            Fused feature vector [B, output_dim]
        """
        batch_size = images.shape[0]
        features = []

        for i in range(self.num_cameras):
            if self.share_weights:
                feat = self.encoder(images[:, i])
            else:
                feat = self.encoders[i](images[:, i])
            features.append(feat)

        # Concatenate and fuse
        concat_features = torch.cat(features, dim=-1)
        return self.fusion(concat_features)
