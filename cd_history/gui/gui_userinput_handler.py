from cd_history.logging_config import configure_logger
from cd_history.user_input_handler import UserInputHandler


class GuiUserInputHandler(UserInputHandler):

    def __init__(self, app, options):
        super().__init__(app, options)
        self.logger = configure_logger(self.__class__.__name__)
        self.escape_count = 0

    def on_escape(self):
        if self.app.is_search_done():
            self.app.close_program()
        else:
            if self.escape_count == 0:
                self.app.end_search()
            else:
                self.app.close_program()
        self.escape_count += 1
