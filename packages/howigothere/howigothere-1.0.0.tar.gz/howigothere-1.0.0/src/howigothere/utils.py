"""
Utility functions used by `howigothere()`.
"""

import inspect
import os
import os.path

from typing import Optional


def get_path(frame_info: inspect.FrameInfo, keep_dirs: Optional[int]) -> str:
    """
    Return path or a part of it, depending on the arguments.
    """
    if keep_dirs is None:
        return frame_info.filename
    else:
        fname = cutoff = frame_info.filename
        for _ in range(keep_dirs + 1):
            cutoff = os.path.dirname(cutoff)
            if not cutoff or cutoff == os.sep:
                break
        if cutoff:
            if not cutoff.endswith(os.sep):
                cutoff = f"{cutoff}{os.sep}"
            fname = fname[len(cutoff):]
        return fname


def ct(s: str, color: str, no_color: bool, color_reset: str) -> str:
    """
    Return colored text, depending on the arguments.
    """
    return s if no_color or not color else f"{color}{s}{color_reset}"
