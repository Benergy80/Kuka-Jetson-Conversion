"""Training Loop"""
import torch
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Any
import time

class Trainer:
    """Training loop for robot policy models."""

    def __init__(self, model, optimizer, config: Dict = None):
        self.model = model
        self.optimizer = optimizer
        self.config = config or {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.callbacks = []
        self.history = {"train_loss": [], "val_loss": []}

    def add_callback(self, callback):
        """Add training callback."""
        self.callbacks.append(callback)

    def train(self, train_loader: DataLoader, val_loader: Optional[DataLoader] = None,
              epochs: int = 100) -> Dict:
        """Run training loop."""
        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0.0
            for batch_obs, batch_actions in train_loader:
                batch_obs = {k: v.to(self.device) for k, v in batch_obs.items()}
                batch_actions = batch_actions.to(self.device)

                self.optimizer.zero_grad()
                loss = self.model.compute_loss(batch_obs, batch_actions)
                loss.backward()
                self.optimizer.step()
                train_loss += loss.item()

            train_loss /= len(train_loader)
            self.history["train_loss"].append(train_loss)

            # Validation
            val_loss = None
            if val_loader:
                val_loss = self._validate(val_loader)
                self.history["val_loss"].append(val_loss)

            # Callbacks
            for cb in self.callbacks:
                cb.on_epoch_end(epoch, train_loss, val_loss, self.model)

            print(f"Epoch {epoch+1}/{epochs} - Loss: {train_loss:.6f}" +
                  (f" - Val Loss: {val_loss:.6f}" if val_loss else ""))

        return self.history

    def _validate(self, val_loader: DataLoader) -> float:
        """Run validation."""
        self.model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch_obs, batch_actions in val_loader:
                batch_obs = {k: v.to(self.device) for k, v in batch_obs.items()}
                batch_actions = batch_actions.to(self.device)
                loss = self.model.compute_loss(batch_obs, batch_actions)
                val_loss += loss.item()
        return val_loss / len(val_loader)
