#!/bin/sh

echo "Running Ruff..."
uv run ruff check src/
uv run ruff format src/