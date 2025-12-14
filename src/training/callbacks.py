"""Training Callbacks"""
import os
import torch
from typing import Optional

class Callback:
    """Base callback class."""
    def on_epoch_end(self, epoch: int, train_loss: float, val_loss: Optional[float], model):
        pass

class CheckpointCallback(Callback):
    """Save model checkpoints."""
    def __init__(self, save_dir: str, save_every: int = 10):
        self.save_dir = save_dir
        self.save_every = save_every
        self.best_loss = float("inf")
        os.makedirs(save_dir, exist_ok=True)

    def on_epoch_end(self, epoch: int, train_loss: float, val_loss: Optional[float], model):
        loss = val_loss if val_loss else train_loss

        # Save periodic checkpoint
        if (epoch + 1) % self.save_every == 0:
            path = os.path.join(self.save_dir, f"checkpoint_epoch{epoch+1}.pth")
            model.save(path)

        # Save best model
        if loss < self.best_loss:
            self.best_loss = loss
            path = os.path.join(self.save_dir, "best_model.pth")
            model.save(path)

class EarlyStoppingCallback(Callback):
    """Early stopping based on validation loss."""
    def __init__(self, patience: int = 10, min_delta: float = 1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float("inf")
        self.counter = 0
        self.should_stop = False

    def on_epoch_end(self, epoch: int, train_loss: float, val_loss: Optional[float], model):
        loss = val_loss if val_loss else train_loss
        if loss < self.best_loss - self.min_delta:
            self.best_loss = loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
                print(f"Early stopping at epoch {epoch+1}")
