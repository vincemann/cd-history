#!/bin/bash

interface=$1
scope=$2


print_usage() {
    echo "usage: $0 gui|terminal local|system"
    exit 1
}



# Parse arguments
case $interface in
    gui)
        echo "installing interface version"
        ;;
    terminal)
        echo "installing terminal version"
        ;;
    *)
        print_usage
        ;;
esac
local_installation=false
root=false
case $scope in
    local)
        echo "installing locally"
        local_installation=true
        ;;
    system)
        root=true
        echo "installing system wide"
        ;;
    *)
        print_usage
        ;;
esac



# edit files as root?
user="normal"
if $root; then
    user="root"
    echo "editing files as root"
else
    echo "editing files as $USER"
fi



# install deps
./scripts/install/install-python.sh
./scripts/install/setup-venv.sh



# which bashrc file to edit?
bashrc="/etc/bash.bashrc"
bashrc_template="./templates/system-bashrc-template"
if $local_installation; then
    bashrc="$HOME/.bashrc"
    bashrc_template="./templates/local-bashrc-template"
fi
echo "Editing file: $bashrc"
echo "Using bashrc template file: $bashrc_template"


# where to store cd_history file
hist_file="/opt/.cd_history"
if $local_installation; then
    hist_file="$HOME/.cd_history"
fi
echo "cd hist file location: $hist_file"


# create hist file if not there yet
if $local_installation; then
    [ ! -f "$hist_file" ] && touch "$hist_file"
else
    [ ! -f "$hist_file" ] && sudo touch "$hist_file"
    sudo chmod a+rw "$hist_file"
fi


# backup
./scripts/install/backup.sh "$scope" "$bashrc"



# add paragraph
start_pattern="# CD HISTORY START"
end_pattern="# CD HISTORY END"
start_found=$(cat "$bashrc" | grep --count "$start_pattern")
end_found=$(cat "$bashrc" | grep --count "$end_pattern")
template_file=$(mktemp)
cat "$bashrc_template" > "$template_file"
bash ./scripts/install/replace_or_add_line.sh "$template_file" "export CD_HIST_FILE=" "export CD_HIST_FILE=$hist_file" "$user"
bash ./scripts/install/replace_or_add_line.sh "$template_file" "export CD_HIST_MODE=" "export CD_HIST_MODE=$interface" "$user"
echo "paragraph to add:"
cat "$template_file"
echo "adding bashrc paragraph"
bash ./scripts/install/replace_or_add_paragraph.sh "$bashrc" "$start_pattern" "$end_pattern" "$template_file" "$user"
echo "done updating bashrc"



# create symlinks if needed
./scripts/install/create-symlink.sh "./cd-history" $scope
./scripts/install/create-symlink.sh "./bin/cd-hist-get" $scope


# done
echo "installed"
echo "current installations: $installations"
echo "restart terminal for changes to take effect"
