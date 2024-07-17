import os.path
import sys

from cd_history.append.history_appender import HistoryAppender
from cd_history.args import HISTORY_FILE_ENV
from cd_history.append.dir_validator import validate
from cd_history.dir_sanitizer import sanitize_dir
from cd_history.file_checker import FileChecker

USAGE_STRING = "usage: cd-history append /path/to/dir/to/append"


class AppendApp:

    def get_hist_file(self):
        file_checker = FileChecker()
        cd_history = os.getenv(HISTORY_FILE_ENV)
        if not cd_history:
            raise Exception("%s env var must be set. Example: 'export %s=~/.cd_history'" % HISTORY_FILE_ENV)
        if not file_checker.isfile(cd_history):
            raise Exception(f"cd_history file '{cd_history}' does not exist")
        return cd_history

    def exit(self, code):
        exit(code)

    def get_dir_arg(self):
        if len(sys.argv) != 3:
            raise Exception("Invalid amount of args, " + USAGE_STRING)
        dir = sys.argv[2]
        return dir

    def start(self):
        try:
            dir = self.get_dir_arg()
            cd_history = self.get_hist_file()
            validate(dir)
            sanitized = sanitize_dir(dir)
            appender = HistoryAppender(cd_history)
            appender.append_dir(sanitized)
        except Exception as e:
            print(e)
            self.exit(1)
