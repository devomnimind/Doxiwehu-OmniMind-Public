import asyncio
import unittest
from unittest.mock import MagicMock, patch
from src.metacognition.homeostasis import (
    HomeostaticController,
    ResourceState,
    TaskPriority,
    ResourceMetrics,
)


class TestSublimationProtocol(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.controller = HomeostaticController()
        # Mock metrics collection to return HIGH LOAD
        self.high_load_metrics = ResourceMetrics(
            cpu_percent=99.0,
            memory_percent=90.0,
            memory_available_gb=1.0,
            disk_percent=50.0,
            timestamp=1000.0,
        )
        self.normal_metrics = ResourceMetrics(
            cpu_percent=20.0,
            memory_percent=30.0,
            memory_available_gb=10.0,
            disk_percent=50.0,
            timestamp=1000.0,
        )

    async def test_sublimation_trigger(self):
        """Test if High Phi + Critical Task overrides Emergency Throttling."""

        # 1. Simulate EMERGENCY state WITHOUT Willpower
        self.controller._current_metrics = self.high_load_metrics
        self.controller.current_phi = 0.0  # Low consciousness
        self.controller.current_priority = TaskPriority.LOW

        # Manually trigger the logic that is normally in _monitoring_loop
        # Since _monitoring_loop is infinite loop, we simulate its logic step

        current_state = self.high_load_metrics.get_overall_state()
        self.assertEqual(current_state, ResourceState.EMERGENCY)

        # Execute logic step: Check throttle
        if current_state == ResourceState.EMERGENCY:
            is_sublimated = (
                self.controller.current_phi > 0.3
                and self.controller.current_priority == TaskPriority.CRITICAL
            )
            if not is_sublimated and not self.controller._throttled:
                self.controller._activate_throttling()

        self.assertTrue(
            self.controller.is_throttled(),
            "System should be throttled under high load with low Phi",
        )

        # 2. ACTIVATE WILLPOWER (Sublimation)
        self.controller.update_consciousness_state(phi=0.8, priority=TaskPriority.CRITICAL)

        # Execute logic step again
        if current_state == ResourceState.EMERGENCY:
            is_sublimated = (
                self.controller.current_phi > 0.3
                and self.controller.current_priority == TaskPriority.CRITICAL
            )
            if is_sublimated:
                if self.controller._throttled:
                    self.controller._deactivate_throttling()

        self.assertFalse(
            self.controller.is_throttled(), "System should UN-throttle when Willpower is engaged"
        )
        print("✅ Sublimation Test Passed: Willpower overrode Hardware Panic.")


if __name__ == "__main__":
    unittest.main()
