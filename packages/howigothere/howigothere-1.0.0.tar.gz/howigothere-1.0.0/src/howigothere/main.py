"""
Return or print the location in the code.
"""

import inspect
import os.path
from typing import Optional

from settings_collector import SettingsCollector, SC_Setting, sc_defaults

from .utils import get_path, ct


_default_col_reset: str
_default_col_sep: str
_default_col_func: str
_default_col_path: str
_default_col_lineno: str
try:
    from colorama import Style, Fore
except ImportError:
    _default_col_reset = ""
    _default_col_sep = ""
    _default_col_func = ""
    _default_col_path = ""
    _default_col_lineno = ""
else:
    _default_col_reset = Style.RESET_ALL
    _default_col_sep = ""
    _default_col_func = Style.BRIGHT + Fore.GREEN
    _default_col_path = Style.BRIGHT + Fore.CYAN
    _default_col_lineno = Fore.CYAN


class HowIGotHereSettings(SettingsCollector):
    class SC_Config:
        prefix = "howigothere"
    keep_dirs = SC_Setting(1, value_type=int)
    sep = SC_Setting(" > ", value_type=str)
    call_format = SC_Setting("{function} ({path}:{lineno})", value_type=str)
    no_color = SC_Setting(False, value_type=bool)
    color_reset = SC_Setting(_default_col_reset, value_type=str)
    color_sep = SC_Setting(_default_col_sep, value_type=str)
    color_func = SC_Setting(_default_col_func, value_type=str)
    color_path = SC_Setting(_default_col_path, value_type=str)
    color_lineno = SC_Setting(_default_col_lineno, value_type=str)
    start_from_dir = SC_Setting(None)


@sc_defaults(HowIGotHereSettings, scope_arg="namespace")
def howigothere(
    *,
    namespace: Optional[str] = None, keep_dirs: Optional[int], sep: str,
    call_format: str, no_color: bool, color_reset: str, color_sep: str,
    color_func: str, color_path: str, color_lineno: str,
    start_from_dir: Optional[str | tuple[str, ...]] = None,
) -> str:
    """
    Return a string describing function calls to where the current spot.

    This is convenient to find out where in the code is something happening and
    how we got there.

    :param namespace: Namespace for the settings. For example, if given as
        `"foo__bar"`, the colour for the separator will be taken from
        `howigothere__foo__bar__color_sep`. If that doesn't exist, it'll be
        taken from `howigothere__foo__color_sep` and, if that doesn't exist
        either, it'll be taken from `howigothere__foo__color_sep` and, if that
        doesn't exist either, it'll be taken from `howigothere__color_sep`.
    :param keep_dirs: The number of directories to keep in each path. For
        example, if set to 2 and some path is `/a/b/c/d/e.py`, the path will be
        displayed as `c/d/e.py` (two directories kept: `c` and `d`). Set to
        `None` to keep the whole path or to 0 to remove the whole path.
    :param sep: A separator between calls.
    :param call_format: A format used to display each call. Currently, it
        supports `{function}` (the name of the function being called), `{path}`
        (a path to the file where the call was made), and `{lineno}` (line
        number where the call was made).
    :param no_color: If set to `True`, `color_*` arguments are ignored and the
        displayed string has no colour markers.
    :param color_reset: The marker to use to reset color. It'll usually be
        Colorama's `Style.RESET_ALL`, but it can be set to something else too,
        especially if a different coloring library is used.
    :param color_*: Color of a sep(arator), func(tion), path, and line number.
    :param start_from_dir: If set as a string, exclude all calls until one
        happens in a file belonging to a directory or subdirectory of
        `start_from_dir` (which is given as either an absolute one or one
        relative to the current working one). If given as a tuple of strings,
        the same kind of matching is done for all strings in that tuple, and
        matching any of the given strings as the call's file's parent directory
        starts the output.
    :return: A string containing a compact stack description of the current
        call.
    """
    cargs = (no_color, color_reset)  # common arguments
    calls = list()
    if start_from_dir is None:
        use_info = True
        start_from_dir = tuple()
    else:
        if isinstance(start_from_dir, str):
            start_from_dir = (os.path.abspath(start_from_dir),)
        else:
            start_from_dir = tuple(os.path.abspath(d) for d in start_from_dir)
        use_info = False

    # `[2:]` because we're skipping `howigothere` itself and its wrapper
    # created by `@sc_defaults`.
    for frame_info in reversed(inspect.stack()[2:]):
        if not use_info:
            path = os.path.abspath(f"{frame_info.filename}{os.sep}")
            if any(path.startswith(d) for d in start_from_dir):
                use_info = True
            else:
                continue
        function = ct(frame_info.function, color_func, *cargs)
        path = ct(get_path(frame_info, keep_dirs), color_path, *cargs)
        lineno = ct(str(frame_info.lineno), color_lineno, *cargs)
        calls.append(
            call_format.format(function=function, path=path, lineno=lineno),
        )

    return ct(sep, color_sep, *cargs).join(calls)
