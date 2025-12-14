"""
Kuka ML Controller - Main Package

This package contains the complete software stack for ML-based control
of a Kuka 5-axis robot arm with turning bed.

Modules:
    control: Real-time control system (1kHz loop)
    hardware: Hardware interfaces (EtherCAT, GPIO, encoders)
    sensors: Sensor interfaces (cameras, force/torque, temperature)
    models: ML model implementations (BC, ACT, Diffusion)
    data: Data handling and preprocessing
    training: Training pipeline
    deployment: Model deployment and optimization
    safety: Safety systems and validation
    teleoperation: Teleoperation for data collection
    simulation: Digital twin simulation
    utils: Utility functions
"""

__version__ = "0.1.0"
__author__ = "Kuka ML Controller Team"
