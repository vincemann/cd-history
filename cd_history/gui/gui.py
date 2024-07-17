import sys
import tkinter as tk
from tkinter import Toplevel, simpledialog

from cd_history.logging_config import configure_logger


class Gui:
    def __init__(self, parent):
        self.logger = configure_logger(self.__class__.__name__)
        self.parent = parent
        self.child = None
        self.listbox = None
        self.size = 20
        self.dirs = []
        self.selected_index = 0
        self.dir_selected_callback = None
        self.escape_callback = None

    def is_open(self):
        return self.child and self.child.winfo_exists()

    def close_window(self):
        self.logger.debug("closing child window")
        self.child.quit()
        self.child.destroy()

    def ask_user_for_string(self, msg):
        return simpledialog.askstring("Input", msg, parent=self.parent)

    # user pressed enter to select the currently focuses dir
    def on_dir_selected(self, event):
        if self.selected_index is None:
            self.logger.debug("No dir selected")
            print("no dir selected", file=sys.stderr)
            return
        try:
            selected_dir = self.dirs[self.selected_index]
            self.logger.debug(f"Selected dir: {selected_dir}")
            self.dir_selected_callback(selected_dir)
        except IndexError as e:
            if len(self.dirs) == 0:
                self.escape_callback()
                return
            self.logger.error("Selected index is out of range", e)
            print("Selected index is out of range", file=sys.stderr)

    def on_escape(self, event):
        if self.escape_callback:
            self.escape_callback()

    # must be called after open window
    def setup_callbacks(self, dir_selected_callback=None, escape_callback=None):
        self.escape_callback = escape_callback
        self.dir_selected_callback = dir_selected_callback
        self.listbox.bind("<<ListboxSelect>>", self.on_focus_dir)
        self.child.bind("<Return>", self.on_dir_selected)
        self.child.bind("<Escape>", self.on_escape)

    def open_window(self):
        self.logger.debug("opening window")
        self.child = Toplevel(self.parent)
        # make sure child loop ends on exit window
        self.child.protocol("WM_DELETE_WINDOW", self.close_window)
        self.listbox = tk.Listbox(self.child, font=('Times', self.size))
        self.listbox.config(width=0)

        # Calculate the number of items that can be displayed on the screen without scrolling
        max_items = self.child.winfo_screenheight() // self.size
        self.listbox.config(height=max_items)
        self.listbox.pack()

    # adds dirs to gui
    def show_dir(self, dir):
        self.logger.debug("showing dir in gui: %s" % dir)

        def add_dir_to_gui(dir):
            self.listbox.insert("end", dir)
            self.listbox.select_set(0)
            self.listbox.focus_set()
            self.dirs.append(dir)
        # run on main gui thread
        self.child.after(0, add_dir_to_gui(dir))

    # on user focuses dir -> update current selection index
    def on_focus_dir(self, event):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            self.selected_index = selected_index

