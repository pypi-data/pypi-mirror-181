from inspect import FrameInfo
from unittest.mock import MagicMock

import howigothere.utils

from .utils import TestsBase


class TestAuxFunctions(TestsBase):

    def test_get_path(self):
        frame_info = MagicMock(FrameInfo)
        frame_info.filename = "/quick/brown/fox/jumps/over/the/lazy/tests.py"

        self.assertEqual(
            howigothere.utils.get_path(frame_info, None),
            "/quick/brown/fox/jumps/over/the/lazy/tests.py",
        )
        self.assertEqual(
            howigothere.utils.get_path(frame_info, 999),
            "quick/brown/fox/jumps/over/the/lazy/tests.py",
        )
        self.assertEqual(
            howigothere.utils.get_path(frame_info, 2),
            "the/lazy/tests.py",
        )
        self.assertEqual(
            howigothere.utils.get_path(frame_info, 1),
            "lazy/tests.py",
        )
        self.assertEqual(
            howigothere.utils.get_path(frame_info, 0),
            "tests.py",
        )

    def test_ct(self):
        self.assertEqual(
            howigothere.utils.ct("TeSt", "", False, ""),
            "TeSt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "", False, "rEsEt"),
            "TeSt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "", True, ""),
            "TeSt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "", True, "rEsEt"),
            "TeSt",
        )

        self.assertEqual(
            howigothere.utils.ct("TeSt", "CoL", False, ""), "CoLTeSt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "CoL", False, "rEsEt"), "CoLTeStrEsEt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "CoL", True, ""), "TeSt",
        )
        self.assertEqual(
            howigothere.utils.ct("TeSt", "CoL", True, "rEsEt"), "TeSt",
        )
