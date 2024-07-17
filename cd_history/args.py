from cd_history.action import Action
from cd_history.interface_mode import InterfaceMode

SCRIPT_NAME = "cd-history.py"

# default values
DEFAULT_MODE = InterfaceMode.TERMINAL
DEFAULT_MAX_RESULT_DIRS = 25
DEFAULT_MAX_SCANNED_DIRS = -1
DEFAULT_ACTION = Action.SELECT

# args
MAX_SCANNED_DIRS_ARG = "--dirs"
MAX_RESULT_DIRS_ARG = "--results"
FILTER_ARG = "--filter"
MODE_ARG = "--mode"
ACTION_ARG = "--action"

# env vars
MAX_RESULTS_ENV = "CD_HIST_RESULTS"
MAX_SCANNED_ENV = "CD_HIST_MAX_SCANNED"
MODE_ENV = "CD_HIST_MODE"
HISTORY_FILE_ENV = "CD_HIST_FILE"
