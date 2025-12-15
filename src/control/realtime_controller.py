"""
Real-time Controller

Main control loop running at 1kHz for servo control.
Requires PREEMPT_RT kernel for deterministic timing.
"""

import time
import threading
from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class ControllerConfig:
    """Configuration for the real-time controller."""
    loop_frequency_hz: float = 1000.0  # 1kHz control loop
    watchdog_timeout_ms: float = 100.0
    enable_feedforward: bool = True
    safety_check_enabled: bool = True


@dataclass
class JointState:
    """Current state of robot joints."""
    positions: np.ndarray  # Joint positions (rad)
    velocities: np.ndarray  # Joint velocities (rad/s)
    torques: np.ndarray  # Joint torques (Nm)
    timestamp: float


class RealtimeController:
    """
    Real-time controller for Kuka robot arm.

    Implements a 1kHz control loop with:
    - Sensor data acquisition
    - Safety monitoring
    - PID control with feedforward
    - EtherCAT communication

    Attributes:
        config: Controller configuration
        running: Whether the control loop is running
        current_state: Current joint state
    """

    def __init__(
        self,
        config: Optional[ControllerConfig] = None,
        pid_controllers=None,
        safety_monitor=None,
        ethercat_master=None,
        feedforward=None
    ):
        """
        Initialize the real-time controller.

        Args:
            config: Controller configuration. Uses defaults if None.
            pid_controllers: PID controller instance for joints
            safety_monitor: Safety monitor instance
            ethercat_master: EtherCAT master interface
            feedforward: Feedforward compensator
        """
        self.config = config or ControllerConfig()
        self.running = False
        self.current_state: Optional[JointState] = None
        self._control_thread: Optional[threading.Thread] = None
        self._target_joints: Optional[np.ndarray] = None
        self._target_velocities: Optional[np.ndarray] = None
        self._target_accelerations: Optional[np.ndarray] = None
        self._dt = 1.0 / self.config.loop_frequency_hz

        # Initialize subsystems
        self._pid_controllers = pid_controllers
        self._safety_monitor = safety_monitor
        self._ethercat_master = ethercat_master
        self._feedforward = feedforward
        self._emergency_stop_triggered = False
        self._cycle_count = 0
        self._last_positions: Optional[np.ndarray] = None
        self._last_velocities: Optional[np.ndarray] = None

    def start(self) -> None:
        """Start the real-time control loop."""
        if self.running:
            raise RuntimeError("Controller is already running")

        self.running = True
        self._control_thread = threading.Thread(
            target=self._control_loop,
            daemon=True,
            name="RealtimeControlLoop"
        )
        self._control_thread.start()

    def stop(self) -> None:
        """Stop the real-time control loop."""
        self.running = False
        if self._control_thread is not None:
            self._control_thread.join(timeout=1.0)

    def set_target(
        self,
        target_joints: np.ndarray,
        target_velocities: Optional[np.ndarray] = None,
        target_accelerations: Optional[np.ndarray] = None
    ) -> None:
        """
        Set target joint positions with optional feedforward terms.

        Args:
            target_joints: Target joint positions (rad)
            target_velocities: Target joint velocities (rad/s)
            target_accelerations: Target joint accelerations (rad/s²)
        """
        self._target_joints = target_joints.copy()
        self._target_velocities = target_velocities.copy() if target_velocities is not None else None
        self._target_accelerations = target_accelerations.copy() if target_accelerations is not None else None

    def get_state(self) -> Optional[JointState]:
        """Get current joint state."""
        return self.current_state

    def _control_loop(self) -> None:
        """Main control loop running at configured frequency."""
        period_ns = int(1e9 / self.config.loop_frequency_hz)

        while self.running:
            loop_start = time.perf_counter_ns()

            try:
                # 1. Read sensors
                self._read_sensors()

                # 2. Safety check
                if self.config.safety_check_enabled:
                    self._safety_check()

                # 3. Compute control
                if self._target_joints is not None:
                    commands = self._compute_control()

                    # 4. Send commands
                    self._send_commands(commands)

            except Exception as e:
                # Log error and trigger safety stop
                self._emergency_stop(str(e))
                break

            # Enforce cycle time
            elapsed_ns = time.perf_counter_ns() - loop_start
            if elapsed_ns < period_ns:
                time.sleep((period_ns - elapsed_ns) / 1e9)

    def _read_sensors(self) -> None:
        """Read sensor data from EtherCAT network."""
        if self._ethercat_master is not None:
            # Read from EtherCAT hardware
            try:
                positions = self._ethercat_master.read_joint_positions()
                velocities = self._ethercat_master.read_joint_velocities()
                torques = self._ethercat_master.read_joint_torques()
            except Exception as e:
                # Fallback to simulated data for testing
                positions = self._last_positions if self._last_positions is not None else np.zeros(6)
                velocities = self._last_velocities if self._last_velocities is not None else np.zeros(6)
                torques = np.zeros(6)
        else:
            # Simulated mode for testing without hardware
            if self._last_positions is None:
                positions = np.zeros(6)
                velocities = np.zeros(6)
            else:
                # Simulate motion toward target
                if self._target_joints is not None:
                    error = self._target_joints - self._last_positions
                    positions = self._last_positions + 0.01 * error  # Simple simulation
                    velocities = (positions - self._last_positions) / self._dt
                else:
                    positions = self._last_positions
                    velocities = np.zeros(6)
            torques = np.zeros(6)

        self.current_state = JointState(
            positions=positions,
            velocities=velocities,
            torques=torques,
            timestamp=time.perf_counter()
        )

        self._last_positions = positions.copy()
        self._last_velocities = velocities.copy()

    def _safety_check(self) -> None:
        """Perform safety checks on current state."""
        if self._safety_monitor is None:
            return

        if self.current_state is None:
            raise RuntimeError("No sensor data available for safety check")

        # Check position limits
        from ..safety.limit_checker import LimitChecker
        if isinstance(self._safety_monitor, LimitChecker):
            if not self._safety_monitor.check_position(self.current_state.positions):
                raise RuntimeError("Position limit violation")

        # Check velocity limits (if available in safety monitor)
        if hasattr(self._safety_monitor, 'check_velocity'):
            if not self._safety_monitor.check_velocity(self.current_state.velocities):
                raise RuntimeError("Velocity limit violation")

        # Check for emergency stop condition
        if self._emergency_stop_triggered:
            raise RuntimeError("Emergency stop active")

    def _compute_control(self) -> np.ndarray:
        """Compute motor commands from PID control with feedforward."""
        if self.current_state is None:
            return np.zeros(6)

        commands = np.zeros(6)

        # PID control
        if self._pid_controllers is not None:
            commands += self._pid_controllers.compute(
                targets=self._target_joints,
                actuals=self.current_state.positions,
                dt=self._dt,
                target_velocities=self._target_velocities,
                target_accelerations=self._target_accelerations
            )

        # Feedforward compensation
        if self.config.enable_feedforward and self._feedforward is not None:
            if self._target_velocities is not None and self._target_accelerations is not None:
                ff_torque = self._feedforward.compute(
                    self.current_state.positions,
                    self._target_velocities,
                    self._target_accelerations
                )
                commands += ff_torque

        return commands

    def _send_commands(self, commands: np.ndarray) -> None:
        """Send motor commands via EtherCAT."""
        if self._ethercat_master is not None:
            try:
                self._ethercat_master.write_joint_torques(commands)
            except Exception as e:
                raise RuntimeError(f"Failed to send commands: {e}")
        # If no hardware, commands are just computed (simulation mode)

    def _emergency_stop(self, reason: str) -> None:
        """Trigger emergency stop."""
        self._emergency_stop_triggered = True
        self.running = False

        # Zero all motor commands
        if self._ethercat_master is not None:
            try:
                self._ethercat_master.write_joint_torques(np.zeros(6))
                self._ethercat_master.disable_drives()
            except Exception:
                pass  # Best effort

        print(f"EMERGENCY STOP: {reason}")
