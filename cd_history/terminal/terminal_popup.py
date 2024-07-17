import sys

from cd_history.logging_config import configure_logger


class TerminalPopup:

    def __init__(self, ui, options):
        self.logger = configure_logger(self.__class__.__name__)
        self.ui = ui
        self.options = options

    def ask_for_filter(self):
        filter = self.ui.ask_user_for_string("Enter Filter:")
        if filter is None:
            self.logger.debug("no filter selected")
            print("no filter selected", file=sys.stderr)
        self.logger.debug(f"Popup is True, filter set to: {filter}")
        return filter

