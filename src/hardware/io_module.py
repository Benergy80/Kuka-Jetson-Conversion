"""
I/O Module Interface

Interface for EtherCAT digital and analog I/O modules.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class IOModuleConfig:
    """I/O module configuration."""
    slave_id: int
    num_digital_inputs: int = 16
    num_digital_outputs: int = 16
    num_analog_inputs: int = 4
    num_analog_outputs: int = 2
    analog_input_range: float = 10.0  # Volts
    analog_output_range: float = 10.0  # Volts


class IOModule:
    """
    Interface for EtherCAT I/O modules.

    Provides:
    - Digital input/output
    - Analog input/output
    - Safety I/O mapping
    """

    def __init__(self, config: IOModuleConfig, ethercat_master=None):
        """
        Initialize I/O module interface.

        Args:
            config: Module configuration
            ethercat_master: EtherCAT master instance
        """
        self.config = config
        self.master = ethercat_master

        # State storage
        self._digital_inputs = [False] * config.num_digital_inputs
        self._digital_outputs = [False] * config.num_digital_outputs
        self._analog_inputs = [0.0] * config.num_analog_inputs
        self._analog_outputs = [0.0] * config.num_analog_outputs

        # Named I/O mapping
        self._input_names: Dict[str, int] = {}
        self._output_names: Dict[str, int] = {}

    def map_input(self, name: str, channel: int) -> None:
        """Map a name to an input channel."""
        if 0 <= channel < self.config.num_digital_inputs:
            self._input_names[name] = channel

    def map_output(self, name: str, channel: int) -> None:
        """Map a name to an output channel."""
        if 0 <= channel < self.config.num_digital_outputs:
            self._output_names[name] = channel

    def read_digital_input(self, channel: int) -> bool:
        """
        Read digital input.

        Args:
            channel: Input channel number

        Returns:
            Input state
        """
        if 0 <= channel < self.config.num_digital_inputs:
            return self._digital_inputs[channel]
        return False

    def read_digital_input_by_name(self, name: str) -> bool:
        """Read digital input by mapped name."""
        channel = self._input_names.get(name)
        if channel is not None:
            return self.read_digital_input(channel)
        return False

    def write_digital_output(self, channel: int, state: bool) -> None:
        """
        Write digital output.

        Args:
            channel: Output channel number
            state: Output state
        """
        if 0 <= channel < self.config.num_digital_outputs:
            self._digital_outputs[channel] = state

    def write_digital_output_by_name(self, name: str, state: bool) -> None:
        """Write digital output by mapped name."""
        channel = self._output_names.get(name)
        if channel is not None:
            self.write_digital_output(channel, state)

    def read_analog_input(self, channel: int) -> float:
        """
        Read analog input.

        Args:
            channel: Input channel number

        Returns:
            Analog value in volts
        """
        if 0 <= channel < self.config.num_analog_inputs:
            return self._analog_inputs[channel]
        return 0.0

    def write_analog_output(self, channel: int, value: float) -> None:
        """
        Write analog output.

        Args:
            channel: Output channel number
            value: Output value in volts
        """
        if 0 <= channel < self.config.num_analog_outputs:
            # Clamp to range
            value = max(-self.config.analog_output_range,
                       min(self.config.analog_output_range, value))
            self._analog_outputs[channel] = value

    def update_pdo(self) -> None:
        """
        Update PDO data for cyclic exchange.

        Called at 1kHz from control loop.
        """
        if self.master is None:
            return

        # Pack output PDO data
        # Digital outputs as bit-packed bytes
        output_bits = 0
        for i, state in enumerate(self._digital_outputs):
            if state:
                output_bits |= (1 << i)

        # TODO: Pack analog outputs and send via EtherCAT

        # Read input PDO data
        input_data = self.master.read_pdo(self.config.slave_id)
        if input_data:
            # TODO: Unpack digital and analog inputs
            pass

    def get_all_digital_inputs(self) -> List[bool]:
        """Get all digital input states."""
        return self._digital_inputs.copy()

    def get_all_digital_outputs(self) -> List[bool]:
        """Get all digital output states."""
        return self._digital_outputs.copy()

    def get_all_analog_inputs(self) -> List[float]:
        """Get all analog input values."""
        return self._analog_inputs.copy()
