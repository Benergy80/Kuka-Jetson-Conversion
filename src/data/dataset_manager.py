"""Dataset Manager - Storage and retrieval of demonstration data"""
import os
import h5py
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Episode:
    observations: Dict[str, np.ndarray]
    actions: np.ndarray
    timestamps: np.ndarray
    metadata: Dict

class DatasetManager:
    """Manages demonstration datasets in HDF5 format."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_episode(self, episode: Episode, episode_id: str) -> str:
        """Save an episode to HDF5."""
        path = os.path.join(self.data_dir, f"{episode_id}.h5")
        with h5py.File(path, "w") as f:
            for key, value in episode.observations.items():
                f.create_dataset(f"observations/{key}", data=value, compression="gzip")
            f.create_dataset("actions", data=episode.actions, compression="gzip")
            f.create_dataset("timestamps", data=episode.timestamps)
            for key, value in episode.metadata.items():
                f.attrs[key] = value
        return path

    def load_episode(self, episode_id: str) -> Episode:
        """Load an episode from HDF5."""
        path = os.path.join(self.data_dir, f"{episode_id}.h5")
        with h5py.File(path, "r") as f:
            observations = {key: f[f"observations/{key}"][:] for key in f["observations"].keys()}
            actions = f["actions"][:]
            timestamps = f["timestamps"][:]
            metadata = dict(f.attrs)
        return Episode(observations, actions, timestamps, metadata)

    def list_episodes(self) -> List[str]:
        """List all episode IDs."""
        return [f[:-3] for f in os.listdir(self.data_dir) if f.endswith(".h5")]
