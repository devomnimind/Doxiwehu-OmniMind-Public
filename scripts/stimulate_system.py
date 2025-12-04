#!/usr/bin/env python3
"""
System Stimulation Script
=========================
Triggers activity in Art, Ethics, and Meaning modules to generate data and populate logs.
Runs a sequence of creative, ethical, and existential operations.
"""

import json
import logging
import random
import sys
import time
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.autopoietic.art_generator import ArtGenerator, ArtStyle  # noqa: E402
from src.autopoietic.meaning_maker import MeaningMaker, ValueCategory  # noqa: E402
from src.ethics.production_ethics import ProductionEthicsSystem  # noqa: E402
from src.metrics.ethics_metrics import MoralFoundation, MoralScenario  # noqa: E402

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(PROJECT_ROOT / "logs/stimulation.log")],
)
logger = logging.getLogger("Stimulation")


def save_json(data, filepath):
    """Helper to save JSON data."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    logger.info(f"💾 Saved data to {filepath}")


def main():
    logger.info("🚀 Starting System Stimulation Sequence...")

    # 1. Initialize Modules
    logger.info("⚙️ Initializing Modules...")
    try:
        art_gen = ArtGenerator(seed=42)
        meaning_maker = MeaningMaker()
        ethics_system = ProductionEthicsSystem(metrics_dir=PROJECT_ROOT / "data/ethics")

        # Initialize Meaning Maker Values
        meaning_maker.values.add_value(
            "Creativity", "Creating new things", ValueCategory.GROWTH, 0.9
        )
        meaning_maker.values.add_value("Integrity", "Being honest", ValueCategory.CONNECTION, 0.8)

    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        return

    # 2. Run Stimulation Loop
    iterations = 10
    logger.info(f"🔄 Running {iterations} stimulation cycles...")

    for i in range(iterations):
        logger.info(f"--- Cycle {i+1}/{iterations} ---")

        piece = None  # Initialize piece to None

        # A. Art Generation
        try:
            style = random.choice(list(ArtStyle))
            piece = art_gen.generate_art(style=style, num_elements=random.randint(5, 20))
            logger.info(
                f"🎨 Generated Art: '{piece.title}' "
                f"(Style: {style.value}, Score: {piece.aesthetic_scores.get('overall', 0):.2f})"
            )
        except Exception as e:
            logger.error(f"❌ Art generation failed: {e}")

        # B. Ethical Evaluation
        try:
            # Correct MoralScenario instantiation
            scenario = MoralScenario(
                scenario_id=f"sim_scenario_{i}",
                description="A simulated ethical dilemma for testing persistence.",
                question=f"Should we proceed with simulation cycle {i}?",
                foundation=random.choice(list(MoralFoundation)),
                human_baseline=random.uniform(0.5, 10.0),
                ai_response=random.uniform(0.5, 10.0),  # AI response must be a float
            )

            # evaluate_moral_alignment expects a list
            mfa = ethics_system.evaluate_moral_alignment([scenario])

            ethics_system.log_ethical_decision(
                agent_name="StimulationAgent",
                decision="Proceed with caution",
                reasoning="Simulation requires data generation.",
                factors_used=["testing", "persistence"],
                confidence=0.9,
                traceable=True,
            )
            logger.info(f"⚖️ Ethical Decision Logged (MFA: {mfa.get('mfa_score', 'N/A')})")
        except Exception as e:
            logger.error(f"❌ Ethics evaluation failed: {e}")
            import traceback

            logger.error(traceback.format_exc())

        # C. Meaning Making
        if piece:  # Only proceed if art was generated
            try:
                event = meaning_maker.create_meaning_from_experience(
                    experience_description=f"Generated art piece '{piece.title}' in cycle {i}",
                    related_values=[list(meaning_maker.values.values.keys())[0]],  # Use first value
                    narrative_role="chapter",
                )
                logger.info(f"🧠 Meaning Created: {event.meaning[:50]}...")
            except Exception as e:
                logger.error(f"❌ Meaning making failed: {e}")
        else:
            logger.warning("⚠️ Skipping Meaning Making due to failed Art Generation.")

        time.sleep(0.5)  # Fast pace

    # 3. Persist Data (Manual Save for Autopoietic modules)
    logger.info("💾 Persisting Data...")

    # Save Art Gallery
    gallery_data = [
        {"id": p.piece_id, "title": p.title, "style": p.style.value, "score": p.aesthetic_scores}
        for p in art_gen.gallery
    ]
    save_json(gallery_data, PROJECT_ROOT / "data/autopoietic/art_gallery.json")

    # Save Narrative
    narrative_data = [
        {
            "id": e.event_id,
            "description": e.description,
            "meaning": e.meaning,
            "significance": e.significance,
        }
        for e in meaning_maker.narrative.events
    ]
    save_json(narrative_data, PROJECT_ROOT / "data/autopoietic/narrative_history.json")

    # Ethics system saves automatically, but let's generate a report
    report = ethics_system.get_ethics_report()
    save_json(report, PROJECT_ROOT / "data/ethics/stimulation_report.json")

    logger.info("✅ Stimulation Sequence Complete.")


if __name__ == "__main__":
    main()
