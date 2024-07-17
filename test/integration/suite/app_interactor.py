import sys
import threading
import time
import tkinter as tk
import traceback
from pathlib import Path

from cd_history.app_launcher import DefaultAppLauncher
from test.integration.suite.cdhistoryreader_delay_mod import CdHistoryReaderDelayMod
from test.integration.suite.utils import *
from test.integration.suite.wait_util import WaitUtil


# facade for interacting with app under test (via stdin/out and via gui)
# encapsulates all internal state and setup logic needed for testing
class AppInteractor:

    def __init__(self):
        self.stdout_buf = io.StringIO()
        self.stderr_buf = io.StringIO()
        self.app_successful = False
        self.app = None
        self.root = None
        self.application_finished = threading.Event()
        self.reader_mod = None
        self.log_file = None
        self.start_delayed = False
        self.raise_exceptions = True
        self.gui = False

    def enable_file_logging(self):
        # for debugging purposes to get the output of the program under test in real time
        # useful when test is stuck to see what's up
        # tail -f test/files/output-log.txt
        output_log_file = open(resolve_test_file_path('output-log.txt'), 'w')
        self.log_file = str(Path(output_log_file.name).resolve())
        output_log_file.close()

    def teardown(self):
        if self.reader_mod:
            self.reader_mod.reset_mock()
        print("Teardown completed")

    # expected_result is either true (successful) or false
    def assert_app_finished_with_result(self, successful):
        assertEqual(successful, self.app_successful, "apps success status did not match")

    def assert_dirs_displayed(self, expected, strict=True):
        listbox_items = self.get_displayed_items()
        if strict:
            assertEqual(len(expected), len(listbox_items), "did not display expected amount of files")
        for expected_file in expected:
            assertIn(expected_file, listbox_items)
        return listbox_items

    def assert_dirs_not_displayed(self, unexpected):
        listbox_items = self.get_displayed_items()
        for expected_file in unexpected:
            assertNotIn(expected_file, listbox_items)
        return listbox_items

    # must be called on main thread
    def start(self):
        self.gui = self.is_gui_mode()
        self.start_app()

    def is_gui_mode(self):
        return "gui" in sys.argv

    def set_raise_exceptions(self, value):
        self.raise_exceptions = value

    # executed on main -> application under test will run on main thread
    def start_app(self):
        try:
            print("Starting application...")
            launcher = DefaultAppLauncher(raise_exceptions=self.raise_exceptions,
                                          log_file=self.log_file, delay_start=self.start_delayed)
            # make sure I can verify what was printed to stdout
            sys.stdout = self.stdout_buf
            sys.stderr = self.stderr_buf

            self.extract_internal_variables(launcher)
            launcher.start()
            # need to wait here so stdout of program makes it into the buffer
            # and stdout is not reset to old buf too fast
            time.sleep(0.3)
            self.app_successful = True
            # restore old stdout buf
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            print("app finished successfully")
        except Exception as exception:
            # need to restore here instead of finally so the print is executed after stdout is restored
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            traceback.print_exception(type(exception), exception, exception.__traceback__)
            print(f"Exception in app: {exception}")
            self.app_successful = False
        finally:
            self.application_finished.set()

    def delay_start(self):
        self.start_delayed = True

    # strict=False means the program may print more than the expected files to stdout
    def assert_printed_to_stdout(self, expected_outputs, strict=True):
        return assert_printed_to_stream(self.stdout_buf, expected_outputs, strict=strict)

    def assert_printed_to_stderr(self, expected_outputs, strict=True):
        return assert_printed_to_stream(self.stderr_buf, expected_outputs, strict=strict)

    def assert_not_printed_to_stderr(self, unexpected):
        stderr_lines = self.stderr_buf.getvalue().splitlines()
        for line in unexpected:
            assertNotIn(line, str(stderr_lines))

    def assert_nothing_printed_to_stdout(self):
        stdout = self.stdout_buf.getvalue()
        assertEqual(0, len(stdout), "stuff was written to stdout, but should not")

    # makes sure each reader.send_to_buf call is delayed by n seconds
    # this enables to create tests for long running searches that should be terminated while running
    # in a way that is deterministic across all pc speeds
    def slow_down_reader(self, delay):
        self.wait_until_app_set()
        self.wait_until_search_set()
        self.reader_mod = CdHistoryReaderDelayMod(self.app.get_reader())
        self.reader_mod.slow_down(delay)

    # can be used together with delay_start()
    def allow_start(self):
        self.wait_until_app_set()
        self.app.signal_start()

    # wait until app is closed
    def wait_until_app_finished(self):
        self.application_finished.wait()

    def wait_until_n_lines_printed(self, n):
        WaitUtil.wait_until(lambda: len(self.stdout_buf.getvalue().splitlines()) >= n, f"print {n} lines")

    def get_displayed_items(self):
        return self.root.children['!toplevel'].children['!listbox'].get(0, tk.END)

    def wait_until_window_open(self):
        self.wait_until_app_set()
        WaitUtil.wait_until(lambda: self.app.ui is not None)
        WaitUtil.wait_until(lambda: self.app.ui.is_open())

    def wait_until_search_started(self):
        self.wait_until_app_set()
        WaitUtil.wait_until(lambda: self.app.is_search_started(), "search start")

    def print_stdout(self):
        stdout = self.stdout_buf.getvalue()
        print("stdout:\n")
        print(stdout)
        print("\n")

    def print_stderr(self):
        stderr = self.stderr_buf.getvalue()
        print("stderr:\n")
        print(stderr)
        print("\n")

    # waits until launched app has its internal app variables set and sets it as member var of this class
    # if gui=True also capture app.root object
    def extract_internal_variables(self, launcher):
        def capture_refs():
            self.wait_until_app_initialized(launcher)
            # set app for operating on the app object graph
            self.app = launcher.app
            if self.gui:
                self.wait_until_root_initialized(launcher)
                if self.app:
                    self.root = self.app.root

        capture_thread = threading.Thread(target=capture_refs)
        capture_thread.start()

    # waits until app object is created in main of launched program
    def wait_until_app_initialized(self, launcher):
        WaitUtil.wait_until(lambda: launcher.app is not None or self.application_finished.is_set(), "set app instance")

    def wait_until_root_initialized(self, launcher):
        self.wait_until_app_initialized(launcher)
        WaitUtil.wait_until(lambda: self.app.root is not None or self.application_finished.is_set(), "set app instance")

    def wait_until_app_set(self):
        WaitUtil.wait_until(lambda: self.app is not None or self.application_finished.is_set(), "set app instance")

    def wait_until_root_set(self):
        WaitUtil.wait_until(lambda: self.root is not None or self.application_finished.is_set(), "set app instance")

    def wait_until_search_set(self):
        WaitUtil.wait_until(lambda: self.app.search is not None or self.application_finished.is_set(), "set search instance")

    def is_search_done(self):
        return self.app.is_search_done()
    def wait_until_search_done(self):
        self.wait_until_app_set()
        WaitUtil.wait_until(lambda: self.is_search_done() or self.application_finished.is_set(), "end search")

    def press_enter(self):
        self.root.event_generate("<Return>")

    def press_escape(self):
        self.root.event_generate("<Escape>")

    def press_down(self):
        self.root.event_generate("<Down>")
