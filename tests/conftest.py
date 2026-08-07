"""
Some useful information for the dev:

This code below is to set it for the whole file:
```
pytestmark = pytest.mark.additional
```

This is to set a marker to one specific test method:
```
@pytest.mark.mandatory
def test_transition_mandatory():
```
or
```
@pytest.mark.additional
def test_transitions():
```

And you have to add this in the 'pyproject.toml' file:
```
[tool.pytest.ini_options]
markers = [
    "mandatory: mandatory tests for release",
    "additional: exhaustive and demanding tests"
]
```
"""
from pytest_easy import TestFilesHandler

import pytest


pytest_plugins = ['pytest_easy.hooks', 'pytest_asyncio']

TESTS_LOG_FILENAME = 'test_files/tests.log'

@pytest.fixture(scope = 'session', autouse = True)
def setup_and_teardown_session(
    request
):
    """
    Method to remove the folder for temporary files when
    the testing process has finished.
    """
    from printer_easy import ConsolePrinter

    # Code to run at the begining
    ConsolePrinter().deactivate_print()
    test_files_handler = TestFilesHandler()

    yield
    
    # Code to run after all tests have finished
    test_files_handler.delete_new_files()