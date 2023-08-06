import importlib
import inspect
import re
from unittest import mock
import sys

from howigothere import main

from .utils import TestsBase, SomeClass, MockColorama


class TestHowIGotHere(TestsBase):

    def test_howigothere(self):
        frameinfo = inspect.getframeinfo(inspect.currentframe())
        result_with_sfd = SomeClass.some_method("tests")
        result_with_sfd_bogus = SomeClass.some_method("bogus dir")
        result_with_sfds = SomeClass.some_method(("src", "tests"))
        result_without_sfd = SomeClass.some_method(None)
        lineno = frameinfo.lineno
        self.assertEqual(
            result_with_sfd,
            f"test_howigothere (tests/test_howigothere.py:{lineno + 1})"
            f" > some_method (tests/utils.py:51)"
            f" > some_inner_function (tests/utils.py:47)",
        )
        self.assertEqual(result_with_sfd_bogus, "")
        self.assertEqual(
            result_with_sfds,
            f"test_howigothere (tests/test_howigothere.py:{lineno + 3})"
            f" > some_method (tests/utils.py:51)"
            f" > some_inner_function (tests/utils.py:47)",
        )
        result_with_sfd_moved = (
            f"test_howigothere (tests/test_howigothere.py:{lineno + 4})"
            f" > some_method (tests/utils.py:51)"
            f" > some_inner_function (tests/utils.py:47)",
        )
        self.assertTrue(
            result_without_sfd.endswith(result_with_sfd_moved)
            and len(result_without_sfd) > len(result_with_sfd_moved),
        )

    def test_defaults_without_colorama(self):
        self.assertEqual(main._default_col_reset, "")
        self.assertEqual(main._default_col_sep, "")
        self.assertEqual(main._default_col_func, "")
        self.assertEqual(main._default_col_path, "")
        self.assertEqual(main._default_col_lineno, "")

    def _assert_comes_from_mock(self, s: str):
        self.assertTrue(re.match(r"^(?:foo)*$", s))

    def test_defaults_with_colorama(self):
        try:
            with mock.patch.dict(sys.modules, {"colorama": MockColorama}):
                importlib.reload(main)
                self._assert_comes_from_mock(main._default_col_reset)
                self.assertEqual(main._default_col_sep, "")
                self._assert_comes_from_mock(main._default_col_func)
                self._assert_comes_from_mock(main._default_col_path)
                self._assert_comes_from_mock(main._default_col_lineno)
        finally:
            importlib.reload(main)
