"""Physics Engine Interface"""
import numpy as np

class PhysicsEngine:
    """Interface to physics simulation (PyBullet, MuJoCo, etc.)."""

    def __init__(self, engine: str = "pybullet"):
        self.engine = engine
        self._client = None

    def connect(self, gui: bool = False):
        """Connect to physics engine."""
        if self.engine == "pybullet":
            try:
                import pybullet as p
                mode = p.GUI if gui else p.DIRECT
                self._client = p.connect(mode)
                p.setGravity(0, 0, -9.81)
            except ImportError:
                print("PyBullet not available")

    def disconnect(self):
        """Disconnect from physics engine."""
        if self._client is not None:
            try:
                import pybullet as p
                p.disconnect(self._client)
            except:
                pass

    def step(self):
        """Step physics simulation."""
        if self._client is not None:
            try:
                import pybullet as p
                p.stepSimulation()
            except:
                pass
