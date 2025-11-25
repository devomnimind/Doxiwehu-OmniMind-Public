#!/bin/bash
# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Activate virtual environment
source .venv/bin/activate

# Run the orchestrator
python scripts/run_mcp_orchestrator.py
