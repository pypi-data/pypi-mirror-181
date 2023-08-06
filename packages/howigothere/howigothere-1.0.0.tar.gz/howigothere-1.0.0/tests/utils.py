"""
Testing utilities.
"""

import unittest
from typing import Optional

from howigothere import howigothere


try:
    import colorama  # noqa: W0601
except ImportError:
    pass
else:
    raise RuntimeError(
        "tests must be run in an environment that doesn't provide colorama.\n"
        "Try using a virtual environment:\n"
        "    python -m venv venv && . venv/bin/activate && pip install -r"
        " requirements_dev.txt && ./run_tests.sh && deactivate",
    )


class TestsBase(unittest.TestCase):
    """
    The base unit tests class, used as a foundation for all other unit tests.
    """

    def setUp(self):
        """
        For future uses (common resets between runs).
        """
        pass

    def tearDown(self):
        """
        For future uses (common resets between runs).
        """
        pass


class SomeClass:

    @staticmethod
    def some_method(start_from_dir: Optional[str | tuple[str, ...]]):
        def some_inner_function() -> str:
            return howigothere(
                no_color=True,
                start_from_dir=start_from_dir,
            )
        return some_inner_function()


class _MockColoramaConstant:

    def __getattr__(self, name: str) -> str:
        return "foo"


class MockColorama:

    Back = _MockColoramaConstant()
    Fore = _MockColoramaConstant()
    Style = _MockColoramaConstant()
