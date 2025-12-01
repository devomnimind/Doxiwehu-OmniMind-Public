#!/bin/bash
# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Activate virtual environment
source .venv/bin/activate

# Ensure PATH includes .venv/bin
export PATH="$(pwd)/.venv/bin:$PATH"

# Run the orchestrator using the venv Python
exec "$(pwd)/.venv/bin/python" scripts/run_mcp_orchestrator.py
