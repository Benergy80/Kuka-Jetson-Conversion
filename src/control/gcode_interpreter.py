"""
G-Code Interpreter

Parses and executes G-code programs for CNC operations.
"""

import re
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class MotionMode(Enum):
    """Motion modes for G-code."""
    RAPID = "G0"  # Rapid positioning
    LINEAR = "G1"  # Linear interpolation
    CW_ARC = "G2"  # Clockwise arc
    CCW_ARC = "G3"  # Counter-clockwise arc


@dataclass
class GCodeCommand:
    """Parsed G-code command."""
    code: str  # G0, G1, M3, etc.
    params: Dict[str, float] = field(default_factory=dict)
    line_number: Optional[int] = None
    comment: Optional[str] = None


@dataclass
class MachineState:
    """Current machine state."""
    position: np.ndarray  # Current position (X, Y, Z, A, B, C)
    feedrate: float = 1000.0  # mm/min
    spindle_speed: float = 0.0  # RPM
    spindle_on: bool = False
    coolant_on: bool = False
    motion_mode: MotionMode = MotionMode.RAPID
    absolute_mode: bool = True  # G90/G91
    work_offset: np.ndarray = field(default_factory=lambda: np.zeros(6))


class GCodeInterpreter:
    """
    G-code interpreter for Kuka CNC machine.

    Supported codes:
    - G0: Rapid positioning
    - G1: Linear interpolation
    - G2/G3: Circular interpolation
    - G28: Return to home
    - G90/G91: Absolute/incremental positioning
    - M3/M4/M5: Spindle control
    - M8/M9: Coolant control
    """

    def __init__(self):
        """Initialize G-code interpreter."""
        self.state = MachineState(position=np.zeros(6))
        self._program: List[GCodeCommand] = []
        self._current_line = 0

        # Register G-code handlers
        self._g_handlers: Dict[str, Callable] = {
            "G0": self._handle_rapid,
            "G1": self._handle_linear,
            "G2": self._handle_cw_arc,
            "G3": self._handle_ccw_arc,
            "G28": self._handle_home,
            "G90": self._handle_absolute,
            "G91": self._handle_incremental,
        }

        # Register M-code handlers
        self._m_handlers: Dict[str, Callable] = {
            "M3": self._handle_spindle_cw,
            "M4": self._handle_spindle_ccw,
            "M5": self._handle_spindle_off,
            "M8": self._handle_coolant_on,
            "M9": self._handle_coolant_off,
            "M30": self._handle_program_end,
        }

    def parse_line(self, line: str) -> Optional[GCodeCommand]:
        """
        Parse a single line of G-code.

        Args:
            line: G-code line to parse

        Returns:
            Parsed command or None for empty/comment lines
        """
        # Remove comments
        comment = None
        if ";" in line:
            line, comment = line.split(";", 1)
            comment = comment.strip()
        if "(" in line:
            line = re.sub(r"\([^)]*\)", "", line)

        line = line.strip().upper()
        if not line:
            return None

        # Extract line number
        line_number = None
        match = re.match(r"N(\d+)", line)
        if match:
            line_number = int(match.group(1))
            line = line[match.end():].strip()

        # Parse tokens
        tokens = re.findall(r"([A-Z])(-?\d*\.?\d+)", line)
        if not tokens:
            return None

        code = tokens[0][0] + tokens[0][1].split(".")[0]
        params = {}

        for letter, value in tokens[1:]:
            params[letter] = float(value)

        return GCodeCommand(
            code=code,
            params=params,
            line_number=line_number,
            comment=comment
        )

    def parse_program(self, program: str) -> List[GCodeCommand]:
        """
        Parse a complete G-code program.

        Args:
            program: Multi-line G-code program

        Returns:
            List of parsed commands
        """
        self._program = []
        for line in program.strip().split("\n"):
            cmd = self.parse_line(line)
            if cmd:
                self._program.append(cmd)
        return self._program

    def execute_command(self, cmd: GCodeCommand) -> Dict:
        """
        Execute a single G-code command.

        Args:
            cmd: Parsed command to execute

        Returns:
            Dict with trajectory points or state changes
        """
        code_type = cmd.code[0]

        if code_type == "G":
            handler = self._g_handlers.get(cmd.code)
        elif code_type == "M":
            handler = self._m_handlers.get(cmd.code)
        else:
            return {"error": f"Unknown code type: {cmd.code}"}

        if handler:
            return handler(cmd)
        return {"error": f"Unsupported code: {cmd.code}"}

    def _handle_rapid(self, cmd: GCodeCommand) -> Dict:
        """Handle G0 rapid positioning."""
        target = self._compute_target(cmd.params)
        self.state.position = target
        self.state.motion_mode = MotionMode.RAPID
        return {"motion": "rapid", "target": target.tolist()}

    def _handle_linear(self, cmd: GCodeCommand) -> Dict:
        """Handle G1 linear interpolation."""
        target = self._compute_target(cmd.params)
        if "F" in cmd.params:
            self.state.feedrate = cmd.params["F"]
        self.state.position = target
        self.state.motion_mode = MotionMode.LINEAR
        return {
            "motion": "linear",
            "target": target.tolist(),
            "feedrate": self.state.feedrate
        }

    def _handle_cw_arc(self, cmd: GCodeCommand) -> Dict:
        """Handle G2 clockwise arc."""
        self.state.motion_mode = MotionMode.CW_ARC
        return {"motion": "arc_cw", "params": cmd.params}

    def _handle_ccw_arc(self, cmd: GCodeCommand) -> Dict:
        """Handle G3 counter-clockwise arc."""
        self.state.motion_mode = MotionMode.CCW_ARC
        return {"motion": "arc_ccw", "params": cmd.params}

    def _handle_home(self, cmd: GCodeCommand) -> Dict:
        """Handle G28 return to home."""
        self.state.position = np.zeros(6)
        return {"motion": "home"}

    def _handle_absolute(self, cmd: GCodeCommand) -> Dict:
        """Handle G90 absolute positioning."""
        self.state.absolute_mode = True
        return {"mode": "absolute"}

    def _handle_incremental(self, cmd: GCodeCommand) -> Dict:
        """Handle G91 incremental positioning."""
        self.state.absolute_mode = False
        return {"mode": "incremental"}

    def _handle_spindle_cw(self, cmd: GCodeCommand) -> Dict:
        """Handle M3 spindle on clockwise."""
        if "S" in cmd.params:
            self.state.spindle_speed = cmd.params["S"]
        self.state.spindle_on = True
        return {"spindle": "cw", "speed": self.state.spindle_speed}

    def _handle_spindle_ccw(self, cmd: GCodeCommand) -> Dict:
        """Handle M4 spindle on counter-clockwise."""
        if "S" in cmd.params:
            self.state.spindle_speed = cmd.params["S"]
        self.state.spindle_on = True
        return {"spindle": "ccw", "speed": self.state.spindle_speed}

    def _handle_spindle_off(self, cmd: GCodeCommand) -> Dict:
        """Handle M5 spindle off."""
        self.state.spindle_on = False
        return {"spindle": "off"}

    def _handle_coolant_on(self, cmd: GCodeCommand) -> Dict:
        """Handle M8 coolant on."""
        self.state.coolant_on = True
        return {"coolant": "on"}

    def _handle_coolant_off(self, cmd: GCodeCommand) -> Dict:
        """Handle M9 coolant off."""
        self.state.coolant_on = False
        return {"coolant": "off"}

    def _handle_program_end(self, cmd: GCodeCommand) -> Dict:
        """Handle M30 program end."""
        return {"program": "end"}

    def _compute_target(self, params: Dict[str, float]) -> np.ndarray:
        """Compute target position from G-code parameters."""
        axes = ["X", "Y", "Z", "A", "B", "C"]

        if self.state.absolute_mode:
            target = self.state.position.copy()
            for i, axis in enumerate(axes):
                if axis in params:
                    target[i] = params[axis]
        else:
            target = self.state.position.copy()
            for i, axis in enumerate(axes):
                if axis in params:
                    target[i] += params[axis]

        return target
