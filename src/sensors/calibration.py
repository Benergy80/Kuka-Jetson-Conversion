"""Sensor Calibration Utilities"""
import numpy as np
from typing import Dict, Any
import json

class SensorCalibration:
    """Sensor calibration data management."""

    def __init__(self):
        self.camera_intrinsics: Dict[str, np.ndarray] = {}
        self.camera_extrinsics: Dict[str, np.ndarray] = {}
        self.ft_calibration: Dict[str, Any] = {}

    def save(self, path: str) -> None:
        """Save calibration to file."""
        data = {
            "camera_intrinsics": {k: v.tolist() for k, v in self.camera_intrinsics.items()},
            "camera_extrinsics": {k: v.tolist() for k, v in self.camera_extrinsics.items()},
            "ft_calibration": self.ft_calibration,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, path: str) -> None:
        """Load calibration from file."""
        with open(path) as f:
            data = json.load(f)
        self.camera_intrinsics = {k: np.array(v) for k, v in data.get("camera_intrinsics", {}).items()}
        self.camera_extrinsics = {k: np.array(v) for k, v in data.get("camera_extrinsics", {}).items()}
        self.ft_calibration = data.get("ft_calibration", {})
