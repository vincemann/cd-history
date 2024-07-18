#!/bin/bash
# usage: create-symlink.sh /path/to/binary local|system
# creates symlink pointing to given binary either in /usr/local/bin or $HOME/bin depending on scope arg
# makes sure dirs exist


print_usage() {
    echo "usage: $0 /path/to/binary local|system"
    exit 1
}

# Check if at least two arguments are provided
if [[ $# -lt 2 ]]; then
    print_usage
fi


# make sure binary exists and is executable
binary="$(readlink -f "$1")"
if [[ ! -f "$binary" ]]; then
	echo "binary does not exist: $binary"
	exit 1
fi
chmod a+x "$binary"


# parse scope
scope="$2"
local_installation=false
case $scope in
    local)
        local_installation=true
        ;;
    system)
        local_installation=false
        ;;
    *)
        print_usage
        ;;
esac



# prepare link location
if $local_installation; then
    link_location="$HOME/bin"
    if [[ ! -d "$link_location" ]]; then
    	echo "creating bin directory at $link_location"
    	mkdir -p "$link_location"
	fi
else
    link_location="/usr/local/bin"
fi
echo "link location: $link_location"



# create link
name="$(basename "$binary")"
link="${link_location}/${name}"


# create link
if [ ! -f "$link" ]; then
    echo "creating symlink: $link -> $binary"
    if $local_installation; then
    	ln -sf "$binary" "$link"
    else
    	sudo ln -sf "$binary" "$link"
    fi
else
    echo "symlink already exists at $link"
fi
