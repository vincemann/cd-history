import sys
import time

from cd_history.logging_config import configure_logger
from cd_history.terminal.index_selector import TerminalIndexSelector


class TerminalUi:

    """
    :parameter print_file_stream stream to print file output to (example: 1: /my/file)
               can either be sys.stderr or sys.stdout
    """
    def __init__(self, print_file_stream, print_numbers):
        self.logger = configure_logger(self.__class__.__name__)
        self.dirs = []
        self.current_index = 1
        self.print_files_stream = print_file_stream
        self.print_numbers = print_numbers
        self.terminal_content_reset = False
        self.index_selector = None

    def ask_user_for_string(self, msg):
        self.logger.debug(msg)
        print(msg, file=sys.stderr)
        try:
            filter = input()
            return filter
        except KeyboardInterrupt:
            # give user enough time to see no filter was used
            # otherwise the print \033c will hide this msg
            time.sleep(1)
            return None

    def print_dir(self, dir):
        to_print = self.get_print_string(dir)
        self.logger.debug(to_print)
        print(to_print, file=self.print_files_stream)
        self.current_index += 1

    def get_print_string(self, dir):
        if self.print_numbers:
            return "%d: %s" % (self.current_index, dir)
        else:
            return "%s" % dir

    def reset_terminal_content(self):
        if self.terminal_content_reset:
            print("\033c", end="", file=self.print_files_stream)
            self.terminal_content_reset = True

    def show_dir(self, dir):
        self.logger.debug("showing dir in terminal: " + dir)
        self.dirs.append(dir)
        self.print_dir(dir)

    def wait_until_selection_started(self):
        while self.index_selector is None:
            time.sleep(0.05)

    # blocking call that can be interrupted via stop_selection from diff thread
    def select_dir(self, cancel_callback, select_dir_callback):
        # if old selector is running, stop
        if self.index_selector:
            self.index_selector.stop_selection()

        def on_select_index(index):
            try:
                dir = self.dirs[index-1]
                select_dir_callback(dir)
            except IndexError as e:
                print("wrong input", file=sys.stderr)
                self.logger.debug("wrong input", e)

        self.reset_terminal_content()
        # need to instantiate here to allow for second call of this method
        self.index_selector = TerminalIndexSelector()
        self.index_selector.start_selection(cancel_callback, on_select_index)
        self.index_selector.join()

    def stop_selection(self):
        self.index_selector.stop_selection()
