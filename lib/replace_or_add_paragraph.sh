#!/bin/bash


file="$1"
start_pattern="$2"
end_pattern="$3"
data_file="$4"

start_found=$(sudo cat "$file" | grep --count "$start_pattern")
end_found=$(sudo cat "$file" | grep --count "$end_pattern")

if [[ "$start_found" -eq 1 && "$end_found" -eq 1 ]];then
	echo "found prev installation, updating..."
	# remove old version
	sudo sed -i "/$start_pattern/,/$end_pattern/d" "$file"
	# install new
	cat "$data_file" | sudo tee -a "$file" 1>/dev/null
elif [[ "$start_found" -eq 0 && "$end_found" -eq 0 ]];then
	cat "$data_file" | sudo tee -a "$file" 1>/dev/null
else
	echo "invalid amount of installations found: start: $start_found, end: $end_found"
	exit 1
fi

