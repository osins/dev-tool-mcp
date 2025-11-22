#!/bin/bash

# Launch script for the MCP (Model Context Protocol) server
# This script provides a convenient way to start the dev-tool-mcp-server

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

echo "Checking virtual environment..."

# Check if virtual environment exists, create if it doesn't
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Ensure pip is available and upgrade it
python3 -m ensurepip --upgrade
pip install --upgrade pip

echo "Installing dependencies from pyproject.toml..."
# Install the package in editable mode from the current directory
cd "$SCRIPT_DIR"
pip install -e .

echo "Starting dev-tool-mcp-server..."
echo "This server provides web crawling, content extraction, and browser interaction features."
echo "Press Ctrl+C to stop the server."
echo

# Run the Python server
python "${SCRIPT_DIR}/mcp_server/server.py"

# Check the exit status
if [ $? -eq 0 ]; then
    echo "Server stopped."
else
    echo "Server stopped with error."
    exit 1
fi