from cd_history.args import *

MISSING_CD_HISTORY_ENV_VAR_MSG = f"{HISTORY_FILE_ENV} env var not set. Example fix: Add this to your bashrc and restart terminal. 'export {HISTORY_FILE_ENV}=/home/user/.cd_history'"
def CD_HISTORY_FILE_NOT_FOUND_MSG(location): return f"Cant find cd history file at: {location}. Generating new."
def CD_HISTORY_FILE_CANT_BE_CREATED_MSG(location): return f"Cant generate cd history file at: {location}"
def NON_EXISTENT_DIR_MSG(dir): return "Given dir '%s' does not exist" % dir
def NO_ABS_PATH_DIR_MSG(dir): return "dir path must be absolute path: %s" % dir
