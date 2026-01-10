#!/bin/bash
set -e

# Directly call the pip inside your venv without "activating"
./.venv/bin/python -m pip install -e ".[dev]"
