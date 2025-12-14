"""Force/Torque Sensor Interface"""
import numpy as np
from dataclasses import dataclass

@dataclass
class FTReading:
    force: np.ndarray  # [Fx, Fy, Fz] in N
    torque: np.ndarray  # [Tx, Ty, Tz] in Nm
    timestamp: float

class ForceTorqueSensor:
    """Interface for 6-axis force/torque sensor."""

    def __init__(self, interface: str = "serial", port: str = "/dev/ttyUSB0"):
        self.interface = interface
        self.port = port
        self._bias = np.zeros(6)

    def read(self) -> FTReading:
        """Read current force/torque values."""
        import time
        # Placeholder - actual implementation reads from sensor
        raw = np.zeros(6)
        corrected = raw - self._bias
        return FTReading(
            force=corrected[:3],
            torque=corrected[3:],
            timestamp=time.time()
        )

    def tare(self) -> None:
        """Zero the sensor (remove bias)."""
        readings = [self.read() for _ in range(10)]
        forces = np.array([r.force for r in readings])
        torques = np.array([r.torque for r in readings])
        self._bias = np.concatenate([forces.mean(axis=0), torques.mean(axis=0)])
