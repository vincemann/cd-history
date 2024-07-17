import threading

from cd_history.dir_filter import DirFilter
from cd_history.logging_config import configure_logger
from cd_history.cd_history_reader import CdHistoryReader
from cd_history.dir_sanitizer import sanitize_dir
from cd_history.file_checker import FileChecker
from cd_history.exception_thread import ExceptionThread


class Search:

    def __init__(self, options, dir_found_callback, end_search_callback):
        self.logger = configure_logger(self.__class__.__name__)
        self.options = options
        self.search_thread = ExceptionThread(target=self.run)
        self.dir_found_callback = dir_found_callback
        self.end_search_callback = end_search_callback
        self.dirs_read = []
        self.reader = self.create_reader()
        self.file_checker = FileChecker()
        self.started = False
        self.filter = None

    def create_reader(self):
        return CdHistoryReader(self.options.cd_history,
                               self.options.max_scanned_dirs,
                               callback=self.on_dir_found)

    def is_started(self):
        return self.started

    def is_done(self):
        if not self.is_started():
            return False
        else:
            return not self.search_thread.is_alive()

    def join(self):
        self.search_thread.join()

    def start(self):
        # needs to be done here bc of some timing issues
        # -> options.filter can change but this constructor needs to be called early
        self.filter = DirFilter(self.options.filter)
        self.logger.debug("starting search thread")
        self.search_thread.start()
        self.started = True

    # this code is executed on thread starting
    def run(self):
        self.reader.read()
        self.end_search_callback()

    def end(self):
        if self.is_done():
            # already ended
            return
        self.logger.debug("ending search")
        self.reader.stop()

    def on_dir_found(self, dir):
        dir = sanitize_dir(dir)
        if not self.filter.accept(dir):
            return
        if self.read_enough_dirs():
            self.end()
        else:
            self.dir_found_callback(dir)
        self.dirs_read.append(dir)

    def read_enough_dirs(self):
        dirs_left_to_find = self.options.max_result_dirs - len(self.dirs_read)
        return dirs_left_to_find <= 0

