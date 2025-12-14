"""
Online Learning Module

Enables continuous learning from human corrections during deployment.
"""

from typing import Dict, Any, Optional, List
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
from collections import deque
from dataclasses import dataclass
import threading
import time

from .base_model import BasePolicy


@dataclass
class CorrectionSample:
    """A human correction sample for online learning."""
    observation: Dict[str, np.ndarray]
    ml_action: np.ndarray
    human_action: np.ndarray
    timestamp: float


class ReplayBuffer:
    """
    Experience replay buffer for online learning.

    Stores human corrections and samples mini-batches for training.
    """

    def __init__(self, max_size: int = 10000):
        """
        Initialize replay buffer.

        Args:
            max_size: Maximum number of samples to store
        """
        self.max_size = max_size
        self.buffer: deque = deque(maxlen=max_size)
        self._lock = threading.Lock()

    def add(self, sample: CorrectionSample) -> None:
        """Add a sample to the buffer."""
        with self._lock:
            self.buffer.append(sample)

    def sample(self, batch_size: int) -> List[CorrectionSample]:
        """Sample a mini-batch of corrections."""
        with self._lock:
            indices = np.random.choice(
                len(self.buffer),
                size=min(batch_size, len(self.buffer)),
                replace=False
            )
            return [self.buffer[i] for i in indices]

    def __len__(self) -> int:
        return len(self.buffer)


class OnlineLearner:
    """
    Online learning system for continuous policy improvement.

    Collects human corrections during deployment and periodically
    fine-tunes the policy model.
    """

    def __init__(
        self,
        policy: BasePolicy,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize online learner.

        Args:
            policy: Policy model to fine-tune
            config: Learning configuration
        """
        self.policy = policy
        self.config = config or {}

        self.buffer = ReplayBuffer(
            max_size=self.config.get("buffer_size", 10000)
        )
        self.batch_size = self.config.get("batch_size", 32)
        self.learning_rate = self.config.get("learning_rate", 1e-5)
        self.update_frequency = self.config.get("update_frequency", 100)
        self.min_samples = self.config.get("min_samples", 50)

        self.optimizer = torch.optim.Adam(
            policy.parameters(),
            lr=self.learning_rate
        )

        self._step_count = 0
        self._is_training = False
        self._training_thread: Optional[threading.Thread] = None

    def add_correction(
        self,
        observation: Dict[str, np.ndarray],
        ml_action: np.ndarray,
        human_action: np.ndarray
    ) -> None:
        """
        Add a human correction to the buffer.

        Called when human intervenes during ML execution.

        Args:
            observation: Current observation
            ml_action: Action predicted by ML
            human_action: Corrected action from human
        """
        sample = CorrectionSample(
            observation=observation,
            ml_action=ml_action,
            human_action=human_action,
            timestamp=time.time()
        )
        self.buffer.add(sample)

        self._step_count += 1

        # Trigger training if conditions met
        if (self._step_count % self.update_frequency == 0 and
            len(self.buffer) >= self.min_samples and
            not self._is_training):
            self._trigger_training()

    def _trigger_training(self) -> None:
        """Start background training thread."""
        self._training_thread = threading.Thread(
            target=self._train_step,
            daemon=True
        )
        self._training_thread.start()

    def _train_step(self) -> None:
        """Perform one training step on collected corrections."""
        self._is_training = True

        try:
            # Sample batch
            samples = self.buffer.sample(self.batch_size)

            # Prepare batch tensors
            observations = self._collate_observations(samples)
            target_actions = torch.stack([
                torch.from_numpy(s.human_action).float()
                for s in samples
            ])

            device = next(self.policy.parameters()).device
            for key in observations:
                observations[key] = observations[key].to(device)
            target_actions = target_actions.to(device)

            # Training step
            self.policy.train()
            self.optimizer.zero_grad()

            loss = self.policy.compute_loss(observations, target_actions)
            loss.backward()
            self.optimizer.step()

            self.policy.eval()

        finally:
            self._is_training = False

    def _collate_observations(
        self,
        samples: List[CorrectionSample]
    ) -> Dict[str, torch.Tensor]:
        """Collate observations from samples into batch tensors."""
        result = {}

        # Get keys from first sample
        keys = samples[0].observation.keys()

        for key in keys:
            tensors = [
                torch.from_numpy(s.observation[key]).float()
                for s in samples
            ]
            result[key] = torch.stack(tensors)

        return result

    def save_buffer(self, path: str) -> None:
        """Save replay buffer to disk."""
        import pickle
        with open(path, "wb") as f:
            pickle.dump(list(self.buffer.buffer), f)

    def load_buffer(self, path: str) -> None:
        """Load replay buffer from disk."""
        import pickle
        with open(path, "rb") as f:
            samples = pickle.load(f)
            for sample in samples:
                self.buffer.add(sample)

    def get_stats(self) -> Dict[str, Any]:
        """Get online learning statistics."""
        return {
            "buffer_size": len(self.buffer),
            "step_count": self._step_count,
            "is_training": self._is_training,
        }
