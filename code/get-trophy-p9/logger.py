"""Replace print for logging."""
import logging
import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_COLOR_SEQ = "\033[1;%dm"

COLORS = {
    "DEBUG": COLOR_SEQ % BLUE,
    "INFO": COLOR_SEQ % GREEN,
    "WARNING": COLOR_SEQ % YELLOW,
    "ERROR": COLOR_SEQ % RED,
    "CRITICAL": BOLD_COLOR_SEQ % RED,
}


class ColoredFormatter(logging.Formatter):
    """Color message."""

    def format(self, record):
        """Override format for coloring."""
        levelname = record.levelname
        if levelname in COLORS:
            record.msg = RESET_SEQ + record.msg
            y = COLORS[levelname] + logging.Formatter.format(self, record)
        else:
            y = logging.Formatter.format(self, record)
        return y


class ErrorExiter(logging.Handler):
    """Exit on error logging."""

    def emit(self, record):
        """Exit when error."""
        logging.shutdown()
        sys.exit(-1)


FORMAT = "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)s] %(message)s"
DATE_FORMAT = r"%Y-%m-%d %H:%M:%S"


def _get_logger():
    stream_handler = logging.StreamHandler()
    formatter = ColoredFormatter(FORMAT, DATE_FORMAT)
    stream_handler.setFormatter(formatter)

    error_exiter = ErrorExiter(level=logging.ERROR)

    y = logging.getLogger()
    y.addHandler(stream_handler)
    y.addHandler(error_exiter)
    y.setLevel(logging.DEBUG)
    return y


LOGGER = _get_logger()
