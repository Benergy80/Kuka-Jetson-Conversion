"""Training Metrics"""
import numpy as np
from typing import Dict

def compute_metrics(predictions: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
    """Compute evaluation metrics."""
    mse = np.mean((predictions - targets) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(predictions - targets))

    # Per-joint metrics
    per_joint_mse = np.mean((predictions - targets) ** 2, axis=0)

    return {
        "mse": float(mse),
        "rmse": float(rmse),
        "mae": float(mae),
        "per_joint_mse": per_joint_mse.tolist(),
    }
