#!/usr/bin/env python3
from lib import ezlib as ezlib
import sys
import os


gui = None
clip = 0
last_dirs_amount=10
matchword=""

if len(sys.argv) > 1:
    gui = sys.argv[1]
    if not (gui == "gui" or gui == "terminal"):
        ezlib.eprint("usage: python3 show-last-dirs.py gui|terminal [matchword [last-dirs-amount=num default 10 [ clip=[0|1] default 0]]]")
        exit(1)



if len(sys.argv) > 2:
    matchword = sys.argv[2]

if len(sys.argv) > 3:
    last_dirs_amount = int(sys.argv[3])

if len(sys.argv) > 4:
    clip = int(sys.argv[4])
    if not (clip == "0" or clip == "1"):
        ezlib.eprint("usage: python3 show-last-dirs.py gui|terminal [matchword [last-dirs-amount=num default 10 [ clip=[0|1] default 0]]]")
        exit(1)

dir_history_file = os.getenv("DIR_HISTORY")
if dir_history_file == None or dir_history_file == "":
	ezlib.eprint("cannot find dir dir history-file, set DIR_HISTORY env var")
	exit(1)

last_dirs = ezlib.find_recent_dirs(last_dirs_amount,matchword)


if gui == "gui":
    selected_dir = selection.show_gui_selection(last_dirs)
else:
    selected_dir = selection.show_terminal_selection(last_dirs)

if clip == 1:
	ezlib.put_to_clipboard(selected_dir)
else:
	# put out as return value for calling bash scripts
	print(selected_dir)
	

