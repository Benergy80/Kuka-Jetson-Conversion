"""Model Evaluator"""
import torch
import numpy as np
from typing import Dict, List

class Evaluator:
    """Evaluates trained policy models."""

    def __init__(self, model, device: str = "cuda"):
        self.model = model
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def evaluate_dataset(self, dataloader) -> Dict[str, float]:
        """Evaluate on a dataset."""
        total_loss = 0.0
        total_mse = 0.0
        count = 0

        with torch.no_grad():
            for batch_obs, batch_actions in dataloader:
                batch_obs = {k: v.to(self.device) for k, v in batch_obs.items()}
                batch_actions = batch_actions.to(self.device)

                loss = self.model.compute_loss(batch_obs, batch_actions)
                pred = self.model(batch_obs)

                total_loss += loss.item()
                total_mse += ((pred - batch_actions) ** 2).mean().item()
                count += 1

        return {
            "loss": total_loss / count,
            "mse": total_mse / count,
            "rmse": np.sqrt(total_mse / count),
        }

    def benchmark_inference(self, sample_obs: Dict, num_runs: int = 100) -> Dict:
        """Benchmark inference speed."""
        import time

        # Warmup
        for _ in range(10):
            self.model.predict(sample_obs)

        # Benchmark
        times = []
        for _ in range(num_runs):
            start = time.perf_counter()
            self.model.predict(sample_obs)
            times.append((time.perf_counter() - start) * 1000)  # ms

        return {
            "mean_ms": np.mean(times),
            "std_ms": np.std(times),
            "min_ms": np.min(times),
            "max_ms": np.max(times),
        }
