from qstyle import QStyle
from argparse import ArgumentParser
import logging

log = logging.getLogger('qstyle')
handler = None
try:
    from log_colorizer import make_colored_stream_handler
    handler = make_colored_stream_handler()
except ImportError:
    handler = logging.StreamHandler()
log.addHandler(handler)

parser = ArgumentParser(
        description='An XCB X composite manager',
        prog='qstyle',
        version="0.1")

parser.add_argument(
    '-l', '--log-level',
    default='DEBUG',
    dest='log_level',
    choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
    help='Set debugging log level')


options = parser.parse_args()
log_level = getattr(logging, options.log_level)
log.setLevel(log_level)

qstyle = QStyle()
