import os

from cd_history.args import HISTORY_FILE_ENV
from cd_history.clean.cd_history_cleaner import CdHistoryCleaner
from cd_history.file_checker import FileChecker


class CleanApp:

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

    def start(self):
        try:
            file = self.get_hist_file()
            cleaner = CdHistoryCleaner(file)
            cleaner.clean()
        except Exception as e:
            print(e)
            self.exit(1)




