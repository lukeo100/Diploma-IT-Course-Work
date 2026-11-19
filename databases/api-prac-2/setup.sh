#!/usr/bin/env bash
# Creates the virtual environment and installs dependencies.
# Usage:  ./setup.sh   then   source .venv/bin/activate
set -e
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
echo "Done. Activate with: source .venv/bin/activate"
