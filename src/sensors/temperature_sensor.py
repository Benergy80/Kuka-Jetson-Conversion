"""Temperature Sensor Interface"""
from typing import Dict, List

class TemperatureSensor:
    """Interface for temperature monitoring sensors."""

    def __init__(self, sensor_ids: List[str]):
        self.sensor_ids = sensor_ids
        self._thresholds = {sid: 80.0 for sid in sensor_ids}  # °C

    def read_all(self) -> Dict[str, float]:
        """Read all temperature sensors."""
        # Placeholder - actual implementation reads from hardware
        return {sid: 25.0 for sid in self.sensor_ids}

    def check_overtemp(self) -> List[str]:
        """Return list of sensors exceeding threshold."""
        readings = self.read_all()
        return [sid for sid, temp in readings.items()
                if temp > self._thresholds.get(sid, 80.0)]
