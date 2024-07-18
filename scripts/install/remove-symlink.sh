#!/bin/bash
# usage: remove-symlink.sh /path/to/binary local|system
# removes symlink pointing to given binary either in /usr/local/bin or $HOME/bin depending on scope arg


print_usage() {
    echo "usage: $0 binary-name local|system"
    exit 1
}

# Check if at least two arguments are provided
if [[ $# -lt 2 ]]; then
    print_usage
fi


# make sure binary exists and is executable
binary_name="$1"


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



# eval link location
if $local_installation; then
    link_location="$HOME/bin"
else
    link_location="/usr/local/bin"
fi
echo "link location: $link_location"



# get full link path
link="${link_location}/${binary_name}"


# remove link if exists
if [ -f "$link" ]; then
    echo "removing symlink: $link"
    if $local_installation; then
    	rm -f "$link"
    else
    	sudo rm -f "$link"
    fi
else
    echo "symlink already removed: $link"
fi
