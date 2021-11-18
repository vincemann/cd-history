#!/bin/bash

GUI=$1
LOCAL=$2

print_usage()
{
	echo "(cd-history)usage ./install gui|terminal local|system"
	exit 1
}

if [[ $GUI = "gui" ]]; then
	echo "installing gui version"
elif [[ $GUI = "terminal" ]]; then
	echo "installing terminal version"
else
	print_usage
fi


if [[ $LOCAL = "local" ]];then
	echo "installing locally"
elif [[ $LOCAL = "system" ]];then
	echo "installing system wide"
else
	print_usage
fi

load_libs()
{
	echo "loading dependencies"
	git clone https://github.com/vincemann/ez-bash.git
	mv ./ez-bash/lib .
	rm -rf ./ez-bash
}

load_libs

bashrc="/etc/bash.bashrc"
if [[ "$LOCAL" = "local" ]]; then
	bashrc="$HOME/.bashrc"
fi

start_pattern="# CD HISTORY START"
end_pattern="# CD HISTORY END"
start_found=$(sudo cat "$bashrc" | grep --count "$start_pattern")
end_found=$(sudo cat "$bashrc" | grep --count "$end_pattern")

# backup
mkdir -p "$HOME/.ezbash-suite-backups"
sudo cp "$bashrc" "$HOME/.ezbash-suite-backups/.cd-history-bashrc.bak"

# replace vars
template_file=$(mktemp)
cat bashrc-template > "$template_file"
sed -i -e "s@§HOME@$HOME@g" "$template_file"


sudo bash ./lib/replace_or_add_paragraph.sh "$bashrc" "$start_pattern" "$end_pattern" "$template_file"
sudo bash ./lib/replace_or_add_line.sh "$bashrc" "export CD_HIST_GUI=" "export CD_HIST_GUI=$GUI"


echo "creating symlink in path (/usr/local/bin)"
chmod a+x "./show-last-dirs.py"
sudo ln -sf "$(pwd)/show-last-dirs.py" "/usr/local/bin/show-last-dirs"

echo "installed"
echo "restart terminal for changes to take effect"
