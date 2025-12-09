"""API routes for Tribunal do Diabo monitoring."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter

from src.services.daemon_monitor import get_cached_status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tribunal", tags=["tribunal"])


def _interpret_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret raw metrics data for visual representation.

    Returns visual interpretations and recommendations.
    """
    attacks_count = metrics.get("attacks_count", 0)
    duration_hours = metrics.get("duration_hours", 0)
    success_rate = metrics.get("success_rate", 0.0)

    # Visual interpretations
    recommendations: List[str] = []
    visual_indicators: Dict[str, str] = {}
    interpretations: Dict[str, Any] = {
        "threat_level": "low",
        "performance_status": "optimal",
        "recommendations": recommendations,
        "visual_indicators": visual_indicators,
    }

    # Threat level assessment
    if attacks_count > 10:
        interpretations["threat_level"] = "critical"
        visual_indicators["threat_color"] = "#ff4444"
        visual_indicators["threat_icon"] = "⚠️"
    elif attacks_count > 5:
        interpretations["threat_level"] = "high"
        visual_indicators["threat_color"] = "#ffaa00"
        visual_indicators["threat_icon"] = "🔴"
    elif attacks_count > 0:
        interpretations["threat_level"] = "medium"
        visual_indicators["threat_color"] = "#ffcc00"
        visual_indicators["threat_icon"] = "🟡"
    else:
        interpretations["threat_level"] = "low"
        visual_indicators["threat_color"] = "#44ff44"
        visual_indicators["threat_icon"] = "🟢"

    # Performance assessment
    if success_rate < 0.5:
        interpretations["performance_status"] = "critical"
        recommendations.append("Melhorar taxa de sucesso - sistema em risco")
    elif success_rate < 0.75:
        interpretations["performance_status"] = "degraded"
        recommendations.append("Otimizar execução de ataques")
    elif success_rate < 0.9:
        interpretations["performance_status"] = "acceptable"
        recommendations.append("Monitorar performance contínuamente")
    else:
        interpretations["performance_status"] = "optimal"
        recommendations.append("Sistema funcionando normalmente")

    # Duration assessment
    if duration_hours > 72:
        recommendations.append(
            "Tribunal em execução prolongada - verificar para bloqueios"
        )

    return interpretations


@router.get("/activity")
async def get_activity() -> Dict[str, Any]:
    """
    Get Tribunal activity and status.

    Returns:
        Dict containing status, activity score, and proposals.
    """
    cache = get_cached_status()
    tribunal_info = cache.get("tribunal_info", {})

    # Calculate a synthetic activity score based on attacks executed
    attacks_executed = tribunal_info.get("attacks_executed", 0)
    activity_score = min(1.0, attacks_executed * 0.25)  # 4 attacks = 1.0

    status = tribunal_info.get("status") or "unknown"

    # Generate proposals based on status
    proposals = []
    if status == "running":
        proposals.append(
            {
                "id": "wait_completion",
                "title": "Aguardar Conclusão",
                "description": "O Tribunal está em execução. Aguarde o relatório final.",
                "severity": "info",
            }
        )
    elif status == "finished":
        compatible = tribunal_info.get("consciousness_compatible", False)
        if compatible:
            proposals.append(
                {
                    "id": "approve_integration",
                    "title": "Aprovar Integração",
                    "description": "Sistema compatível com consciência. Integração recomendada.",
                    "severity": "success",
                }
            )
        else:
            proposals.append(
                {
                    "id": "review_architecture",
                    "title": "Revisar Arquitetura",
                    "description": "Sistema vulnerável ou incompatível. Revisão necessária.",
                    "severity": "warning",
                }
            )

    return {
        "status": status,
        "activity_score": activity_score,
        "proposals": proposals,
        "details": tribunal_info,
        "metrics": {
            "attacks_count": attacks_executed,
            "duration_hours": tribunal_info.get("duration_hours", 0),
        },
    }


@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get detailed Tribunal metrics with visual interpretation.

    Returns:
        Dict containing raw metrics, interpretations, and visual data.
    """
    cache = get_cached_status()
    tribunal_info = cache.get("tribunal_info", {})

    # Raw metrics
    metrics = {
        "attacks_count": tribunal_info.get("attacks_executed", 0),
        "attacks_successful": tribunal_info.get("attacks_successful", 0),
        "attacks_failed": tribunal_info.get("attacks_failed", 0),
        "duration_hours": tribunal_info.get("duration_hours", 0),
        "consciousness_compatible": tribunal_info.get("consciousness_compatible", False),
        "status": tribunal_info.get("status") or "unknown",
        "last_attack_type": tribunal_info.get("last_attack_type", "none"),
        "error_count": tribunal_info.get("error_count", 0),
    }

    # Calculate success rate
    total_attacks = metrics["attacks_count"]
    success_rate = metrics["attacks_successful"] / total_attacks if total_attacks > 0 else 0.0
    metrics["success_rate"] = success_rate

    # Get interpretations
    interpretations = _interpret_metrics(metrics)

    # Build visualization data
    visualization = {
        "charts": {
            "attack_distribution": {
                "type": "doughnut",
                "data": {
                    "labels": ["Successful", "Failed"],
                    "values": [metrics["attacks_successful"], metrics["attacks_failed"]],
                    "colors": ["#44ff44", "#ff4444"],
                },
            },
            "threat_gauge": {
                "type": "gauge",
                "value": min(100, metrics["attacks_count"] * 10),
                "max": 100,
                "color": interpretations["visual_indicators"]["threat_color"],
            },
            "performance_timeline": {
                "type": "line",
                "label": "Success Rate Over Time",
                "current_value": success_rate * 100,
                "color": "#00aaff",
            },
        },
        "status_indicators": {
            "threat_level": {
                "value": interpretations["threat_level"],
                "color": interpretations["visual_indicators"]["threat_color"],
                "icon": interpretations["visual_indicators"]["threat_icon"],
            },
            "performance": {
                "value": interpretations["performance_status"],
                "color": (
                    "#00aaff" if interpretations["performance_status"] == "optimal" else "#ffaa00"
                ),
                "icon": "✅" if interpretations["performance_status"] == "optimal" else "⚠️",
            },
            "consciousness_compatibility": {
                "value": "Compatible" if metrics["consciousness_compatible"] else "Incompatible",
                "color": "#44ff44" if metrics["consciousness_compatible"] else "#ff4444",
                "icon": "✅" if metrics["consciousness_compatible"] else "❌",
            },
        },
        "summary_metrics": {
            "total_attacks": metrics["attacks_count"],
            "success_rate_percent": round(success_rate * 100, 1),
            "duration_hours": metrics["duration_hours"],
            "error_count": metrics["error_count"],
        },
    }

    return {
        "raw_metrics": metrics,
        "interpretations": interpretations,
        "visualization": visualization,
        "timestamp": tribunal_info.get("last_update", ""),
    }
