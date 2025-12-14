"""PyTorch DataLoader creation"""
import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict
import numpy as np

class RobotDataset(Dataset):
    """PyTorch Dataset for robot demonstrations."""

    def __init__(self, episodes: List, chunk_size: int = 10):
        self.episodes = episodes
        self.chunk_size = chunk_size
        self._build_index()

    def _build_index(self):
        """Build index of (episode_idx, timestep) pairs."""
        self.index = []
        for ep_idx, episode in enumerate(self.episodes):
            num_steps = len(episode.actions) - self.chunk_size
            for t in range(max(1, num_steps)):
                self.index.append((ep_idx, t))

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        ep_idx, t = self.index[idx]
        episode = self.episodes[ep_idx]

        obs = {key: torch.from_numpy(value[t]).float()
               for key, value in episode.observations.items()}
        actions = torch.from_numpy(episode.actions[t:t+self.chunk_size]).float()

        return obs, actions

def create_dataloader(episodes: List, batch_size: int = 32, shuffle: bool = True,
                      num_workers: int = 4, chunk_size: int = 10) -> DataLoader:
    """Create DataLoader for training."""
    dataset = RobotDataset(episodes, chunk_size)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle,
                     num_workers=num_workers, pin_memory=True)
