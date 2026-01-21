#!/bin/bash
set -e

# check to see if .venv is initialized first
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# Upgrade pip inside the venv
./.venv/bin/python -m pip install --upgrade pip

# Directly call the pip inside your venv without "activating"
./.venv/bin/python -m pip install -e ".[dev]"
