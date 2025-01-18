#!/bin/bash

# Create a virtual environment
python3 -m venv meshtastic_node_log_env

# Activate the virtual environment
source meshtastic_node_log_env/bin/activate

# Install dependencies
pip install -r requirements.txt
deactivate

echo "Setup complete. Run './run_my_script.sh' to start the tool."
