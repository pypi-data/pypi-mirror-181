"""
HowIGotHere example.
"""

import sys

from settings_collector import sc_settings
from howigothere import howigothere


namespace_x_colors: dict[str, str]
try:
    from colorama import Fore
except ImportError:
    sys.stderr.write(
        "This example would be more colourful if you ran it in an environment"
        " that has colorama installed. :-)\n",
    )
    namespace_x_colors = dict()
else:
    namespace_x_colors = {
        "howigothere__x__color_reset": Fore.RESET,
        "howigothere__x__color_sep": Fore.BLUE,
        "howigothere__x__color_func": Fore.RED,
        "howigothere__x__color_path": Fore.GREEN,
        "howigothere__x__color_lineno": Fore.YELLOW,
    }


def f():
    """
    Call inner function to print various `howigothere()` outputs.
    """
    def g():
        """
        Print various `howigothere()` outputs.
        """
        print("Default:            ", howigothere())
        print("Namespace 'x':      ", howigothere(namespace="x"))
        print("Local arguments:    ", howigothere(sep=" ==> ", keep_dirs=None))
        print("Namespace 'mono':   ", howigothere(namespace="mono"))
        print("Local monochrome:   ", howigothere(no_color=True))
        print("Namespace 'mono__y':", howigothere(namespace="mono__y"))
    g()


if __name__ == "__main__":
    sc_settings.update({
        "howigothere__x__trim_paths": 2,
        "howigothere__x__sep": "~~>",
        "howigothere__x__call_format": "{function} [{lineno}: {path}]",
        **namespace_x_colors,
        "howigothere__mono__no_color": True,
        "howigothere__mono__y__call_format": "{function}",
    })
    f()
