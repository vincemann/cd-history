import select
import sys
import threading

from cd_history.exception_thread import ExceptionThread
from cd_history.logging_config import configure_logger


# non blocking
class TerminalIndexSelector:
    def __init__(self):
        self.logger = configure_logger(self.__class__.__name__)
        self.select_index_callback = None
        self.cancel_callback = None
        self.stop_event = threading.Event()
        self.selection_thread = ExceptionThread(target=self.run)

    def run(self):
        user_input = None
        try:
            while not self.stop_event.is_set():

                if self.stop_event.wait(timeout=0.1):
                    return

                # using select here so I can still terminate the thread via stop event, otherwise its blocking call
                # and setting the stop event wont shut it down
                if sys.stdin.readable() and select.select([sys.stdin], [], [], 0.1)[0]:
                    user_input = input()
                    break

            if self.stop_event.is_set():
                self.logger.debug("stop event set")
                return

            # Give user option to stop search by pressing enter
            if user_input == "":
                self.cancel_callback()
                return

            selection = int(user_input)
        except ValueError as e:
            self.logger.debug("invalid input: %s" % user_input, e)
            print("invalid input", file=sys.stderr)
            raise e

        if selection is None:
            self.logger.debug("nothing selected")
            print("nothing selected", file=sys.stderr)
            return

        if self.stop_event.is_set():
            return
        index = selection
        self.logger.debug("selected index: %d" % index)
        self.select_index_callback(index)

    def join(self):
        self.selection_thread.join()

    def start_selection(self, cancel_callback, select_index_callback):
        self.cancel_callback = cancel_callback
        self.select_index_callback = select_index_callback
        self.selection_thread.start()

    def stop_selection(self):
        self.stop_event.set()
