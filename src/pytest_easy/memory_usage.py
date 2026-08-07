"""
Module to include utils related to printing
and loggin the memory usage of the tests.
"""
from printer_easy import ConsolePrinter

import os
import psutil
import gc
import tracemalloc
import time


TESTS_LOG_FILENAME = 'test_files/tests.log'


def print_and_log_test_memory_usage(
    item
):
    """
    Print and log the memory usage of every test.

    This method must be used
    """
    tracemalloc.start()
    process = psutil.Process(os.getpid())
    test_name = item.nodeid
    
    general_memory_before = process.memory_info().rss / 1024**2
    python_memory_before = tracemalloc.get_traced_memory()[0] / 1024**2

    _print_and_log(f'\n{test_name}')
    _print_and_log(f'-- Before --')
    _print_and_log(f'[MEM] {general_memory_before:.2f} MB')
    _print_and_log(f'[MEM PYTHON] {python_memory_before:.2f} MB')

    start = time.perf_counter()

    yield

    elapsed = time.perf_counter() - start
    seconds = int(elapsed)

    gc.collect()

    general_memory_after = process.memory_info().rss / 1024**2
    python_memory_after = tracemalloc.get_traced_memory()[0] / 1024**2

    _print_and_log(f'-- After --')
    _print_and_log(f'[MEM ] {general_memory_after:.2f} MB')
    _print_and_log(f'[MEM PYTHON] {python_memory_after:.2f} MB')
    _print_and_log(f'-- Total --')
    _print_and_log(f'[TIME] {seconds//60:02}:{seconds%60:02}s')
    _print_and_log(f'[GC OBJECTS]: {str(len(gc.get_objects()))}')

    return True

def _print_and_log(
    message: str
):
    """
    *For internal use only*

    Print and log the `message` provided.
    """
    do_print = ConsolePrinter()._do_print
    do_write_file = ConsolePrinter()._do_write_file

    ConsolePrinter().print(
        message = message,
        output_filename = TESTS_LOG_FILENAME
    )

    # Preserve previous values to avoid conflicts
    # with other libraries
    ConsolePrinter()._do_print = do_print
    ConsolePrinter()._do_write_file = do_write_file

    return