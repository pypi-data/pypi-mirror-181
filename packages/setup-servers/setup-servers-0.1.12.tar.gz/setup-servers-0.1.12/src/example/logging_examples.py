import logging
import sys


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[92;1m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATTERS = {
        logging.DEBUG: logging.Formatter(grey + format + reset),
        logging.INFO: logging.Formatter(green + format + reset),
        logging.WARNING: logging.Formatter(yellow + format + reset),
        logging.ERROR: logging.Formatter(red + format + reset),
        logging.CRITICAL: logging.Formatter('\u001b[95;1m' + format + reset)
    }

    def format(self, record):
        formatter = self.FORMATTERS.get(record.levelno)
        return formatter.format(record)


handler = logging.StreamHandler(stream=sys.stdout)
handler.formatter = CustomFormatter()
logger = logging.Logger(name='Shahim')
logger.addHandler(handler)

logger.info("Test")
logger.error("Critical")
logger.critical("Critical")
