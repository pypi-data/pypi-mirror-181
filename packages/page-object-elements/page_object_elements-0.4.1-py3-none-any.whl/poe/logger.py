import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from poe.utility import load_config


class TestLogger(logging.Logger):
    def __init__(self, *, location_path, folder='LOGS', log_name='log', level='INFO', stdout='False'):
        super().__init__("logger")
        self.level = getattr(logging, level)
        if eval(stdout):
            self.addHandler(_StdOutHHandler(level))
        self.addHandler(TxtFileHandler(location_path=location_path, folder=folder, log_name=log_name))
        self.handled_element_exceptions: list[dict[
                                              str:str,
                                              str:str,
                                              str:list[str],
                                              str:bool]] = []


class _StdOutHHandler(logging.StreamHandler):
    def __init__(self, level):
        self.stream = sys.stdout
        self.level = getattr(logging, level)
        super().__init__(self.stream)
        self.setFormatter(StdOutFormatter())


class TxtFileHandler(logging.FileHandler):
    def __init__(self, *, location_path, folder, log_name):
        self.filename = f'{log_name}_{datetime.now().strftime("%d-%m-%y__%H-%M-%S")}.log'
        (location_path / folder).mkdir(exist_ok=True, parents=True)
        super().__init__(str(location_path / folder / self.filename))
        self.setFormatter(TxtFileFormatter())


class TxtFileFormatter(logging.Formatter):
    def __init__(self):
        self.fmt = '%(asctime)s | %(levelname)8s | %(message)s'
        super().__init__(self.fmt)


class StdOutFormatter(logging.Formatter):
    """Logging colored formatter for stdout"""
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self):
        super().__init__()
        self.fmt = '%(asctime)s | %(levelname)8s | %(message)s'
        self.formats = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


LEVEL = 'DEBUG'
LOG_NAME = 'log'
STDOUT = 'False'
LOGS_DIR = Path(os.getcwd())

config = load_config()
try:
    if config is not None:
        LEVEL = config['LOGGER']['level']
        print(f'Loaded log LEVEL from config [{LEVEL}]')
        STDOUT = config['LOGGER']['stdout']
        print(f'Loaded STDOUT state from config [{STDOUT}]')
        LOG_NAME = config['LOGGER']['log_name']
        print(f'Loaded LOG_NAME from config [{LOG_NAME}]')
        LOGS_DIR = Path(config['LOGGER']['logs_absolute_path'])
        print(f'Loaded LOGS_ABSOLUTE_PATH from config [{LOGS_DIR}]')
except KeyError as e:
    print(f'{e} is not valid key or not set in [poe.ini]. Default value will be used.')
except Exception as e:
    print('\n'.join([str(e), traceback.format_exc()]))

logger = TestLogger(location_path=LOGS_DIR, log_name=LOG_NAME, level=LEVEL, stdout=STDOUT)

if __name__ == '__main__':
    logger = TestLogger(location_path=LOGS_DIR, folder='test-logger', stdout='True')
    logger.info('test')
    logger.debug('test')
    logger.warning('test')
    logger.error('test')
    logger.fatal('test')
