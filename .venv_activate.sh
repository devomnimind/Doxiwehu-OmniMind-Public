#!/bin/bash
# Auto-activate venv when entering project directory
# Add this to your ~/.zshrc or ~/.bashrc:
# source ~/projects/omnimind/.venv_activate.sh

OMNIMIND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$OMNIMIND_DIR/.venv/bin/activate" ]; then
    source "$OMNIMIND_DIR/.venv/bin/activate"
    echo "✅ OmniMind venv ativado (Python 3.12.8)"
else
    echo "⚠️  Venv não encontrado em $OMNIMIND_DIR/.venv"
fi
