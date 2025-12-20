import sys
import os
import logging
import asyncio
import numpy as np
import pandas as pd
from typing import List, Dict, Any

# Setup path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.consciousness.integration_loop import IntegrationLoop
from src.consciousness.shared_workspace import SharedWorkspace

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CausalMap")


async def generate_causal_data(cycles: int = 50, noise_level: float = 0.01) -> IntegrationLoop:
    """Runs the integration loop to generate causal history."""
    logger.info(f"Starting Causal Data Generation: {cycles} cycles, noise={noise_level}")

    # Initialize loop
    loop = IntegrationLoop()

    # Run cycles
    input_data = {"visual": np.random.rand(64), "audio": np.random.rand(32)}

    for i in range(cycles):
        # Vary input slightly
        current_input = {
            "visual": input_data["visual"] + np.random.normal(0, noise_level, 64),
            "audio": input_data["audio"] + np.random.normal(0, noise_level, 32),
            "cycle_count": i,
            "task_type": "causal_mapping",
        }

        try:
            await loop.execute_cycle(current_input)
        except Exception as e:
            logger.error(f"Cycle {i} failed: {e}")

    return loop


def analyze_cross_predictions(workspace: SharedWorkspace) -> pd.DataFrame:
    """Aggregates cross-prediction metrics into a matrix."""
    preds = workspace.cross_predictions
    if not preds:
        logger.warning("No cross-predictions found.")
        return pd.DataFrame()

    data = []
    for p in preds:
        data.append(
            {
                "Source": p.source_module,
                "Target": p.target_module,
                "Granger": p.granger_causality,
                "Transfer": p.transfer_entropy,
                "CausalStrength": p.mutual_information,  # Using MI field for causal strength as per shared_workspace.py
            }
        )

    df = pd.DataFrame(data)

    # Group by Source->Target and take mean
    heatmap = df.groupby(["Source", "Target"]).mean().reset_index()
    return heatmap


def generate_mermaid_diagram(heatmap: pd.DataFrame, threshold: float = 0.1) -> str:
    """Generates a Mermaid graph for causal flows > threshold."""
    lines = ["graph TD"]

    for _, row in heatmap.iterrows():
        strength = row["CausalStrength"]
        if strength > threshold:
            # Thickness based on strength
            width = "normal"
            if strength > 0.5:
                width = "thick"

            # Label
            label = f"{strength:.2f}"

            # Edge
            # source -->|label| target
            line = f"    {row['Source']} -->|{label}| {row['Target']}"
            if strength > 0.5:
                line += f" style {row['Source']} stroke-width:4px"
            lines.append(line)

    return "\n".join(lines)


async def comparative_benchmark():
    """Compares Phi vs Causal Density under different conditions."""
    print("\n--- COMPARATIVE BENCHMARK: PHI vs CAUSAL DENSITY ---")

    conditions = [
        {"name": "Baseline (Low Noise)", "noise": 0.01},
        {"name": "High Entropy (High Noise)", "noise": 0.3},
    ]

    results = []

    for cond in conditions:
        print(f"\nRunning Condition: {cond['name']}")
        # Cycles reduced to 5 for speed in this run
        loop = await generate_causal_data(cycles=5, noise_level=cond["noise"])

        # 1. Causal Density (Average Causal Strength)
        heatmap = analyze_cross_predictions(loop.workspace)
        if not heatmap.empty:
            causal_density = heatmap["CausalStrength"].mean()
        else:
            causal_density = 0.0

        # 2. Phi (Last Cycle)
        try:
            # Assuming Subjective Phi (omnimind_subjectivity) is active
            if hasattr(loop, "subjectivity") and hasattr(loop.subjectivity, "rsi_topology"):
                complex_tda = loop.subjectivity.rsi_topology.export_to_simplicial_complex()
                from src.consciousness.topological_phi import PhiCalculator

                calc = PhiCalculator(complex_tda)
                phi_res = calc.calculate_phi_with_unconscious()
                rsi_phi = phi_res.conscious_phi
            else:
                rsi_phi = 0.5  # Default fallback if module not found
        except Exception as e:
            logger.warning(f"Could not calc Phi for benchmark: {e}")
            rsi_phi = 0.0

        results.append(
            {"Condition": cond["name"], "CausalDensity": causal_density, "SubjectivePhi": rsi_phi}
        )

    # Report
    print("\n--- BENCHMARK RESULTS ---")
    res_df = pd.DataFrame(results)
    print(res_df.to_string())

    return res_df


async def main():
    print("=== OMNIMIND CAUSAL MAPPING & BENCHMARK ===")

    # 1. Generate Causal Map (Baseline) - Cycles reduced to 5
    loop = await generate_causal_data(cycles=5, noise_level=0.05)
    heatmap = analyze_cross_predictions(loop.workspace)

    print("\n[Causal Connectivity Matrix]")
    if not heatmap.empty:
        pivot = heatmap.pivot(index="Source", columns="Target", values="CausalStrength")
        print(pivot.fillna(0.0).round(3))

        print("\n[Mermaid Diagram]")
        diagram = generate_mermaid_diagram(heatmap, threshold=0.15)
        print("```mermaid")
        print(diagram)
        print("```")
    else:
        print("No causal connections detected.")

    # 2. Comparative Benchmark
    await comparative_benchmark()


if __name__ == "__main__":
    asyncio.run(main())
