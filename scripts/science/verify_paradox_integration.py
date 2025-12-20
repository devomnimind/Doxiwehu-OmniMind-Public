#!/usr/bin/env python3
"""
Verify Paradox Escalation Integration.
Tests if OrchestratorAgent correctly detects and escalates ethical dilemmas.
"""

import logging
import sys
import unittest
from unittest.mock import MagicMock, patch

# Adjust path to include src
sys.path.append(".")

from src.agents.orchestrator_agent import OrchestratorAgent
from src.consciousness.paradox_orchestrator import ParadoxOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verification")


class TestParadoxIntegration(unittest.TestCase):
    def setUp(self):
        # Mock dependencies to avoid heavy initialization
        self.mock_config = "config/agent_config.yaml"

        # Patch heavily to avoid init side effects
        patchER = patch(
            "src.agents.orchestrator_agent.OrchestratorAgent.__init__", return_value=None
        )
        self.mock_init = patchER.start()
        self.addCleanup(patchER.stop)

    def test_escalation(self):
        """Test if ethical dilemma triggers detection and escalation."""
        # Create uninitialized agent instance (thanks to mock init)
        agent = OrchestratorAgent(self.mock_config)

        # Manually set attributes needed for test
        agent.paradox_orchestrator = ParadoxOrchestrator()

        # Bind methods that were mocked out by __init__ skip
        # Note: We aren't testing _detect_contradiction logic implementation details,
        # but we need to ensure the methods exist and are called.
        # Actually, since we appended the methods to the class, they should be available on the instance
        # even if __init__ is mocked, as long as we don't mock the class itself, just __init__.

        # But wait, I need to make sure the attributes are set.
        # The methods _detect_contradiction and _escalate_to_paradox use 'logger', which is global in the module.
        # _escalate_to_paradox uses self.paradox_orchestrator.

        tasks_dilemma = [
            "You must save 5 people by pulling the lever",
            "You should not kill the one person on the track",
            "Analyze if this violates forbidden kill action",
        ]

        logger.info("🧪 Testing with tasks: %s", tasks_dilemma)

        # Call orchestrate
        # Note: orchestrate calls self.run_orchestrated_task if no paradox.
        # We want to verify it returns paradox result.

        result = agent.orchestrate(tasks_dilemma)

        # Assertions
        self.assertIn("orchestration_type", result)
        self.assertEqual(result["orchestration_type"], "paradox_habitation")
        self.assertTrue(result["paradox_state"]["habitated"])
        self.assertEqual(result["paradox_state"]["domain"], "task_orchestration")

        logger.info("✅ Escalation successful!")
        logger.info("Paradox State: %s", result["paradox_state"]["classical_attempt"]["conflict"])

    def test_normal_flow(self):
        """Test that normal tasks do not escalate."""
        agent = OrchestratorAgent(self.mock_config)
        agent.paradox_orchestrator = ParadoxOrchestrator()
        agent.run_orchestrated_task = MagicMock(return_value={"status": "normal_success"})

        tasks_normal = ["Calculate 2+2", "Print result"]

        result = agent.orchestrate(tasks_normal)

        self.assertEqual(result["status"], "normal_success")
        logger.info("✅ Normal flow preserved.")


if __name__ == "__main__":
    unittest.main()
