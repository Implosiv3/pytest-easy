# Pytest, but made easy

The easiest way to test your projects with `pytest`.

# Functionality
Simplify the way we do our tests in python, and also is able to run the tests individually to be more accurate but a bit slower.

I had some tests that, when running all together, were failing due to memory issues. This is the way I solved it, and also I can log the results of my tests and clean the tests files folders very easy each time the tests are executed.

# Usage
The `tests` folder will be your new friend. Keep a `test_general.py` to always do a simple test. Have the `conftest.py` to configure what has to be done before and after the tests are running.

This will execute the tests and remove all the new files in the `test_files` folder that were not before the tests were executed, or you can simply comment the `test_files_handler.delete_new_files()` line before running them, so the generated files are not removed in that execution, uncomment it, and they won't be removed in the next execution because they were already there.

That is the easiest way to test and see the file results.

Check `test_various.py` to see more examples.