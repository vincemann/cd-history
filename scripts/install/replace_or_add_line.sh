#!/bin/bash

file="$1"
pattern="$2"
line="$3"
root_arg=$4


root=false
if [[ "$root_arg" == "root" ]]; then
	root=true
fi


found=$(cat "$file" | grep --count "$pattern")

if [[ "$found" -eq 1 ]];then
	echo "replacing line containing: $pattern with: $line"
	if $root; then
		sudo sed -i "s|.*$pattern.*|$line|g" "$file"
	else
		sed -i "s|.*$pattern.*|$line|g" "$file"
	fi
elif [[ "$found" -eq 0 ]];then
	echo "adding line: $line"
	if $root; then
		echo "$pattern" | sudo tee -a "$file"
	else
		echo "$pattern" | tee -a "$file"
	fi
	
else
	echo "pattern found multiple times, skip replacement"
fi