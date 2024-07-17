import sys
import threading

from cd_history.logging_config import configure_logger
from cd_history.action import Action


class UserInputHandler:

    def __init__(self, app, options):
        self.logger = configure_logger(self.__class__.__name__)
        self.options = options
        self.app = app
        # this stuff is related to on_dir_selected being called multiple times, see below
        self.dir_selected = False
        self.lock = threading.Lock()

    # this method may be called twice on selection in specific cases
    # make sure this does not affect the program
    # todo fix this in the future
    def on_dir_selected(self, selected):
        with self.lock:
            if self.dir_selected:
                return
            self.dir_selected = True
            if self.options.action == Action.SELECT:
                print(selected, file=sys.stdout)
            self.app.close_program()
