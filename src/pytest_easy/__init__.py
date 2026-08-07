"""
The Youtube Autonomous Testing Module.
"""
from typing import Union, Callable
from pathlib import Path
from dotenv import load_dotenv
from functools import wraps

import inspect
import functools
import os
import pytest


TEST_FILES_PATH = 'test_files'
"""
The relative path to the test files
folder. This is the one we should use
in all our projects.
"""


def assert_exception_is_raised(
    function: Callable,
    exception_type: Union[type[Exception], str, None] = None,
    message: Union[str, None] = None
) -> None:
    """
    Version for synchronous functions. Use the
    `assert_exception_is_raised_async` for an
    asynchronous function.

    Validate that calling the provided function
    raises an exception.

    Call this method providing some code defined
    as a function to validate that it is raising
    an exception when called (send the function,
    not the call).

    The `exception_type` can be an Exception, a
    TypeError, a ValueError, a string including
    the name of the exception type to expect, or
    None if the type is not important and must 
    not be checked.

    The `message` can be the string we expect to
    be received as the exception message, or None
    if we don't care about the message. We will
    look for the provided 'message' text inside
    the exception message, it can be a part of 
    the message and not the exact one.

    Here is an example:
    ```
    assert_exception_is_raised(
        function = lambda: ParameterValidator.validate_tuple('tuple', 3),
        exception_type = None,
        message = 'The provided "tuple" parameter is not a tuple.'
    )
    ```
    """
    with pytest.raises(BaseException) as exception:
        result = function()

        if inspect.isawaitable(result):
            raise Exception('The provided "function" is asynchronous, please use "assert_exception_is_raised_async" instead.')

    _validate_exception(
        exception = exception,
        exception_type = exception_type,
        message = message
    )

async def assert_exception_is_raised_async(
    function: Callable,
    exception_type: Union[type[Exception], str, None] = None,
    message: Union[str, None] = None
) -> None:
    """
    Version for asynchronous functions. Use the
    `assert_exception_is_raised` for a
    synchronous version.

    Validate that calling the provided async
    function raises an exception (awaiting).

    Call this method providing some code defined
    as a function to validate that it is raising
    an exception when called (send the function,
    not the call).

    The `exception_type` can be an Exception, a
    TypeError, a ValueError, a string including
    the name of the exception type to expect, or
    None if the type is not important and must 
    not be checked.

    The `message` can be the string we expect to
    be received as the exception message, or None
    if we don't care about the message. We will
    look for the provided 'message' text inside
    the exception message, it can be a part of 
    the message and not the exact one.

    Here is an example with an async iterator
    generator:
    ```
    async def consume():
        async for _ in response.iter_bytes():
            pass

    assert await assert_exception_is_raised_async(
        function = consume,
        exception_type = StreamAlreadyConsumedError
    )
    ```
    """
    with pytest.raises(BaseException) as exception:
        result = function()

        if inspect.isawaitable(result):
            await result

    _validate_exception(
        exception = exception,
        exception_type = exception_type,
        message = message
    )
    
def _validate_exception(
    exception: pytest.ExceptionInfo,
    exception_type: Union[type[Exception], str, None],
    message: Union[str, None]
) -> None:
    """
    *For internal use only*

    Method to validate an exception and its
    message.

    This method has been extracted here to be
    used by the `assert_exception_is_raised`
    and the `assert_exception_is_raised_async`
    methods.
    """
    if isinstance(exception_type, str):
        if exception.type.__name__ != exception_type:
            raise Exception(
                f'Expected exception of type '
                f'"{exception_type}" but obtained '
                f'"{exception.type.__name__}".'
            )

    elif exception_type is not None:
        if not issubclass(exception.type, exception_type):
            raise Exception(
                f'Expected exception of type '
                f'"{exception_type.__name__}" '
                f'but obtained '
                f'"{exception.type.__name__}".'
            )

    if message is not None:
        if message not in str(exception.value):
            raise Exception(
                f'The "{message}" provided '
                f'is not in the exception '
                f'message "{str(exception.value)}".'
            )

def assert_optional_library_is_missing(
    function: callable,
    library_name: str,
):
    """
    This method will check if the 'function'
    provided raises an exception telling us
    that the optional library is not installed
    only if that library is not actually
    installed, and will do nothing if it is
    installed.
    """
    import importlib
    
    is_library_installed = importlib.util.find_spec(library_name) is None

    if not is_library_installed:
        assert_exception_is_raised(
            function = function,
            # message = f'The class "library.YoutubeAPI" needs the "{library_name}" installed. You can install it with this command: pip install library[{library_name}]'
            message = f'needs the "{library_name}" installed. You can install it with this command: pip install'
        )
        
    assert True

def is_dependency_installed(
    dependency_name: str
) -> bool:
    """
    Check if the dependency `dependency_name` is installed
    or not.

    The `dependency_name` is the name to import it and 
    use in the code, not the name in pypi:
    - `PIL` must be used and not `pillow`
    - `cv2` must be used and not `opencv-python`

    Note for developer: This method is duplicated
    somwhere (ask developer) but copied here to avoid
    imports as this library is just for testing and we
    don't want dependencies.
    """
    import importlib

    return importlib.util.find_spec(dependency_name) is not None

def execute_if_dependency_installed(
    dependency_name: str
) -> Union[any, bool]:
    """
    *Decorator*

    Decorator to execute the code only if the dependency
    with the given `dependency_name` is installed in this
    project, returning True in case it was not installed.

    The `dependency_name` is the name to import it and 
    use in the code, not the name in pypi:
    - `PIL` must be used and not `pillow`
    - `cv2` must be used and not `opencv-python`

    Note for developer: This method is duplicated
    somwhere (ask developer) but copied here to avoid
    imports as this library is just for testing and we
    don't want dependencies.
    """
    def decorator(
        func
    ):
        @wraps(
            func
        )
        def wrapper(
            *args,
            **kwargs
        ):
            return (
                func(*args, **kwargs)
                if is_dependency_installed(dependency_name) else
                True
            )
        return wrapper
    
    return decorator

def float_approx_to_compare(float):
    """
    Compare float values with 
    approximation due to the decimal
    differences we can have.

    Then, you can compare floats by
    using:

    - `assert fa == float_approx_to_compare(fb)`
    """
    return pytest.approx(float, rel = 1e-5, abs = 1e-8)


def skip_pytest(
    env_var: str = 'SKIP_TESTS'
):
    """
    *Decorator*

    Decorator to skip the pytest if the env
    variable `env_var` is set and has a valid
    value ('1', 'true', 'yes', ''). This is
    useful when we have some tests we want to
    execute only in local, so we can set the
    variable in remote environments to avoid
    them of being executed.

    The `env_var` is read from the local `.env`
    file.
    """
    def decorator(
        function
    ):
        @functools.wraps(function)
        def wrapper(
            *args,
            **kwargs
        ):
            path = os.getcwd().replace('\\', '/')
            load_dotenv(f'{path}/.env')
            env_var_value = os.getenv(env_var, '').lower()

            if env_var_value in ('1', 'true', 'yes', ''):
                pytest.skip(f'Skipping test "{function.__name__}": file-related tests are disabled by configuration ("{env_var_value}" environment variable).')

            return function(*args, **kwargs)
        
        return wrapper
    
    return decorator

def assert_images_are_identical(
    filename_one: str,
    filename_two: str
):
    """
    *Optional dependency `numpy` (imported as `numpy`) required*
        
    *Optional dependency `pillow` (imported as `PIL`) required*

    Check that the `filename_one` and the `filename_two`
    are 2 identical images by reading them as numpy
    arrays.
    """
    if not is_dependency_installed('numpy'):
        raise Exception('The "numpy" optional library is needed to use this "assert_images_are_identical" functionality. You can install it with this command: pip install pytest_easy[numpy]')

    if not is_dependency_installed('PIL'):
        raise Exception('The "PIL" optional library is needed to use this "assert_images_are_identical" functionality. You can install it with this command: pip install pytest_easy[pillow]')

    from pytest_easy._utils import read_image_as_numpy
    import numpy as np

    assert np.array_equal(
        a1 = read_image_as_numpy(filename_one),
        a2 = read_image_as_numpy(filename_two)
    )

    
def does_file_exist(
    filename: str,
    do_check_is_not_0b: bool = True
) -> bool:
    """
    Return `True` if the `filename` provided exists
    and is a file.

    If `do_check_is_not_0b` is `True`, the file must
    also have a size greater than 0 bytes.
    """
    output_path = Path(filename)

    if not output_path.is_file():
        return False

    if (
        do_check_is_not_0b and
        output_path.stat().st_size == 0
    ):
        return False

    return True
    

class TestFilesHandler:
    """
    Class to easily handle the files we
    create when testing the projects.
    
    This class must be instantiated before
    the tests are executed, and the 
    '.delete_new_files()' method must be
    called when all the tests have finished.
    """

    __test__ = False
    """
    Attribute to be ignored by pytest.
    """

    @property
    def files(
        self
    ) -> list[str]:
        """
        The files that are currently in the
        'test_files' folder.
        """
        return set(os.listdir(self._test_files_path))

    def __init__(
        self,
        test_files_path: str = TEST_FILES_PATH
    ):
        self._test_files_path: str = test_files_path
        """
        The relative path to the test files
        folder.
        """
        self._initial_files: list[str] = self.files
        """
        The files that were available when the
        class was instantiated (before executing
        the tests).
        """

    def delete_new_files(
        self
    ) -> list[str]:
        """
        Delete all the new files found and return
        a list containing the names of the files
        that have been deleted.
        """
        files_removed = []

        for f in self.files - self._initial_files:
            path = os.path.join(self._test_files_path, f)
            if os.path.isfile(path):
                os.remove(path)
                files_removed.append(path)

        return files_removed