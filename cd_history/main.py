import sys

from cd_history.app_launcher import DefaultAppLauncher
from cd_history.append.append_app import AppendApp
from cd_history.clean.clean_app import CleanApp
from cd_history.mode import Mode
from cd_history.mode_parser import eval_mode


def start_default_app():
    app = DefaultAppLauncher()
    app.start()


def start_clean_app():
    app = CleanApp()
    app.start()


def start_append_app():
    app = AppendApp()
    app.start()


def main():
    mode = eval_mode()
    if mode is None:
        err = "unknown first arg, use either 'cd-history clean', 'cd-history append /path/to/dir' "
        "or default mode (type 'cd-history -h' for instructions for default mode)"
        print(err, file=sys.stderr)
        exit(1)
    if mode is Mode.DEFAULT:
        start_default_app()
    elif mode is Mode.CLEAN:
        start_clean_app()
    else:
        start_append_app()


if __name__ == "__main__":
    main()
