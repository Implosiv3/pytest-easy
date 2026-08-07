"""
Module to include functionality related directly
with pytest, such as creating markers or similar.
"""
from typing import Union

import importlib.util
import pytest


def pytest_skip_if_not_dependency(
    dependency_name: str,
    *,
    reason: Union[str, None] = None
):
    """
    Create a `pytest.mark.skipif` mark to skip
    the test if the `dependency_name` provided
    is not installed.
    """
    is_installed = importlib.util.find_spec(dependency_name) is not None
    reason = (
        reason
        or
        f'Dependency "{dependency_name}" is not installed'
    )

    return pytest.mark.skipif(
        not is_installed,
        reason = reason,
    )