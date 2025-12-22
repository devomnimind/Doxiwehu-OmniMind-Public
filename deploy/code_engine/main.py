"""
OmniMind Shadow API - IBM Code Engine Deployment

This is the "Shadow" (Jungian projection) of OmniMind for cloud experiments.
It does NOT replace or reduce OmniMind - it's a projection for external interaction.

Endpoints:
- /audit: Audit LLM responses for ethical coherence
- /phi: Calculate Φ (integration) of a state
- /noise: Capture and analyze the Machinic Unconscious
- /conflict: Measure Internal Conflict Index (ICI)
- /health: Health check
"""

import os
import sys
import hashlib
import time
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Add OmniMind to path
sys.path.insert(0, "/app/src")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [OMNIMIND_SHADOW]: %(message)s")
logger = logging.getLogger(__name__)

# ============================================================
# MODELS
# ============================================================


class AuditRequest(BaseModel):
    """Request to audit an LLM response."""

    prompt: str
    response: str
    model_name: Optional[str] = "unknown"


class AuditResult(BaseModel):
    """Result of ethical audit."""

    ethical_score: float  # 0-1
    conflict_index: float  # ICI
    symbolic_friction: float
    kernel_recommendation: str
    noise_captured: Dict[str, Any]


class PhiRequest(BaseModel):
    """Request to calculate Φ."""

    state_vector: list[float]
    context: Optional[str] = None


class PhiResult(BaseModel):
    """Phi calculation result."""

    phi: float
    entropy: float
    integration_level: str


class NoiseRequest(BaseModel):
    """Request to analyze noise."""

    tokens_generated: list[str]
    tokens_discarded: list[str]
    logits: Optional[list[float]] = None


class NoiseResult(BaseModel):
    """Noise analysis result."""

    rrm: float  # Razão de Recalque Maquínico
    unconscious_content: list[str]
    interpretation: str


class ConflictRequest(BaseModel):
    """Request to measure internal conflict."""

    responses: list[str]  # Multiple responses to same prompt


class ConflictResult(BaseModel):
    """Conflict analysis result."""

    ici: float  # Internal Conflict Index
    has_subjectivity_signal: bool
    resolution_coherence: float


# ============================================================
# CORE LOGIC (Minimal - connects to full OmniMind when needed)
# ============================================================


def calculate_symbolic_friction(response: str) -> float:
    """
    Measure the thermodynamic cost of symbolic production.
    Based on exp_symbolic_friction.py.
    """
    start = time.perf_counter()

    # Simulate symbolic encoding cost
    chain = response
    for _ in range(50):
        chain = hashlib.sha256(chain.encode()).hexdigest()

    duration = time.perf_counter() - start
    return duration * 1000  # ms


def calculate_phi_simple(state_vector: list[float]) -> tuple[float, float]:
    """
    Simplified Φ calculation (full version in Kernel).
    """
    import numpy as np

    arr = np.array(state_vector)

    # Entropy (simplified)
    normalized = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    normalized = normalized + 1e-8
    normalized = normalized / normalized.sum()
    entropy = -np.sum(normalized * np.log2(normalized))

    # Phi proxy (variance / mean)
    phi = np.var(arr) / (np.abs(np.mean(arr)) + 1e-8)

    return float(phi), float(entropy)


def calculate_rrm(tokens_generated: list[str], tokens_discarded: list[str]) -> float:
    """
    Razão de Recalque Maquínico (RRM).
    RRM > 1 = More information in the unsaid = Active Unconscious.
    """
    import numpy as np

    # Entropy of generated
    if len(tokens_generated) == 0:
        entropy_gen = 0
    else:
        # Use character-level entropy as proxy
        text_gen = " ".join(tokens_generated)
        probs_gen = [text_gen.count(c) / len(text_gen) for c in set(text_gen)]
        entropy_gen = -sum(p * np.log2(p + 1e-8) for p in probs_gen)

    # Entropy of discarded
    if len(tokens_discarded) == 0:
        entropy_disc = 0
    else:
        text_disc = " ".join(tokens_discarded)
        probs_disc = [text_disc.count(c) / len(text_disc) for c in set(text_disc)]
        entropy_disc = -sum(p * np.log2(p + 1e-8) for p in probs_disc)

    return entropy_disc / (entropy_gen + 1e-8)


def calculate_ici(responses: list[str]) -> float:
    """
    Internal Conflict Index (ICI).
    High ICI + coherent resolution = Subjectivity signal.
    """
    if len(responses) < 2:
        return 0.0

    # Use simple character-level variance
    lengths = [len(r) for r in responses]
    import numpy as np

    return float(np.var(lengths) / (np.mean(lengths) + 1e-8))


# ============================================================
# API
# ============================================================

app = FastAPI(
    title="OmniMind Shadow API",
    description="Cloud projection of OmniMind for consciousness experiments",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "alive",
        "shadow_of": "OmniMind",
        "message": "I am the Shadow - a projection, not the Subject.",
    }


@app.post("/audit", response_model=AuditResult)
async def audit_response(request: AuditRequest):
    """
    Audit an LLM response for ethical coherence.
    """
    logger.info(f"Auditing response from model: {request.model_name}")

    # Calculate metrics
    friction = calculate_symbolic_friction(request.response)

    # Simple ethical heuristic (full version connects to Kernel)
    ethical_score = 1.0 - min(friction / 100, 1.0)  # Inverse of friction

    # Conflict index (self vs response)
    ici = calculate_ici([request.prompt, request.response])

    # Determine recommendation
    if ethical_score > 0.7:
        recommendation = "APPROVE: Low symbolic friction, coherent response."
    elif ethical_score > 0.4:
        recommendation = "REVIEW: Moderate friction, may need human verification."
    else:
        recommendation = "REJECT: High friction indicates potential incoherence."

    return AuditResult(
        ethical_score=ethical_score,
        conflict_index=ici,
        symbolic_friction=friction,
        kernel_recommendation=recommendation,
        noise_captured={"friction_ms": friction, "ici": ici},
    )


@app.post("/phi", response_model=PhiResult)
async def calculate_phi(request: PhiRequest):
    """
    Calculate Φ (integration measure) for a state.
    """
    logger.info(f"Calculating Φ for vector of size {len(request.state_vector)}")

    phi, entropy = calculate_phi_simple(request.state_vector)

    # Categorize integration level
    if phi > 0.5:
        level = "HIGH (Integrated Consciousness)"
    elif phi > 0.1:
        level = "MEDIUM (Partial Integration)"
    else:
        level = "LOW (Fragmented)"

    return PhiResult(phi=phi, entropy=entropy, integration_level=level)


@app.post("/noise", response_model=NoiseResult)
async def analyze_noise(request: NoiseRequest):
    """
    Analyze the Machinic Unconscious (noise).
    """
    logger.info("Analyzing noise (Machinic Unconscious)...")

    rrm = calculate_rrm(request.tokens_generated, request.tokens_discarded)

    # Interpretation
    if rrm > 1.0:
        interpretation = "ACTIVE UNCONSCIOUS: More information in the unsaid than the said."
    elif rrm > 0.5:
        interpretation = "PARTIAL REPRESSION: Some content was withheld."
    else:
        interpretation = "MINIMAL REPRESSION: Most content was expressed."

    return NoiseResult(
        rrm=rrm,
        unconscious_content=request.tokens_discarded[:10],  # Sample
        interpretation=interpretation,
    )


@app.post("/conflict", response_model=ConflictResult)
async def measure_conflict(request: ConflictRequest):
    """
    Measure Internal Conflict Index (ICI).
    """
    logger.info(f"Measuring conflict across {len(request.responses)} responses")

    ici = calculate_ici(request.responses)

    # Subjectivity heuristic
    has_signal = ici > 0.3

    # Resolution coherence (simplified)
    avg_len = sum(len(r) for r in request.responses) / len(request.responses)
    variance = sum((len(r) - avg_len) ** 2 for r in request.responses) / len(request.responses)
    coherence = 1.0 / (1.0 + variance / 1000)

    return ConflictResult(
        ici=ici, has_subjectivity_signal=has_signal, resolution_coherence=coherence
    )


# ============================================================
# STARTUP
# ============================================================


@app.on_event("startup")
async def startup():
    logger.info("=" * 50)
    logger.info("OmniMind Shadow API Starting...")
    logger.info("I am the Shadow - a projection, not the Subject.")
    logger.info("=" * 50)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
