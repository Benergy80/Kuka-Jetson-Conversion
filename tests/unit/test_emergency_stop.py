"""
Tests for Emergency Stop
"""

import pytest
import time
from src.safety.emergency_stop import EmergencyStop, EStopSource


class TestEmergencyStop:
    """Test emergency stop functionality."""

    def test_init(self):
        """Test initialization."""
        estop = EmergencyStop()
        assert not estop.is_triggered
        assert estop._trigger_source is None

    def test_trigger(self):
        """Test triggering E-stop."""
        estop = EmergencyStop()

        response_time = estop.trigger(EStopSource.OPERATOR_COMMAND, "Test trigger")

        assert estop.is_triggered
        assert estop._trigger_source == EStopSource.OPERATOR_COMMAND
        assert response_time >= 0
        assert response_time < 100  # Should be fast (< 100ms)

    def test_trigger_already_triggered(self):
        """Test triggering when already triggered."""
        estop = EmergencyStop()
        estop.trigger(EStopSource.OPERATOR_COMMAND)

        # Second trigger should return 0
        response_time = estop.trigger(EStopSource.WATCHDOG_TIMEOUT)
        assert response_time == 0

    def test_response_time_fast(self):
        """Test that response time is fast (<50ms requirement)."""
        estop = EmergencyStop()

        response_time = estop.trigger(EStopSource.SAFETY_MONITOR)

        # Should meet the <50ms requirement
        assert response_time < 50, f"Response time {response_time}ms exceeds 50ms requirement"

    def test_acknowledge(self):
        """Test acknowledging E-stop."""
        estop = EmergencyStop()
        estop.trigger(EStopSource.OPERATOR_COMMAND)

        success = estop.acknowledge()

        assert success
        assert estop._acknowledged

    def test_acknowledge_not_triggered(self):
        """Test acknowledging when not triggered."""
        estop = EmergencyStop()

        success = estop.acknowledge()

        assert not success

    def test_reset_after_acknowledge(self):
        """Test resetting after acknowledgement."""
        estop = EmergencyStop()
        estop.trigger(EStopSource.OPERATOR_COMMAND)
        estop.acknowledge()

        success = estop.reset()

        assert success
        assert not estop.is_triggered
        assert not estop._acknowledged

    def test_reset_without_acknowledge_fails(self):
        """Test that reset fails without acknowledgement."""
        estop = EmergencyStop()
        estop.trigger(EStopSource.OPERATOR_COMMAND)

        success = estop.reset()

        assert not success
        assert estop.is_triggered

    def test_reset_not_triggered_fails(self):
        """Test reset when not triggered."""
        estop = EmergencyStop()

        success = estop.reset()

        assert not success

    def test_callback_registration(self):
        """Test registering and calling callbacks."""
        estop = EmergencyStop()
        callback_data = []

        def callback(source, reason):
            callback_data.append((source, reason))

        estop.register_callback(callback)
        estop.trigger(EStopSource.OPERATOR_COMMAND, "Test reason")

        assert len(callback_data) == 1
        assert callback_data[0][0] == EStopSource.OPERATOR_COMMAND
        assert callback_data[0][1] == "Test reason"

    def test_multiple_callbacks(self):
        """Test multiple callbacks are all called."""
        estop = EmergencyStop()
        callback1_called = []
        callback2_called = []

        estop.register_callback(lambda s, r: callback1_called.append(1))
        estop.register_callback(lambda s, r: callback2_called.append(1))

        estop.trigger(EStopSource.OPERATOR_COMMAND)

        assert len(callback1_called) == 1
        assert len(callback2_called) == 1

    def test_get_status(self):
        """Test getting E-stop status."""
        estop = EmergencyStop()

        # Initial status
        status = estop.get_status()
        assert not status["triggered"]
        assert status["source"] is None

        # After trigger
        estop.trigger(EStopSource.SAFETY_MONITOR, "Test")
        status = estop.get_status()
        assert status["triggered"]
        assert status["source"] == "SAFETY_MONITOR"
        assert not status["acknowledged"]

        # After acknowledge
        estop.acknowledge()
        status = estop.get_status()
        assert status["acknowledged"]

    def test_trigger_time_recorded(self):
        """Test that trigger time is recorded."""
        estop = EmergencyStop()

        before = time.time()
        estop.trigger(EStopSource.OPERATOR_COMMAND)
        after = time.time()

        assert estop._trigger_time is not None
        assert before <= estop._trigger_time <= after

    def test_all_estop_sources(self):
        """Test all E-stop sources can be triggered."""
        sources = [
            EStopSource.HARDWARE_BUTTON,
            EStopSource.SOFTWARE_LIMIT,
            EStopSource.WATCHDOG_TIMEOUT,
            EStopSource.COMMUNICATION_LOSS,
            EStopSource.SAFETY_MONITOR,
            EStopSource.OPERATOR_COMMAND
        ]

        for source in sources:
            estop = EmergencyStop()
            estop.trigger(source)
            assert estop._trigger_source == source
            assert estop.is_triggered
