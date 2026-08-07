import pytest


@pytest.mark.mandatory
@pytest.mark.asyncio
async def test_various():
    from pytest_easy import float_approx_to_compare, TestFilesHandler, assert_exception_is_raised, assert_exception_is_raised_async, execute_if_dependency_installed, is_dependency_installed, assert_images_are_identical, does_file_exist

    # Validate exceptions
    assert_exception_is_raised(lambda: 1 / 0, exception_type = None, message = None)
    assert_exception_is_raised(lambda: 1 / 0, exception_type = None, message = 'division by zero')
    assert_exception_is_raised(lambda: 1 / 0, exception_type = None, message = 'division by zero')
    # The exception we expect is not ok, so we expect
    # an exception because of that unexpected exception
    async def assert_exception():
        await assert_exception_is_raised_async(
            function = lambda: 1 / 0,
            exception_type = 'Invented',
            message = 'division by zero'
        )
    await assert_exception_is_raised_async(
        function = assert_exception,
        exception_type = Exception,
        message = 'Expected exception of type "Invented" but obtained "ZeroDivisionError".'
    )

    async def assert_exception():
        await assert_exception_is_raised_async(
            function = lambda: 1 / 0,
            exception_type = ZeroDivisionError,
            message = 'not message'
        ),
    await assert_exception_is_raised_async(
        function = assert_exception,
        exception_type = Exception,
        message = 'The "not message" provided'
    )
    assert_exception_is_raised(lambda: TestFilesHandler('non-exist'))
    assert_exception_is_raised(lambda: TestFilesHandler('non-exist'), message = "The system cannot find the path specified: 'non-exist'")

    # TODO: Test optional class if possible

    assert 3.99 == float_approx_to_compare(3.99)
    # 'test.txt' and maybe 'tests.log'
    assert len(TestFilesHandler().files) in [1, 2]

    @execute_if_dependency_installed('opencv-python')
    def get_22():
        return 22
    
    assert not is_dependency_installed('opencv-python')

    assert get_22() == True

    assert_exception_is_raised(
        function = lambda: assert_images_are_identical('test', 'test'),
        message = 'The "yta_numpy" optional library is needed to use this "assert_images_are_identical" functionality. You can install it with this command: pip install yta_testing[yta_numpy]'
    )

    # Asynchronous
    class CustomAsyncError(Exception):
        pass

    async def failing_async_function():
        raise CustomAsyncError(
            'Async exception raised correctly.'
        )
    
    async def failing_async_lambda_function():
        raise CustomAsyncError(
            'Async lambda exception.'
        )
    
    await assert_exception_is_raised_async(
        function = failing_async_function,
        exception_type = CustomAsyncError,
        message = 'Async exception raised correctly.'
    )

    await assert_exception_is_raised_async(
        function = lambda: failing_async_lambda_function(),
        exception_type = CustomAsyncError,
        message = 'Async lambda exception.'
    )

    assert does_file_exist('test_files/test.txt')
    assert not does_file_exist('test_files/file_that_doesnt_exist.tmp')

    # TODO: Create tests