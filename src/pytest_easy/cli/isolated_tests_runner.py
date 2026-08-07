from pytest_easy.isolated_runner import collect_tests, run_test, _print_green, _print_red

import argparse
import sys


def main(
):
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument(
        '--stop-if-failed',
        action = 'store_true',
        help = 'Stop execution immediately when a test fails'
    )
    arguments_parser.add_argument(
        '--mandatory-only',
        action = 'store_true',
        help = 'Execute only the mandatory tests'
    )
    args = arguments_parser.parse_args()

    # Force to only mandatory tests
    do_only_mandatory = (
        True
        if args.mandatory_only else
        False
    )

    tests = collect_tests(do_only_mandatory)

    failed = []
    passed = []

    for test in tests:
        # Remove comments for for manual testing
        # passed.append(test)
        # if len(passed) == 1:
        #     failed.append(test)
        # continue
        code = run_test(test)

        if code == 0:
            passed.append(test)
        else:
            failed.append(test)
            if args.stop_if_failed:
                print('\nTest failed. Stopping execution due to the "--stop-if-failed" option.')
                sys.exit(1)

    print('\n====================')
    print(f'Passed: {len(passed)}')
    print(f'Failed: {len(failed)}')

    if passed:
        print('\nPassed tests:')
        for test in passed:
            _print_green(test)

    if failed:
        print('\nFailed tests:')
        for test in failed:
            _print_red(test)

        sys.exit(1)

    print('\nAll tests passed.')

if __name__ == '__main__':
    main()