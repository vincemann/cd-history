#!/bin/bash

file="$1"
pattern="$2"
line="$3"

found=$(sudo cat "$file" | grep --count "$pattern")

if [[ "$found" -eq 1 ]];then
	echo "replacing line containing: $pattern with: $line"
	sed -i "s/.*$pattern.*/$line/g" "$file"
elif [[ "$found" -eq 0 ]];then
	echo "adding line: $line"
	echo "$pattern" | sudo tee -a "$file"
else
	echo "pattern found multiple times, skip replacement"
fi
