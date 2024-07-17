import sys

from cd_history.mode import Mode


def eval_mode():
    """
    Parses command-line arguments to determine the mode of operation.

    This function evaluates the command-line arguments (sys.argv) to identify the mode in which the script should run.
    It recognizes three modes: DEFAULT, CLEAN, and APPEND. If the command-line arguments do not match any known mode,
    it returns None.

    Examples:
        - Default mode: 'cd-history --mode=terminal --action=select'
        - Clean mode: 'cd-history clean'
        - Append mode: 'cd-history append'

    Returns:
        Mode: The mode of operation. Can be one of Mode.DEFAULT, Mode.CLEAN, or Mode.APPEND. Returns None if an invalid mode is given.
    """
    if len(sys.argv) <= 1:
        return Mode.DEFAULT
    mode_arg = sys.argv[1]
    if mode_arg.startswith("--") or mode_arg.startswith("-"):
        return Mode.DEFAULT
    if mode_arg == Mode.CLEAN.value:
        return Mode.CLEAN
    elif mode_arg == Mode.APPEND.value:
        return Mode.APPEND
    else:
        return None

