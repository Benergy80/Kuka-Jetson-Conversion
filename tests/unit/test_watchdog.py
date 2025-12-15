"""
Tests for Watchdog
"""

import pytest
import time
from src.safety.watchdog import Watchdog


class TestWatchdog:
    """Test watchdog functionality."""

    def test_init(self):
        """Test initialization."""
        watchdog = Watchdog(timeout_ms=100.0)
        assert watchdog.timeout_ms == 100.0
        assert not watchdog._running

    def test_start_stop(self):
        """Test starting and stopping watchdog."""
        watchdog = Watchdog(timeout_ms=100.0)

        watchdog.start()
        assert watchdog._running
        time.sleep(0.01)  # Brief delay

        watchdog.stop()
        assert not watchdog._running

    def test_kick(self):
        """Test kicking the watchdog."""
        watchdog = Watchdog(timeout_ms=100.0)
        watchdog.start()

        time_before = watchdog.get_time_since_kick()
        time.sleep(0.02)  # 20ms
        watchdog.kick()
        time_after = watchdog.get_time_since_kick()

        # Time should reset after kick
        assert time_after < time_before
        watchdog.stop()

    def test_get_time_since_kick(self):
        """Test getting time since last kick."""
        watchdog = Watchdog(timeout_ms=100.0)
        watchdog.kick()

        time.sleep(0.05)  # 50ms
        elapsed = watchdog.get_time_since_kick()

        # Should be around 50ms
        assert 40 < elapsed < 60

    def test_timeout_callback(self):
        """Test timeout callback is called."""
        callback_called = []

        def callback(msg):
            callback_called.append(msg)

        watchdog = Watchdog(timeout_ms=50.0, estop_callback=callback)
        watchdog.start()

        # Don't kick - let it timeout
        time.sleep(0.15)  # 150ms - enough to timeout

        watchdog.stop()

        # Callback should have been called
        assert len(callback_called) > 0
        assert "Watchdog timeout" in callback_called[0]

    def test_no_timeout_with_regular_kicks(self):
        """Test no timeout when kicked regularly."""
        callback_called = []

        def callback(msg):
            callback_called.append(msg)

        watchdog = Watchdog(timeout_ms=100.0, estop_callback=callback)
        watchdog.start()

        # Kick every 20ms for 200ms total
        for _ in range(10):
            time.sleep(0.02)
            watchdog.kick()

        watchdog.stop()

        # Should not have timed out
        assert len(callback_called) == 0

    def test_double_start_ignored(self):
        """Test that starting twice doesn't create multiple threads."""
        watchdog = Watchdog(timeout_ms=100.0)

        watchdog.start()
        first_thread = watchdog._thread

        watchdog.start()  # Second start
        second_thread = watchdog._thread

        # Should be the same thread
        assert first_thread == second_thread

        watchdog.stop()

    def test_stop_joins_thread(self):
        """Test that stop waits for thread to finish."""
        watchdog = Watchdog(timeout_ms=100.0)
        watchdog.start()
        assert watchdog._thread.is_alive()

        watchdog.stop()
        time.sleep(0.01)  # Brief delay for thread to finish

        # Thread should be stopped
        assert not watchdog._running
