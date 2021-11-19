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
        ezlib.eprint("gui was: %s" % gui)
        ezlib.eprint("usage: python3 show-last-dirs.py gui|terminal [matchword [last-dirs-amount=num default 10 [ clip=[0|1] default 0]]]")
        exit(1)
    ezlib.eprint("gui is: %s" % gui)



if len(sys.argv) > 2:
    matchword = sys.argv[2]
    ezlib.eprint("matchword is: %s" % matchword)

if len(sys.argv) > 3:
    last_dirs_amount = int(sys.argv[3])
    ezlib.eprint("last_dirs_amount is: %d" % last_dirs_amount)


if len(sys.argv) > 4:
    clip = int(sys.argv[4])
    if not (clip == 0 or clip == 1):
        ezlib.eprint("clip was %d" % clip)
        ezlib.eprint("usage: python3 show-last-dirs.py gui|terminal [matchword [last-dirs-amount=num default 10 [ clip=[0|1] default 0]]]")
        exit(1)
    ezlib.eprint("clip is %d" % clip)

dir_history_file = os.getenv("DIR_HISTORY")
if dir_history_file == None or dir_history_file == "":
	ezlib.eprint("cannot find dir dir history-file, set DIR_HISTORY env var")
	exit(1)

ezlib.eprint("dir hist file: %s" % dir_history_file)
last_dirs = ezlib.find_recent_dirs(dir_history_file,last_dirs_amount,matchword)
ezlib.eprint("last dirs: %s" % last_dirs)

if gui == "gui":
    selected_dir = ezlib.show_gui_selection(last_dirs)
else:
    selected_dir = ezlib.show_terminal_selection(last_dirs)

ezlib.eprint("selected_dir: %s" % selected_dir)

if selected_dir is None:
    ezlib.eprint("nothing selected - closing")
    exit(0)
if clip == 1:
    ezlib.eprint("putting to clipboard")
	ezlib.put_to_clipboard(selected_dir)
else:
    ezlib.eprint("returning dir")
	# put out as return value for calling bash scripts
	print(selected_dir)
	

