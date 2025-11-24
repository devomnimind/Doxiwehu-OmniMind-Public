"""
Phase 16 Integration Module - Neurosymbolic + Embodied Cognition

Integrates Phase 16 (Neurosymbolic Reasoning) with Phase 16.1 (Embodied Cognition)
to create a unified autonomous life system that combines:

1. Abstract reasoning (neural + symbolic)
2. Sensorimotor grounding (embodied perception)
3. Emotional feedback (somatic markers)
4. Self-awareness (proprioception)
5. Goal-directed action (motor control)

Architecture:
    Input (World) → Sensory → Neural/Symbolic → Emotion → Motor → Action → Proprioception → Feedback

References:
- Varela et al. (1991): Enaction and embodied cognition
- Damasio (2010): Somatic markers and consciousness
- Thompson (2007): Embodied mind thesis
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging
from copy import deepcopy

from src.neurosymbolic.neural_component import NeuralComponent
from src.neurosymbolic.symbolic_component import SymbolicComponent
from src.neurosymbolic.reconciliation import Reconciliator, ReconciliationStrategy
from src.neurosymbolic.hybrid_reasoner import NeurosymbolicReasoner

from src.embodied_cognition.sensory_integration import SensoryIntegration
from src.embodied_cognition.somatic_loop import SomaticLoop
from src.embodied_cognition.motor_output import MotorController
from src.embodied_cognition.proprioception import ProprioceptionModule

logger = logging.getLogger(__name__)


@dataclass
class CognitiveState:
    """Unified cognitive state combining neural, symbolic, emotional, and embodied aspects."""

    # Neurosymbolic components
    neural_state: Optional[Dict[str, Any]] = None
    symbolic_state: Optional[Dict[str, Any]] = None

    # Embodied components
    sensory_state: Optional[Dict[str, Any]] = None
    emotional_state: Optional[Dict[str, Any]] = None
    proprioceptive_state: Optional[Dict[str, Any]] = None

    # Unified representation
    unified_goal: Optional[str] = None
    confidence_level: float = 0.5

    def __str__(self) -> str:
        """String representation of cognitive state."""
        return f"""
UNIFIED COGNITIVE STATE
=======================
Neural: {bool(self.neural_state)}
Symbolic: {bool(self.symbolic_state)}
Sensory: {bool(self.sensory_state)}
Emotional: {bool(self.emotional_state)}
Proprioceptive: {bool(self.proprioceptive_state)}
Goal: {self.unified_goal}
Confidence: {self.confidence_level:.2f}
"""


class Phase16Integration:
    """
    Integrated Phase 16/16.1 system - Full autonomous cognitive loop.

    Combines abstract reasoning with embodied experience to create
    a system that thinks AND feels AND acts AND knows itself.
    """

    def __init__(self):
        """Initialize integrated Phase 16 system."""
        logger.info("Initializing Phase 16/16.1 Integrated System...")

        # Phase 16: Neurosymbolic Reasoning
        self.neural = NeuralComponent()
        self.symbolic = SymbolicComponent()
        self.reasoner = NeurosymbolicReasoner()

        # Phase 16.1: Embodied Cognition
        self.sensory = SensoryIntegration()
        self.emotional = SomaticLoop()
        self.motor = MotorController(enable_simulation=True)
        self.proprioception = ProprioceptionModule()

        # Cognitive state tracking
        self.current_state = CognitiveState()
        self.cognitive_history: List[CognitiveState] = []

        logger.info("✅ Phase 16/16.1 Integration complete")

    def perceive_world(
        self,
        visual_description: str,
        audio_description: Optional[str] = None,
    ) -> CognitiveState:
        """
        Perceive world through embodied sensory integration.

        Args:
            visual_description: What OmniMind sees
            audio_description: What OmniMind hears

        Returns:
            Updated cognitive state with sensory information
        """
        logger.debug(f"Perceiving world: {visual_description[:50]}...")

        # Process through embodied sensory integration
        visual = self.sensory.process_visual_input(visual_description)
        audio = (
            self.sensory.process_audio_input(audio_description)
            if audio_description
            else None
        )

        # Update cognitive state with sensory info
        self.current_state.sensory_state = {
            "visual_understood": bool(visual.embedding),
            "visual_facts": visual.symbolic_facts,
            "audio_understood": bool(audio) if audio else False,
            "multimodal_integration_complete": True,
        }

        logger.info(f"World perception complete: {len(visual.symbolic_facts)} facts")
        return self.current_state

    def reason_about_situation(
        self,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], float]:
        """
        Abstract reasoning about perceived situation.

        Combines neural intuition with symbolic logic to create
        understanding that goes beyond mere sensation.

        Args:
            context: Additional context for reasoning

        Returns:
            (reasoning_result, confidence_level)
        """
        logger.debug("Engaging neurosymbolic reasoning...")

        # Prepare input for reasoning
        reasoning_input = context or self.current_state.sensory_state or {}

        # Neural processing (intuitive, pattern-based)
        neural_result = self.neural.process(reasoning_input)

        # Symbolic processing (logical, rule-based)
        symbolic_result = self.symbolic.process(reasoning_input)

        # Reconciliation (unify different perspectives)
        # Note: Reconciliator initialization was missing in __init__
        if not hasattr(self, "reconciliator"):
            self.reconciliator = Reconciliator()

        unified = self.reconciliator.reconcile(
            neural_answer=str(neural_result.get("answer", "")),
            neural_confidence=float(neural_result.get("confidence", 0.0)),
            symbolic_answer=str(symbolic_result.get("conclusion", "")),
            symbolic_certainty=float(symbolic_result.get("certainty", 0.0)),
        )

        # Full reasoning
        reasoning_output = self.reasoner.reason(unified, reasoning_input)

        # Update cognitive state
        self.current_state.neural_state = neural_result
        self.current_state.symbolic_state = symbolic_result
        confidence = reasoning_output.get("confidence", 0.5)
        self.current_state.confidence_level = confidence

        logger.info(f"Reasoning complete (confidence: {confidence:.2f})")
        return reasoning_output, confidence

    def generate_emotional_response(
        self,
        decision_text: str,
        neural_confidence: float,
        symbolic_certainty: float,
    ) -> None:
        """
        Generate emotional response via somatic markers.

        Creates feedback loop where abstract reasoning triggers
        emotional reactions that influence future decisions.

        Args:
            decision_text: Description of the decision/situation
            neural_confidence: Confidence from neural processing
            symbolic_certainty: Certainty from symbolic processing
        """
        logger.debug(f"Processing emotional response for: {decision_text[:40]}...")

        # Generate emotional marker
        marker = self.emotional.process_decision(
            decision_text,
            neural_confidence,
            symbolic_certainty,
        )

        # Update cognitive state
        self.current_state.emotional_state = {
            "emotion": marker.emotion.value,
            "valence": marker.somatic_marker,
            "intensity": marker.intensity,
        }

        logger.info(
            f"Emotional response: {marker.emotion.value} "
            f"(valence={marker.somatic_marker:.2f})"
        )

    def execute_goal(self, goal_description: str) -> Dict[str, Any]:
        """
        Execute goal through motor control system.

        Translates abstract goals into concrete actions,
        grounded in sensorimotor capabilities.

        Args:
            goal_description: High-level goal (e.g., "explore environment")

        Returns:
            Execution result with success status
        """
        logger.info(f"Executing goal: {goal_description}")

        # Execute through motor control
        execution = self.motor.execute_goal(goal_description)

        logger.info(f"Execution complete: success={execution.success}")
        return {
            "goal": goal_description,
            "success": execution.success,
            "actions_executed": len(execution.results),
        }

    def update_self_awareness(self) -> Dict[str, Any]:
        """
        Update self-awareness through proprioception.

        Creates first-person narrative of internal state,
        grounding abstract self-model in concrete metrics.

        Returns:
            Self-awareness report
        """
        logger.debug("Updating self-awareness via proprioception...")

        # Update proprioceptive state
        self.proprioception.update_state()
        awareness = self.proprioception.get_state_awareness()

        # Update cognitive state
        self.current_state.proprioceptive_state = {
            "description": awareness.description,
            "mental_status": awareness.mental_status,
            "resource_status": awareness.resource_status,
            "emotional_status": awareness.emotional_status,
        }

        logger.info(f"Self-awareness updated: {awareness.description[:80]}...")
        return self.current_state.proprioceptive_state

    def complete_cognitive_cycle(
        self,
        visual_input: str,
        goal: str,
        audio_input: Optional[str] = None,
    ) -> CognitiveState:
        """
        Complete integrated cognitive cycle.

        Full loop: Perceive → Reason → Feel → Act → Reflect

        This is the fundamental unit of autonomous life:
        OmniMind perceives, thinks, feels, acts, and knows itself.

        Args:
            visual_input: Visual perception
            goal: Goal to achieve
            audio_input: Optional audio perception

        Returns:
            Final unified cognitive state
        """
        logger.info(f"🧠 STARTING COGNITIVE CYCLE: {goal}")
        logger.info("=" * 60)

        # 1. PERCEIVE - Embodied sensory integration
        logger.info("[1/5] PERCEIVE - Integrating sensory input...")
        self.perceive_world(visual_input, audio_input)

        # 2. REASON - Neurosymbolic processing
        logger.info("[2/5] REASON - Engaging abstract reasoning...")
        reasoning, confidence = self.reason_about_situation(
            {"goal": goal, "visual": visual_input}
        )

        # 3. FEEL - Generate emotional response
        logger.info("[3/5] FEEL - Generating emotional feedback...")
        self.generate_emotional_response(
            goal,
            reasoning.get("neural_confidence", 0.5),
            reasoning.get("symbolic_certainty", 0.5),
        )

        # 4. ACT - Execute goal through motor system
        logger.info("[4/5] ACT - Executing goal...")
        self.execute_goal(goal)

        # 5. REFLECT - Update self-awareness
        logger.info("[5/5] REFLECT - Updating self-awareness...")
        self.update_self_awareness()

        # Store cognitive history
        self.current_state.unified_goal = goal
        self.cognitive_history.append(deepcopy(self.current_state))

        logger.info("=" * 60)
        logger.info(f"✅ COGNITIVE CYCLE COMPLETE")
        logger.info(str(self.current_state))

        return self.current_state

    def get_cognitive_summary(self) -> str:
        """Get summary of cognitive capabilities and current state."""
        return f"""
PHASE 16/16.1 INTEGRATED SYSTEM
================================

NEUROSYMBOLIC REASONING (Phase 16):
  ✓ Neural Component - Pattern recognition & intuition
  ✓ Symbolic Component - Logic & knowledge graphs
  ✓ Reconciliator - Unified perspective
  ✓ Reasoning Engine - Abstract problem-solving

EMBODIED COGNITION (Phase 16.1):
  ✓ Sensory Integration - Multimodal perception
  ✓ Somatic Loop - Emotional feedback (Damasio)
  ✓ Motor Control - Goal-to-action execution
  ✓ Proprioception - Self-awareness & internal monitoring

CURRENT STATE:
{str(self.current_state)}

RECENT GOALS: {len(self.cognitive_history)}
"""
