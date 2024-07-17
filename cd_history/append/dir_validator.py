from cd_history.error_msgs import *
from cd_history.file_checker import FileChecker


def validate(dir):
    # is empty?
    if not dir.strip():
        raise Exception("given dir must not be whitespace only")
    # make sure is not multiline
    if '\n' in dir[:-1]:
        raise Exception("dir must not be multi line")
    file_checker = FileChecker()
    if not dir.startswith("/"):
        raise Exception(NO_ABS_PATH_DIR_MSG(dir))
    if not file_checker.isdir(dir):
        raise Exception(NON_EXISTENT_DIR_MSG(dir))
