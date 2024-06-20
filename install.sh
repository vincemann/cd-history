#!/bin/bash


# Initialize variables
GUI=$1
SCOPE=$2

# Function to print usage
print_usage() {
    echo "usage: $0 gui|terminal local|system"
    exit 1
}

# Parse arguments
case $GUI in
    gui)
        echo "installing GUI version"
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

case $SCOPE in
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

# Determine user context
user="normal"
if $root; then
    user="root"
fi

# install python if needed
./libs/install-python.sh


# which bashrc file to edit?
bashrc="/etc/bash.bashrc"
if $local_installation; then
    bashrc="$HOME/.bashrc"
fi
echo "Editing file: $bashrc"

# edit files as root?
user="normal"
if $root; then
	user="root"
fi

# backup
./libs/backup.sh "$SCOPE" "$bashrc"


# add paragraph
start_pattern="# CD HISTORY START"
end_pattern="# CD HISTORY END"
start_found=$(cat "$bashrc" | grep --count "$start_pattern")
end_found=$(cat "$bashrc" | grep --count "$end_pattern")
template_file=$(mktemp)
cat bashrc-template > "$template_file"
sed -i -e "s@§HOME@$HOME@g" "$template_file"
echo "adding bashrc paragraph"
bash ./libs/replace_or_add_paragraph.sh "$bashrc" "$start_pattern" "$end_pattern" "$template_file" "$user"


# setting env vars in bashrc
echo "setting FH_MODE to: $GUI"
bash ./libs/replace_or_add_line.sh "$bashrc" "export CD_HIST_GUI=" "export CD_HIST_GUI=$GUI" "$user"
echo "done updating bashrc"

# create symlink
name="cd-history"
echo "creating symlink in path: /usr/local/bin/$name -> $(pwd)/$name.py"
chmod a+x "./cd-history.py"
ln -sf "$(pwd)/$name.py" "/usr/local/bin/$name"

echo "installed"
echo "restart terminal for changes to take effect"
