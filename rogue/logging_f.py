import logging
import sys
import argparse

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

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': WHITE,
    'CRITICAL': RED,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = useEscapeSequences):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

class ColoredLogger(logging.Logger):
    FORMAT = "[%(levelname)-18s] %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

class ArgumentParsingFeature:
    def init_arguments(self):
        parser = argparse.ArgumentParser('Python rogue-like')
        parser.add_argument('--debug', action = 'store_true', help = 'Debug logging')
        parser.add_argument('--silent', '-s', action = 'count', help = 'Each time this appears the info/warnings/error/criticals are suppressed')
        self.argv = parser.parse_args()

class LoggingFeature(ArgumentParsingFeature):
    def init_logging(self):
        self.logger = ColoredLogger('rogue')