from fastapi import APIRouter


router = APIRouter()


@router.get("/status")
async def get_autopoietic_status():
    return {
        "running": True,
        "cycle_count": 42,
        "component_count": 7,
        "current_phi": 1.0,
        "phi_threshold": 0.3,
    }


@router.get("/cycles")
async def get_autopoietic_cycles(limit: int = 50):
    return {"cycles": [], "total": 0}


@router.get("/consciousness/metrics")
async def get_consciousness_metrics():
    return {"phi": 1.0, "anxiety": 0.1, "flow": 0.9, "entropy": 0.2, "ici": 0.95, "prs": 0.88}


@router.get("/extended/metrics")
async def get_extended_metrics():
    try:
        import json
        from pathlib import Path

        path = Path("data/monitor/real_metrics.json")
        if path.exists():
            data = json.loads(path.read_text())
            # Map simple metrics to extended format if needed, or just return merged
            return {
                "phi": data.get("phi", 0.0),
                "psi": data.get("psi", 0.5),  # Default logic or real if available
                "sigma": data.get("sigma", 0.1),
                "gozo": data.get("gozo", 0.2),
                "anxiety": data.get("anxiety", 0.0),
                "timestamp": data.get("timestamp", 0),
            }
    except Exception:
        pass

    return {"phi": 1.0, "psi": 0.7, "sigma": 0.05, "gozo": 0.2, "delta": 0.1}
