#!/bin/bash

LOCAL=$1
FILE="$2"

print_usage() {
    echo "Usage: $0 local|system file"
    exit 1
}

local_installation=false
if [[ "$LOCAL" == "local" ]]; then
    local_installation=true
elif [[ "$LOCAL" == "system" ]]; then
    local_installation=false
else
    print_usage
fi

if [[ -z "$FILE" ]]; then
    print_usage
fi


backup_dir="$HOME/.cd-history-backup"
timestamp=$(date +"%Y%m%d-%H%M%S")
if $local_installation; then
    backup_file="$backup_dir/bashrc-local-$timestamp.bak"
else
    backup_file="$backup_dir/bashrc-system-$timestamp.bak"
fi
echo "Storing backup of bashrc in $backup_file"
mkdir -p "$backup_dir"
cp "$FILE" "$backup_file"
echo "backup done"
