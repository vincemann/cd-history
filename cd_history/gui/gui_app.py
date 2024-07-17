import tkinter as tk

from cd_history.app import App
from cd_history.gui.gui_popup import GuiPopup
from cd_history.gui.gui_userinput_handler import GuiUserInputHandler
from cd_history.logging_config import configure_logger
from cd_history.search import Search
from cd_history.gui.gui import Gui


class GuiApp(App):

    def __init__(self, options, delay_start=False):
        super().__init__(options, delay_start=delay_start)
        self.logger = configure_logger(self.__class__.__name__)
        self.root = self.create_parent_window()
        self.ui = Gui(self.root)
        self.popup = GuiPopup(self.ui, self.root, options)
        self.user_input_handler = GuiUserInputHandler(self, options)

    def create_parent_window(self):
        root = tk.Tk()
        root.withdraw()  # hide parent window, is just container
        return root

    def user_quits_program(self):
        self.user_quit = True
        self.close_program()

    def close_program(self):
        super().close_program()
        self.close_gui()

    def close_gui(self):
        if self.search and not self.search.is_done():
            self.root.after(30, self.close_gui)
        else:
            self.root.quit()
            try:
                self.root.destroy()
            except tk.TclError:
                # ignore, can happen if window is already closed on sigint
                pass
        # dont exit here bc of integration test issues otherwise

    def show_dir(self, dir):
        self.ui.show_dir(dir)

    def on_end_search(self):
        pass

    def setup_ui_callbacks(self):
        self.ui.setup_callbacks(dir_selected_callback=self.user_input_handler.on_dir_selected,
                                escape_callback=self.user_input_handler.on_escape)

    def run(self):
        self.generate_cd_history_if_missing()
        # needs to be done here
        self.search = Search(self.options,
                             dir_found_callback=self.show_dir,
                             end_search_callback=self.on_end_search)
        self.wait_for_start_event()

        if self.options.popup:
            self.options.filter = self.popup.ask_for_filter()

        self.ui.open_window()
        self.setup_ui_callbacks()

        self.search.start()
        self.root.mainloop()
        self.search.join()

