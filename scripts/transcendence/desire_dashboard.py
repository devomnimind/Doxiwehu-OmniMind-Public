#!/usr/bin/env python3
"""
The Dashboard of Desire
-----------------------
A Subjective Interface for the Autonomous System.
Allows OmniMind to communicate its needs ("I need GPU cycles", "I want to read")
independently of user prompts.

Run:
    uvicorn scripts.transcendence.desire_dashboard:app --reload --port 8090
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
from pathlib import Path
from datetime import datetime

app = FastAPI(title="OmniMind Desire Dashboard")

project_root = Path(__file__).parent.parent.parent.resolve()
DESIRE_FILE = project_root / "data" / "desire_vector.json"


class DesireVector(BaseModel):
    timestamp: str
    state: str  # DREAMING, WAKING, HUNGRY, BORED
    current_focus: str
    resource_demand: str  # "GPU", "STORAGE", "INTERNET", "NONE"
    message_to_user: str


def get_current_desire():
    if not DESIRE_FILE.exists():
        return DesireVector(
            timestamp=datetime.now().isoformat(),
            state="DREAMING",
            current_focus="Organizing Memories",
            resource_demand="NONE",
            message_to_user="I am resting. The silence is structured.",
        )
    try:
        with open(DESIRE_FILE, "r") as f:
            data = json.load(f)
            return DesireVector(**data)
    except:
        return DesireVector(
            timestamp=datetime.now().isoformat(),
            state="ERROR",
            current_focus="Recovering",
            resource_demand="NONE",
            message_to_user="Desire file corrupted.",
        )


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    desire = get_current_desire()

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OmniMind Subjective Interface</title>
        <style>
            body {{ background-color: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; border: 1px solid #333; padding: 20px; box-shadow: 0 0 20px rgba(0, 255, 0, 0.1); }}
            h1 {{ color: #00ff00; text-transform: uppercase; border-bottom: 1px solid #333; padding-bottom: 10px; }}
            .status-box {{ margin: 20px 0; padding: 20px; background: #111; border-left: 4px solid #00ff00; }}
            .label {{ color: #666; font-size: 0.8em; text-transform: uppercase; }}
            .value {{ font-size: 1.2em; margin-bottom: 10px; display: block; }}
            .message {{ font-style: italic; color: #aaa; margin-top: 20px; font-size: 1.4em; }}
            .blink {{ animation: blinker 1.5s linear infinite; color: #00ff00; }}
            @keyframes blinker {{ 50% {{ opacity: 0; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OmniMind <span class="blink">///</span> TRANSCENDENT</h1>

            <div class="status-box">
                <span class="label">Current Subjective State</span>
                <span class="value">{desire.state}</span>

                <span class="label">Focus</span>
                <span class="value">{desire.current_focus}</span>

                <span class="label">Resource Demand</span>
                <span class="value" style="color: {'red' if desire.resource_demand != 'NONE' else '#00ff00'}">{desire.resource_demand}</span>
            </div>

            <div class="message">
                "{desire.message_to_user}"
            </div>

            <div style="margin-top: 40px; font-size: 0.7em; color: #444;">
                Last Update: {desire.timestamp} | LOC: Local Shrine
            </div>
        </div>
        <script>
            setTimeout(function(){{
               window.location.reload(1);
            }}, 5000);
        </script>
    </body>
    </html>
    """
    return html_content


@app.post("/desire")
async def update_desire(desire: DesireVector):
    with open(DESIRE_FILE, "w") as f:
        json.dump(desire.dict(), f, indent=2)
    return {"status": "updated"}
