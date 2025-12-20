"""
Verification Script for NPU Governance
"""

import logging
import sys
import os
from unittest.mock import MagicMock

# Adjust path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock dependencies if environment is incomplete
sys.modules["qdrant_client"] = MagicMock()
sys.modules["src.embeddings.code_embeddings"] = MagicMock()

# Inject mocks (removed unused imports)

try:
    from src.governance.npu_metrics import NpuMetrics
except ImportError:
    logger.error("Could not import NpuMetrics")
    sys.exit(1)


def test_npu_metrics():
    logger.info("Testing NpuMetrics...")

    # Mock Qdrant Client
    mock_client = MagicMock()
    # Mock Search Result
    mock_hit = MagicMock()
    mock_hit.score = 0.8
    mock_hit.payload = {"content": "Vizinho relevante"}
    mock_client.search.return_value = [mock_hit, mock_hit]  # 2 neighbors

    # Mock Embeddings
    mock_embeddings = MagicMock()
    mock_embeddings.model.encode.return_value = [0.1] * 384  # 384d vector

    # Patch NpuMetrics to use mocks
    metrics = NpuMetrics()
    metrics.qdrant_client = mock_client
    metrics.embeddings = mock_embeddings

    # Run Measure Impact
    prompt = "O que é consciência?"
    response = "Consciência é a integração de informação em um complexo simplicial."

    # Force loading topological components if possible, or mock them
    # Since we can't easily mock internal imports inside the module without reload,
    # we rely on the module's own fallback or real imports.
    # If real imports fail (e.g. no torch/gpu), Delta Phi will be 0.0, which is fine for this test.

    report = metrics.measure_impact(
        generated_text=response, prompt_context=prompt, latency_ms=1200, model_name="phi-3.5-mini"
    )

    logger.info(f"Report Generated:\n{report.synthesis_log}")

    # Validation
    assert report.entropy_score > 0
    assert "[SINTESE]" in report.synthesis_log
    assert "Phi:" in report.synthesis_log

    logger.info("✅ NPU Metrics Verification Passed")


if __name__ == "__main__":
    test_npu_metrics()
