#!/bin/bash
# Clip Operations Center - Start Dashboard Script
# Usage: ./run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV" ]; then
    echo ".venv not found. Please run setup first:"
    echo "  python -m venv .venv"
    echo "  .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
fi

echo "Starting Clip Operations Center Dashboard..."
echo "Dashboard: http://127.0.0.1:8765"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    "$VENV/Scripts/python.exe" -m clipops serve
else
    "$VENV/bin/python" -m clipops serve
fi