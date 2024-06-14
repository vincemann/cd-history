#!/bin/bash


file="$1"
start_pattern="$2"
end_pattern="$3"
data_file="$4"
root_arg=$5


root=false
if [[ "$root_arg" == "root" ]]; then
	root=true
fi


start_found=$(cat "$file" | grep --count "$start_pattern")
end_found=$(cat "$file" | grep --count "$end_pattern")

if [[ "$start_found" -eq 1 && "$end_found" -eq 1 ]];then
	echo "found prev installation, updating paragraph"
	# remove old version

	if $root; then
		sudo sed -i "/$start_pattern/,/$end_pattern/d" "$file"
	else
		sed -i "/$start_pattern/,/$end_pattern/d" "$file"
	fi

	# install new
	if $root; then
		cat "$data_file" | sudo tee -a "$file" 1>/dev/null
	else
		cat "$data_file" | tee -a "$file" 1>/dev/null
	fi
	
elif [[ "$start_found" -eq 0 && "$end_found" -eq 0 ]];then
	echo "inserting paragraph"
	if $root; then
		cat "$data_file" | sudo tee -a "$file" 1>/dev/null
	else
		cat "$data_file" | tee -a "$file" 1>/dev/null
	fi
	
else
	echo "invalid amount of installations found: start: $start_found, end: $end_found"
	exit 1
fi


