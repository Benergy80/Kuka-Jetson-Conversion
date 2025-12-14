"""Hot-swap model management"""
import threading
from typing import Optional

class HotSwapManager:
    """Manages model hot-swapping during operation."""

    def __init__(self, model_server):
        self.server = model_server
        self._pending_model = None
        self._lock = threading.Lock()

    def queue_model(self, new_model) -> None:
        """Queue a new model for hot-swap."""
        with self._lock:
            self._pending_model = new_model

    def execute_swap(self) -> bool:
        """Execute the model swap (call between control cycles)."""
        with self._lock:
            if self._pending_model is None:
                return False
            self.server.model = self._pending_model
            self._pending_model = None
            return True

    def has_pending(self) -> bool:
        """Check if a model swap is pending."""
        return self._pending_model is not None
