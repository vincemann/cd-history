import signal
import sys

from cd_history import config
from cd_history.gui.gui_app import GuiApp
from cd_history.interface_mode import InterfaceMode
from cd_history.logging_config import configure_logger
from cd_history.options_factory import OptionsFactory
from cd_history.terminal.terminal_app import TerminalApp


# launches app in default mode
class DefaultAppLauncher:
    """
    :parameter raise_exceptions: raise exceptions or exit?
    :parameter log_file: if set, log to this file instead of stderr. stdout is unscathed
    :parameter delay_start: if set, need to call app#signal_start() to allow the app to start (for testing)
    """
    def __init__(self, raise_exceptions=False, log_file=None, delay_start=False):
        self.app = None
        self.logger = None
        self.delay_start = delay_start
        self.raise_exceptions = raise_exceptions
        if log_file:
            config.log_file = log_file

    def configure_logger(self, options):
        config.debug = options.debug
        self.logger = configure_logger("main")

    def exit(self, code):
        sys.exit(code)

    def handle_exception(self, e):
        print(e, file=sys.stderr)
        if self.raise_exceptions:
            raise e
        else:
            self.exit(1)

    def sigint_handler(self, signum, frame):
        self.close()

    def close(self):
        if self.app:
            self.app.close_program()

    def create_app(self, options):
        if options.mode == InterfaceMode.GUI:
            return GuiApp(options, delay_start=self.delay_start)
        else:
            return TerminalApp(options, delay_start=self.delay_start)

    def start(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        try:
            optionsfactory = OptionsFactory()
            options = optionsfactory.create()
            self.configure_logger(options)
            self.logger.debug(f"Options created: {options}")
            options.validate()
            self.app = self.create_app(options)
            self.app.run()
        except Exception as e:
            self.handle_exception(e)
        finally:
            self.close()
