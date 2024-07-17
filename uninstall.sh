#!/bin/bash

print_usage() {
    echo "Usage: $0 local|system"
    exit 1
}

scope=$1

local_installation=false
if [[ "$scope" == "local" ]]; then
    echo "uninstalling locally"
    local_installation=true
elif [[ "$scope" == "system" ]]; then
    echo "uninstalling system-wide"
else
    print_usage
fi


# which file to edit?
bashrc="/etc/bash.bashrc"
if $local_installation; then
    bashrc="$HOME/.bashrc"
fi
echo "editing file: $bashrc"


# backup
./scripts/install/backup.sh "$scope" "$bashrc"


# Remove cd history paragraph from bashrc
echo "modifying bashrc file..."
start="# CD HISTORY START"
end="# CD HISTORY END"
start_found=$(cat "$bashrc" | grep --count "$start")
end_found=$(cat "$bashrc" | grep --count "$end")

# preservers ownership and permissions, uses sudo if 'root' arg is present
# usage: move src target [root]
move()
{
    src="$1"
    target="$2"
    root="$3"
    if [[ "$root" == "root" ]];then
        sudo install -m "$(stat -c '%a' "$target")" -o "$(stat -c '%U' "$target")" -g "$(stat -c '%G' "$target")" "$src" "$target"
    else
        install -m "$(stat -c '%a' "$target")" -o "$(stat -c '%U' "$target")" -g "$(stat -c '%G' "$target")" "$src" "$target"
    fi
}

if [[ $start_found -gt 0 && $end_found -gt 0 ]]; then
    temp_file=$(mktemp)
    sed "/$start/,/$end/d" "$bashrc" > "$temp_file"

    if $local_installation; then
        move "$temp_file" "$bashrc"
    else
        move "$temp_file" "$bashrc" root
    fi

    ./scripts/install/remove-symlink.sh cd-history $scope
    ./scripts/install/remove-symlink.sh cd-hist-get $scope

    echo "successfully uninstalled"
else
    echo "start and end pattern not found"
    echo "already uninstalled, otherwise remove paragraph manually from $bashrc"
fi

