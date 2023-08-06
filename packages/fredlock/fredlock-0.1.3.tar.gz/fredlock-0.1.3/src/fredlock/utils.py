"""
Utilities
"""
import logging
import signal
from signal import signal, getsignal, SIGINT
from contextlib import contextmanager

log = logging.getLogger(__name__)


@contextmanager
def keyboard_interrupt_protection(on_abort='Keyboard Interrupt Detected'):
    """ Context manager for keyboard interrupt protection """
    original = getsignal(SIGINT)

    def handle_abort(signum, frame):
        """ Handle Ctrl-C """
        log.debug("Got signal %s for frame %s", signum, frame)
        log.warning(on_abort)

    signal(SIGINT, handle_abort)

    try:
        log.debug('Started protection from Ctrl-C')
        yield
    finally:
        log.debug('Returning control to default signal handler')
        signal(SIGINT, original)
