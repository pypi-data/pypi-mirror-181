import logging
from sys import stdout


def init_logging_config() -> None:
    '''
    Init 'basic' Configuration
    '''
    logging.basicConfig(
        datefmt='%d %b %H:%M:%S',
        # level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler(stdout)])

def get_basic_logger() -> logging.Logger:
    '''
    Convenience Method to Load the App Logger
    :return: An Instance of the App Logger
    '''
    return logging.getLogger('Thumbnail!MAKER')
