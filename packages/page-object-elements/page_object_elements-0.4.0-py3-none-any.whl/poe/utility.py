import configparser
import inspect
import os
from pathlib import Path


def locate_file(dir_path, file):
    file_path = None
    for path in Path(dir_path).rglob(file):
        file_path = path
    if not file_path:
        print(
            f"ConfigFile [{file}] doesn't exist inside [{dir_path}] directory structure. Logger defaults will be used.")
    return file_path


def load_config(directory=Path(os.getcwd()).parent):
    file_path = locate_file(directory, 'poe.ini')
    if file_path:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config
    return None


def get_all_methods_and_properties(clazz):
    return [name for name, value in inspect.getmembers(clazz)]


def get_methods_and_properties(clazz, dont=False, starts_with=''):
    if starts_with == '':
        return [name for name, value in inspect.getmembers(clazz)]
    if not dont:
        return [name for name, value in inspect.getmembers(clazz) if name.startswith(starts_with)]
    else:
        return [name for name, value in inspect.getmembers(clazz) if not name.startswith(starts_with)]


if __name__ == '__main__':
    from poe.logger import TestLogger
    from poe.elements import ScreenElement, SelectElement, LabelElement, SectionElement, InputElement

    logger = TestLogger(folder='utility', stdout=True)
    logger.info(get_methods_and_properties(ScreenElement))
    logger.warning(get_methods_and_properties(LabelElement, dont=True, starts_with='_'))
    logger.error(get_methods_and_properties(SelectElement, dont=True, starts_with='__'))
    logger.warning(get_methods_and_properties(SectionElement, dont=False, starts_with='_'))
    logger.error(get_methods_and_properties(InputElement, dont=False, starts_with='__'))
