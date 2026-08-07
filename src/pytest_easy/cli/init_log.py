from pytest_easy.memory_usage import TESTS_LOG_FILENAME, _print_and_log
from printer_easy import ConsolePrinter

import argparse


def _init_log(
    project_name: str
):
    """
    *For internal use only*

    Empty the log file to be able to start a new
    log due to the testing.
    """
    do_print = ConsolePrinter()._do_print
    do_write_file = ConsolePrinter()._do_write_file
    
    ConsolePrinter().empty_file(TESTS_LOG_FILENAME)
    _print_and_log(f'---   Testing  > {project_name} <   ---')

    # Preserve previous values to avoid conflicts
    # with other libraries
    ConsolePrinter()._do_print = do_print
    ConsolePrinter()._do_write_file = do_write_file

    return True

def main(
):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('project_name')

    args = argument_parser.parse_args()

    _init_log(args.project_name)

if __name__ == '__main__':
    main()