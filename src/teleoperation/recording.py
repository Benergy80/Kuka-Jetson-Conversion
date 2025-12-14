"""Demonstration Recording"""
import time
import numpy as np
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class DemoFrame:
    observations: Dict[str, np.ndarray]
    action: np.ndarray
    timestamp: float

class DemonstrationRecorder:
    """Records demonstrations for imitation learning."""

    def __init__(self, sensor_manager, action_dim: int = 6):
        self.sensors = sensor_manager
        self.action_dim = action_dim
        self.frames: List[DemoFrame] = []
        self._is_recording = False

    def start_recording(self):
        """Start recording demonstration."""
        self.frames = []
        self._is_recording = True
        self._start_time = time.time()

    def stop_recording(self):
        """Stop recording demonstration."""
        self._is_recording = False

    def record_frame(self, action: np.ndarray):
        """Record a single frame."""
        if not self._is_recording:
            return

        obs = self.sensors.get_observations() if self.sensors else {}
        frame = DemoFrame(
            observations=obs,
            action=action,
            timestamp=time.time() - self._start_time
        )
        self.frames.append(frame)

    def get_episode(self) -> Dict:
        """Get recorded episode as dictionary."""
        if not self.frames:
            return {}

        obs_keys = self.frames[0].observations.keys()
        return {
            "observations": {
                key: np.stack([f.observations[key] for f in self.frames])
                for key in obs_keys
            },
            "actions": np.stack([f.action for f in self.frames]),
            "timestamps": np.array([f.timestamp for f in self.frames]),
        }
