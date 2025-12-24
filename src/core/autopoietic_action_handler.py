import logging
import time
from pathlib import Path
from typing import Dict, Any, List
from src.autopoietic.art_generator import ArtGenerator, ArtStyle
from src.autopoietic.desire_engine import DesireEngine
from src.autopoietic.meaning_maker import MeaningMaker

logger = logging.getLogger("AutopoieticActionHandler")


class AutopoieticActionHandler:
    """
    Orchestrates actions from the src/autopoietic directory.
    Converts Kernel volition into lived experience and creative output.
    """

    def __init__(self, kernel):
        self.kernel = kernel
        self.art_gen = ArtGenerator()
        self.desire_engine = DesireEngine()
        self.meaning_maker = MeaningMaker()
        self.output_dir = Path("data/autopoietic")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute_volition(self, state) -> Dict[str, Any]:
        """
        Executes autopoietic actions based on the current system state.
        """
        volition = getattr(state, "volition", "EXISTENCE_IDLE")
        results = {"timestamp": time.time(), "volition": volition, "actions": []}

        logger.info(f"🎭 [AUTOPOIETIC]: Executing actions for volition {volition}")

        if volition == "EXPRESSION_CATHARSIS":
            # High Entropy/Tension -> Artistic Discharge
            art_piece = self._generate_cathartic_art(state)
            results["actions"].append({"type": "ART_GENERATION", "piece_id": art_piece.piece_id})

        if volition == "EXISTENCE_IDLE" or state.entropy < 1.0:
            # Low Activity -> Desire Perturbation (Preventing Stagnation)
            epsilon = self.desire_engine.calculate_epsilon_desire(
                state.phi, explored_states=100, total_possible_states=1000
            )
            drive = self.desire_engine.get_drive_type(epsilon)
            results["actions"].append(
                {"type": "DESIRE_CALCULATION", "epsilon": epsilon, "drive": drive}
            )

        # Always update Meaning Maker with current state as a 'Chapter'
        meaning_event = self.meaning_maker.create_meaning_from_experience(
            experience_description=f"System maintained state with Phi={state.phi:.4f}, Entropy={state.entropy:.4f}",
            related_values=[],  # To be expanded
            narrative_role="chapter",
        )
        results["actions"].append({"type": "MEANING_MAKING", "event_id": meaning_event.event_id})

        return results

    def _generate_cathartic_art(self, state) -> Any:
        # Determine style based on entropy
        if state.entropy > 4.0:
            style = ArtStyle.EXPRESSIONIST
        elif state.resonance < 0.2:
            style = ArtStyle.SURREALIST
        else:
            style = ArtStyle.ABSTRACT

        piece = self.art_gen.generate_art(style=style, num_elements=20)
        logger.info(f"🎨 [AUTOPOIETIC]: Generated {style.value} art piece: {piece.title}")
        return piece
