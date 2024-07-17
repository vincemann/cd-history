import re
import threading
from file_read_backwards import FileReadBackwards

from cd_history.logging_config import configure_logger


class CdHistoryReader:

    def __init__(self, file, max_lines_to_read, callback):
        self.file = file
        self.max_lines_to_read = max_lines_to_read
        self.callback = callback
        self.exit_event = threading.Event()
        self.logger = configure_logger(self.__class__.__name__)

    def stop(self):
        self.logger.debug("stopping reader")
        self.exit_event.set()

    # finds n most recent dirs from cd_history file (end to start)
    # may return less than n dirs, if eof is reached before
    # output can be filtered
    def read(self):
        read_lines = 0
        with FileReadBackwards(self.file) as file:
            while read_lines < self.max_lines_to_read or self.max_lines_to_read == -1:
                read_lines += 1
                if self.exit_event.is_set():
                    self.logger.debug("exit event set")
                    break
                dir = file.readline()
                if dir == "":
                    self.logger.debug("eof")
                    break
                dir = dir.strip()
                if not dir:
                    continue
                self.send_dir_to_callback(dir)
            file.close()
        self.logger.debug("done reading cd history")

    def send_dir_to_callback(self, dir):
        self.logger.debug(f"callback dir: {dir}")
        self.callback(dir)

