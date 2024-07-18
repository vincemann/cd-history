#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages using the appropriate package manager
install_packages() {
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-tk
    elif command_exists yum; then
        sudo yum install -y python3 python3-tkinter
    elif command_exists dnf; then
        sudo dnf install -y python3 python3-tkinter
    elif command_exists zypper; then
        sudo zypper install -y python3 python3-tk
    else
        echo "Unsupported package manager. Please install python3 and python3-tk manually."
        exit 1
    fi
}

# Check if python3 is installed
if ! command_exists python3; then
    echo "python3 is not installed. Installing..."
    install_packages
else
    echo "python3 is already installed."
fi

# Check if python3-tk is installed
if python3 -c "import tkinter" &>/dev/null; then
    echo "python3-tk is already installed."
else
    echo "python3-tk is not installed. Installing..."
    install_packages
fi

# Continue with your script that requires python3 and python3-tk
echo "python is availible:"
python3 --version
