#!/bin/bash

# Set the path to your virtual environment and script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_PATH="$SCRIPT_DIR/meshtastic_node_log_env"
PYTHON_SCRIPT="$SCRIPT_DIR/meshtastic_node_log.py"

# Validate VENV
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH" >&2
    exit 1
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script with any arguments passed to this wrapper
python "$PYTHON_SCRIPT" "$@"

# Optional: Deactivate the virtual environment (not strictly necessary)
deactivate