"""
Module to be able to run the tests isolated, one
by one, so we can free the memory in between when
dealing with libraries like 'numpy' or 'moderngl'
that need a lot of real memory and is not able to
free it within the same process.
"""
from printer_easy import _print_color

import subprocess
import sys


def collect_tests(
    do_only_mandatory: bool = False
):
    cmd = ['pytest', '--collect-only', '-q']

    if do_only_mandatory:
        cmd.extend(['-m', 'mandatory'])

    result = subprocess.run(
        cmd,
        capture_output = True,
        text = True,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)

    tests = []
    for line in result.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        if "::" not in line:
            continue

        tests.append(line)

    return tests


def run_test(
    test
):
    print(f'{test}')

    result = subprocess.run(
        ['pytest', '-q', test],
    )

    return result.returncode


def _print_red(
    message: str
) -> None:
    """
    *For internal use only*

    Print a message in console in red color.
    """
    return _print_color(message, '31')


def _print_green(
    message: str
) -> None:
    """
    *For internal use only*

    Print a message in console in green color.
    """
    return _print_color(message, '32')