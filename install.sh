#!/bin/bash


GUI=$1
SCOPE=$2

print_usage()
{
	echo "usage: ./install gui|terminal local|system"
	exit 1
}

if [[ $GUI = "gui" ]]; then
	echo "installing gui version"
elif [[ $GUI = "terminal" ]]; then
	echo "installing terminal version"
else
	print_usage
fi


local_installation=false
root=false
if [[ $SCOPE = "local" ]];then
	echo "installing locally"
	local_installation=true
elif [[ $SCOPE = "system" ]];then
	root=true
	echo "installing system wide"
else
	print_usage
fi

# install python if needed
./install-python.sh


# which file to edit?
bashrc="/etc/bash.bashrc"
if $local_installation; then
    bashrc="$HOME/.bashrc"
fi
echo "Editing file: $bashrc"


# backup
./backup.sh "$SCOPE" "$bashrc"



# add paragraph
start_pattern="# CD HISTORY START"
end_pattern="# CD HISTORY END"
start_found=$(cat "$bashrc" | grep --count "$start_pattern")
end_found=$(cat "$bashrc" | grep --count "$end_pattern")
template_file=$(mktemp)
cat bashrc-template > "$template_file"
sed -i -e "s@§HOME@$HOME@g" "$template_file"


user="normal"
if $root; then
	user="root"
fi
echo "replacing/adding paragraph"
bash ./lib/replace_or_add_paragraph.sh "$bashrc" "$start_pattern" "$end_pattern" "$template_file" "$user"
echo "updating/adding gui/terminal line to: $GUI"
bash ./lib/replace_or_add_line.sh "$bashrc" "export CD_HIST_GUI=" "export CD_HIST_GUI=$GUI" "$user"
echo "done updating file"

echo "creating symlink in path: /usr/local/bin/show-last-dirs.py -> $(pwd)/show-last-dirs.py"
chmod a+x "./show-last-dirs.py"
ln -sf "$(pwd)/show-last-dirs.py" "/usr/local/bin/show-last-dirs"

echo "installed"
echo "restart terminal for changes to take effect"
