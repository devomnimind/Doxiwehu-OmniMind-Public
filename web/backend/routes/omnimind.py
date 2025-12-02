"""API routes for OmniMind specific functionality."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/omnimind", tags=["omnimind"])


@router.get("/messages", response_model=List[Dict[str, Any]])
async def get_messages() -> List[Dict[str, Any]]:
    """
    Get recent system messages.
    
    Returns a list of messages from the system.
    """
    # TODO: Connect to actual message bus or log storage
    # For now, return an empty list to satisfy the API contract
    return []
