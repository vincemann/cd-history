import sys

from cd_history.logging_config import configure_logger
from cd_history.interface_mode import InterfaceMode
import tkinter as tk


class GuiPopup:

    def __init__(self, ui, root, options):
        self.logger = configure_logger(self.__class__.__name__)
        self.root = root
        self.ui = ui
        self.options = options

    def ask_for_filter(self):
        popup_filter_var = tk.StringVar()

        def popup():
            filter = self._ask_for_filter()
            popup_filter_var.set(filter)

        self.root.after(0, popup)
        # wait for popup input before continuing, so the filter is actually set before starting
        # the background search thread
        self.root.wait_variable(popup_filter_var)
        return popup_filter_var.get()

    def _ask_for_filter(self):
        filter = self.ui.ask_user_for_string("Enter Filter:")
        if filter is None:
            self.logger.debug("no filter selected")
            print("no filter selected", file=sys.stderr)
        self.logger.debug(f"Popup is True, filter set to: {filter}")
        return filter

