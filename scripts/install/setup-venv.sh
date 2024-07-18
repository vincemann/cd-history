#!/bin/bash

# make sure venv is setup and all deps are installed into it

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment
source ./.venv/bin/activate

# Upgrade pip within the virtual environment
python -m pip install --upgrade pip

# Install requirements from requirements.txt
python -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

# Deactivate the virtual environment
deactivate