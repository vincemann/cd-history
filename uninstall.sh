#!/bin/bash

print_usage() {
    echo "Usage: $0 local|system"
    exit 1
}

SCOPE=$1

local_installation=false
if [[ "$SCOPE" == "local" ]]; then
    echo "Uninstalling locally"
    local_installation=true
elif [[ "$SCOPE" == "system" ]]; then
    echo "Uninstalling system-wide"
else
    print_usage
fi


# which file to edit?
bashrc="/etc/bash.bashrc"
if $local_installation; then
    bashrc="$HOME/.bashrc"
fi
echo "Editing file: $bashrc"


# Backup
./backup.sh "$SCOPE" "$bashrc"


echo "modifying bashrc file..."
# Remove cd history paragraph from bashrc
start="# CD HISTORY START"
end="# CD HISTORY END"
start_found=$(cat "$bashrc" | grep --count "$start")
end_found=$(cat "$bashrc" | grep --count "$end")

if [[ $start_found -gt 0 && $end_found -gt 0 ]]; then
    temp_file=$(mktemp)
    sed "/$start/,/$end/d" "$bashrc" > "$temp_file"

    if $local_installation; then
        mv "$temp_file" "$bashrc"
    else
        sudo mv "$temp_file" "$bashrc"
    fi

    echo "removing symlink"
    rm -f /usr/local/bin/show-last-dirs

    echo "Successfully uninstalled"
else
    echo "Start and end pattern not found"
    echo "Already uninstalled, otherwise remove paragraph manually from $bashrc"
fi

