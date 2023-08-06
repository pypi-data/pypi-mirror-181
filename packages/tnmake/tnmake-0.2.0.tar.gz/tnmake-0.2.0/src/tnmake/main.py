from argparse import ArgumentParser, ArgumentTypeError
from os.path import abspath, exists
from sys import exc_info as debug
from traceback import extract_tb as traceback

from tnmake.logging import get_basic_logger

logger = get_basic_logger()  # stdout only
from tnmake import __project__, __version__
from tnmake.tnmake import Thumbnail # thumbnail class


def apt_path_exists(path: str) -> str:
    '''
    check if passed path to Argsparser exists
    :return: path or ArgumentTypeError
    '''
    if not exists(path):

        raise ArgumentTypeError('No such file or directory')

    return abspath(path) # return absolute path

def main():

    '''
    Here is the ENTRYPOINT for `pip` and `standalone` versions
    '''

    parser = ArgumentParser(description = f'{__project__} creates thumbnails with some additional information')
    # add cli arguments
    parser.add_argument(
        '-i', '--input',
        required = True,
        help = f'set video filepath',
        metavar = 'path',
        type = apt_path_exists)
    parser.add_argument(
        '-o', '--output',
        help = 'force a custom output filepath',
        metavar = 'path')
        # type=abspath,
        # default=getcwd()) # use the current working directory as default
    parser.add_argument(
        '-w', '--width',
        type = int,
        help = 'set width of the output image',
        metavar = 'px',
        default = 1150)
    parser.add_argument(
        '--comment',
        type = str,
        help = 'append a thumbnail annotation',
        metavar = 'annotation',
        default = '') # let it empty if you won't append any commment
    parser.add_argument(
        '--grid',
        type = str,
        help = 'set layout of the output thumbnail',
        metavar = 'layout',
        default = '3x8') # predefined layout consists of 3 cols & 8 rows
    parser.add_argument(
        '-e', '--extension',
        help = 'choose the output extension (default: "jpg")',
        choices = ['bmp', 'jpg', 'png'],
        default = 'jpg')
    parser.add_argument(
        '-q', '--quality',
        type = int,
        help = 'set quality, affects lossy image formats only',
        metavar = 'x',
        default = 100) # quality gets over the space usage
    parser.add_argument(
        '-f', '--font',
        type = str,
        help = 'select an available font or pass a path to a desired fontfile',
        metavar = 'path')
    parser.add_argument(
        '-s', '--size',
        type = int,
        help = 'set desired fontsize (default: 13px)',
        metavar = 'px')
    parser.add_argument(
        '-v', '--verbose',
        action = 'store_true',
        default = False,
        help = 'enable verbose mode')
    parser.add_argument(
        '-V', '--version',
        action = 'version',
        version = f'{__project__} v{__version__}')
    args = parser.parse_args() # evaluate all arguments and pass 'em through
    if args.verbose:
        logger.setLevel(10)
    options = {
        'font': args.font, # set defaults in class itself
        'size': args.size,
        'layout': args.grid, # 3x8
        'comment': args.comment,
        'ext': args.extension,
        'width': args.width, # 1150
        'quality': args.quality # 100 is preferable for quality purpose
        }
    try:
        Thumbnail(options).perform(args.input, args.output) # Run `pip` version
    except Exception as e:
        position = traceback(debug()[2])[-1]
        print(f'Exception: {"".join(str(e).split(chr(10)))} (see@{position[2]}:{position[1]})')

# Thumbnail!MAKER creates customisable thumbnails and adds some tech details in the picture's header
