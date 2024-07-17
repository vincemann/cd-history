import logging
import sys

from cd_history import config


def configure_logger(name):
    logger = logging.getLogger(name)
    # if config.debug=True set log level to debug, otherwise use warn
    if config.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # If config.log_file is set, write logs to file
    if hasattr(config, 'log_file') and config.log_file:
        file_handler = logging.FileHandler(config.log_file)
        if config.debug:
            file_handler.setLevel(logging.DEBUG)
        else:
            file_handler.setLevel(logging.WARN)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # otherwise write to stderr (stdout is reserved for interprocess communication)
        stderr_handler = logging.StreamHandler(sys.stderr)
        if config.debug:
            stderr_handler.setLevel(logging.DEBUG)
        else:
            stderr_handler.setLevel(logging.WARN)
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)

    return logger
