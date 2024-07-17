import sys
import threading
from abc import ABC, abstractmethod

from cd_history.error_msgs import CD_HISTORY_FILE_NOT_FOUND_MSG
from cd_history.file_checker import FileChecker
from cd_history.logging_config import configure_logger


class App(ABC):

    def __init__(self, options, delay_start=False):
        self.logger = configure_logger(self.__class__.__name__)
        self.file_checker = FileChecker()
        self.options = options
        self.reader = None
        self.start_event = threading.Event()
        self.init_start_event(delay_start)
        self.search = None
        self.user_quit = False

    @abstractmethod
    def run(self):
        pass

    def init_start_event(self, delay_start):
        if not delay_start:
            self.start_event.set()

    def get_reader(self):
        return self.search.reader

    def signal_start(self):
        self.start_event.set()

    def close_program(self):
        if self.search:
            self.search.end()

    def generate_cd_history_if_missing(self):
        file = self.options.cd_history
        if not self.file_checker.isfile(file):
            print(CD_HISTORY_FILE_NOT_FOUND_MSG(file), file=sys.stderr)
            self.create_cd_history_file(file)

    def create_cd_history_file(self, path):
        try:
            with open(path, 'w'):
                pass
            self.logger.debug(f"cd_history file at: {path} has been created.")
        except Exception as e:
            self.logger.error("could not create cd_history file at %s" % path)
            raise e

    def wait_for_start_event(self):
        self.start_event.wait()

    def is_search_started(self):
        return self.search.is_started()

    def is_search_done(self):
        return self.search.is_done()

    def end_search(self):
        self.search.end()

    def stream_cd_history(self):
        self.reader.read()
