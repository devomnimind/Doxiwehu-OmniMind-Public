#!/bin/bash
echo "🧹 Cleaning up OmniMind ghost processes..."

# Kill Daemon
pkill -f "omnimind_daemon.py"
echo "Killed omnimind_daemon.py"

# Kill Uvicorn
pkill -f "uvicorn"
echo "Killed uvicorn processes"

# Scan for lingering python processes related to src (aggressive but safe for this context)
# We avoid killing the IDE server or this agent's shell
ps aux | grep "python" | grep "projects/omnimind" | grep -v "vscode-server" | grep -v "grep" | grep -v "experiment_d" | awk '{print $2}' | xargs -r kill -9

echo "✨ Environment Cleaned."
ps aux | grep "python" | grep "omnimind"
