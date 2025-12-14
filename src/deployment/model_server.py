"""Model Server for inference"""
import threading
from typing import Dict, Optional
import numpy as np

class ModelServer:
    """Serves ML model for real-time inference."""

    def __init__(self, model, device: str = "cuda"):
        self.model = model
        self.device = device
        self._lock = threading.Lock()
        self._running = False

    def start(self):
        """Start model server."""
        self._running = True
        self.model.eval()

    def stop(self):
        """Stop model server."""
        self._running = False

    def predict(self, observations: Dict[str, np.ndarray]) -> np.ndarray:
        """Thread-safe prediction."""
        if not self._running:
            raise RuntimeError("Server not running")

        with self._lock:
            return self.model.predict(observations)

    def get_latency_stats(self) -> Dict:
        """Get inference latency statistics."""
        return {"mean_ms": 0.0, "max_ms": 0.0}  # Placeholder
