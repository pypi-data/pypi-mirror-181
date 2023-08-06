"""
Module contains a single class. Some tricks applied, like disabling
garbage collection(it may affect execution time) and using a timing
function designed to performance-measurement use cases.
"""
import gc
import logging
import time

__all__ = ['PerfTimer', 'Timer']

from typing import Callable, Optional

logger = logging.getLogger(__name__)


def _readable_time():
    return time.strftime('%Y %b %d %H:%M:%S +0000',
                         time.gmtime(time.time()))


def _printer(stuff):
    print(stuff)


class _ContextDecorator:
    def __call__(self, func):
        def callback(*args, **kwargs):
            with self:
                func(*args, **kwargs)

        return callback

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class PerfTimer(_ContextDecorator):
    """
    This class can be used as both context manager and function decorator.
    It prints string with formatted time before executing targeted code, and
    follows with the message about time spent executing user's code.
    Examples:
    with PerfTimer():
        ...

    or
ø
    @PerfTimer()
    def workload():
        ...

    Example output will be like:
    > 2020 May 31 19:36:30 +0000 ==== started
    > 2020 May 31 19:36:30 +0000 ==== elapses 0.00000 seconds
    """
    def __init__(self, scope=None, printer=_printer):
        self.scope = scope or '===='
        self.printer = printer
        self.gcold = None
        self.start = None

    def __enter__(self):
        self.gcold = gc.isenabled()
        gc.disable()
        time_readable = _readable_time()
        self.printer(f'{time_readable} {self.scope} started')
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        if self.gcold:
            gc.enable()
        time_readable = _readable_time()
        result_time = end - self.start
        self.printer(
            f'{time_readable} {self.scope} elapsed {result_time:.5f} seconds')


class Timer(_ContextDecorator):
    """
    This class can be used as both context manager and function decorator.
    It expects function as constructor parameter that is executed at the end
    of the code section.
    Examples:
    def printer(seconds):
        print(f'code block 1: {seconds:.5f} elapsed')

    with Timer(printer):
        ...

    or

    @Timer(printer)
    def workload():
        ...

    Example output will be like:
    > code block 1: 0.00000 elapsed
    """
    def __init__(self, time_teller: Optional[Callable[[float], None]]):
        self.time_teller = time_teller
        self.start = None

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        result_time = end - self.start
        self.time_teller(result_time)
