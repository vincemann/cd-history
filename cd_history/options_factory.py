import argparse
import os

from cd_history.args import *
from cd_history.options import Options


class OptionsFactory:

    def create(self):
        parser = argparse.ArgumentParser(description="Parse CLI arguments for cd-history", prog="cd-history")
        parser.add_argument(MODE_ARG, type=str, choices=[mode.value for mode in InterfaceMode],
                            help="Mode to display the last dirs")
        parser.add_argument(ACTION_ARG, type=str, choices=[action.value for action in Action],
                            help="Action to execute on the selected dir")
        parser.add_argument(MAX_RESULT_DIRS_ARG, type=int, help="Stop search after finding this amount of matching dirs")
        parser.add_argument(MAX_SCANNED_DIRS_ARG, type=int, help="Maximum number of directories to search through")
        parser.add_argument(FILTER_ARG, type=str, help="Filter regex or 'popup' for prompting user")
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")
        args = parser.parse_args()

        mode = args.mode or os.getenv(MODE_ENV, DEFAULT_MODE)
        mode = InterfaceMode(mode)

        popup = args.filter == "popup"

        options = Options(
            mode=mode,
            action=args.action or DEFAULT_ACTION,
            max_result_dirs=args.results or int(os.getenv(MAX_RESULTS_ENV, DEFAULT_MAX_RESULT_DIRS)),
            max_scanned_dirs=args.dirs or int(os.getenv(MAX_SCANNED_ENV, DEFAULT_MAX_SCANNED_DIRS)),
            filter=args.filter,
            cd_history=os.getenv(HISTORY_FILE_ENV),
            popup=popup,
            debug=args.debug,
        )
        return options

