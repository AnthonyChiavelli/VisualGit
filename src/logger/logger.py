"""
Provides high-level logging capabilities

Before sending any log statements, use init_logger() to set up the
logger. After this,
"""
import logging

_logger_initialized = False


def init_logger():
    """
    Set up the logger for use.

    Always call this before attempting a log statement. Failure to do
    so will result in an error being logged through the default root
    logger.
    """

    # Don't initialize things twice
    if _logger_initialized:

        return

    # Provides global logging to stderr
    _global_console_logger = logging.getLogger('_global_console_logger')
    _global_console_logger.setLevel(logging.INFO)
    console_logger_handler = logging.StreamHandler()
    console_logger_handler.setLevel(logging.INFO)
    global_console_logger_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    # Connect channel, logger, and formatter
    console_logger_handler.setFormatter(global_console_logger_format)
    _global_console_logger.addHandler(console_logger_handler)

    # Provides logging of git user interactions to a file
    git_interaction_logger = logging.getLogger('_user_logfile_logger')
    git_interaction_logger.setLevel(logging.INFO)
    console_logger_handler = logging.StreamHandler()
    console_logger_handler.setLevel(logging.INFO)
    global_console_logger_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    # Connect channel, logger, and formatter
    console_logger_handler.setFormatter(global_console_logger_format)
    _global_console_logger.addHandler(console_logger_handler)