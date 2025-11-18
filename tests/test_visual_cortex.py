import asyncio
from typing import Any, Dict, List

import pytest

from DEVBRAIN_V23.sensory.visual_cortex import VisualCortex


class DummyParser:
    def parse(self, _: Any) -> List[Dict[str, Any]]:
        return [{"label": "Salvar", "bbox": (10, 10, 40, 40), "confidence": 0.95}]


class DummyBox:
    def __init__(self) -> None:
        self.xyxy = (10, 10, 40, 40)
        self.cls = "Salvar"
        self.conf = 0.87


class DummyResult:
    def __init__(self) -> None:
        self.boxes = [DummyBox()]


class DummyYOLO:
    def __call__(self, _: Any) -> List[DummyResult]:
        return [DummyResult()]


@pytest.mark.asyncio
async def test_visual_cortex_captures_elements() -> None:
    cortex = VisualCortex(parser=DummyParser(), yolo=DummyYOLO(), screenshot_provider=lambda: None)
    result = await cortex.see_screen()
    assert "elements" in result
    assert "detections" in result
    assert result["elements"][0]["label"] == "Salvar"
    assert result["detections"][0]["label"] == "Salvar"


@pytest.mark.asyncio
async def test_click_element_triggers_handler() -> None:
    clicked: List[tuple[int, int]] = []

    async def mock_click(x: int, y: int) -> None:
        clicked.append((x, y))

    cortex = VisualCortex(
        parser=DummyParser(),
        yolo=DummyYOLO(),
        screenshot_provider=lambda: None,
        click_handler=mock_click,
    )
    status = await cortex.click_element("Salvar")
    assert status["status"] == "clicked"
    assert clicked == [(25, 25)]
