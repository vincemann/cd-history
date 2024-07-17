import sys

from cd_history.user_input_handler import UserInputHandler


class TerminalUserInputHandler(UserInputHandler):

    def __init__(self, app, options):
        super().__init__(app, options)
        self.cancel_count = 0

    def on_cancel_terminal_input(self):
        self.cancel_count += 1
        self.logger.debug(f"user canceled terminal input {self.cancel_count} times")
        if self.cancel_count > 1:
            print("nothing selected, exiting", file=sys.stderr)
            return
        if self.app.is_search_done():
            return
        if self.cancel_count == 1:
            self.logger.debug("going into terminal block for second time")
            self.app.end_search()
            self.app.let_user_select_dir()
