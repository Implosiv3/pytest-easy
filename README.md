# Pytest, but made easy

The easiest way to test your projects with `pytest`.

# Why?
I had some tests that, when running all together, were failing due to memory issues. This is the way I solved it, and also I can log the results of my tests and clean the tests files folders very easy each time the tests are executed.

# Functionality
__Simplify__ the way we do our tests in python __and run tests individually__ to be more accurate (and a bit slower, but is testing, accuracy is more important).

There are 2 tags:
- __`mandatory`__ for the tests that __must be tested and passed always__ in order to go on, make a commit or upload a new version.
- __`additional`__ for the tests that are validating some optional or experimental functionality that is __not needed for a commit or a new version__.

You should tests always the `mandatory` to know that your app base code is still working, even though some experimental features could fail.

# Usage
The `tests` folder will be your new friend. Keep a `test_general.py` to always do a simple test. Have the `conftest.py` to configure what has to be done before and after the tests are running.

This will execute the tests and remove all the new files in the `test_files` folder that were not before the tests were executed, or you can simply comment the `test_files_handler.delete_new_files()` line before running them, so the generated files are not removed in that execution, uncomment it, and they won't be removed in the next execution because they were already there.

There are some `.bat` files included to run the tests in 3 different modes:
1. `run_tests.bat` - Non-isolated mode, normal mode.
2. `run_tests_isolated.bat` - Isolated mode, our way.
3. `run_mandatory_tests.bat` - Run only the tests with the `@mandatory` pytest mark.

Check `test_various.py` to see more examples.