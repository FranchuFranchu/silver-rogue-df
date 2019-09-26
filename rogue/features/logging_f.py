import logging
from logging.handlers import RotatingFileHandler
import sys
import argparse
import re

useEscapeSequences = True
try:
    import colorama
    colorama.init()
except ImportError:
    if 'win' in sys.platform():
        # windows, don't use ASCII escape sequences
        useEscapeSequences = False
        
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': WHITE,
    'CRITICAL': RED,
    'ERROR': RED
}

def colorize(text, use_color = useEscapeSequences):
    if use_color:
        text = text.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        text = text.replace("$RESET", "").replace("$BOLD", "")
    return text

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = useEscapeSequences):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        record.msg = colorize(record.msg, self.use_color)
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

class ColoredLogger(logging.Logger):
    FORMAT = "[%(levelname)-18s] %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                

        color_formatter = ColoredFormatter(colorize(self.FORMAT))
        nocolor_formatter = ColoredFormatter(colorize(self.FORMAT, False), use_color = False)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        filehandler = RotatingFileHandler('../logs/rogue.log', mode = 'a', backupCount = 5)
        filehandler.doRollover()
        filehandler.setFormatter(nocolor_formatter)

        self.addHandler(filehandler)
        self.addHandler(console)
        return

class ArgumentParsingFeature:
    def init_arguments(self):
        parser = argparse.ArgumentParser('Python rogue-like')
        parser.add_argument('--debug', action = 'store_true', help = 'Debug logging')
        parser.add_argument('--silent', '-s', action = 'count', help = 'Each time this appears the info/warnings/error/criticals are suppressed')
        self.argv = parser.parse_args()
        self.argv.silent = 0 if self.argv.silent == None else self.argv.silent

class LoggingFeature(ArgumentParsingFeature):
    def init_logging(self):
        self.logger = ColoredLogger('rogue')

        if self.argv.debug:
            self.logger.setLevel(10)
        else:
            self.logger.setLevel(self.argv.silent * 10 + 20)
        self.logger.debug("Logging to $BOLDlog.txt")