from pytest_easy.memory_usage import print_and_log_test_memory_usage

import pytest


@pytest.hookimpl(hookwrapper = True)
def pytest_runtest_call(
    item
):
    yield from print_and_log_test_memory_usage(item)