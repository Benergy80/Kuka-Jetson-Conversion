"""Model Benchmarking"""
import time
import numpy as np
from typing import Dict

def benchmark_model(model, sample_obs: Dict, num_iterations: int = 1000) -> Dict:
    """Benchmark model inference performance."""
    model.eval()

    # Warmup
    for _ in range(50):
        model.predict(sample_obs)

    # Benchmark
    latencies = []
    for _ in range(num_iterations):
        start = time.perf_counter()
        model.predict(sample_obs)
        latencies.append((time.perf_counter() - start) * 1000)

    latencies = np.array(latencies)
    return {
        "mean_ms": float(np.mean(latencies)),
        "std_ms": float(np.std(latencies)),
        "min_ms": float(np.min(latencies)),
        "max_ms": float(np.max(latencies)),
        "p50_ms": float(np.percentile(latencies, 50)),
        "p95_ms": float(np.percentile(latencies, 95)),
        "p99_ms": float(np.percentile(latencies, 99)),
        "throughput_hz": float(1000 / np.mean(latencies)),
    }
