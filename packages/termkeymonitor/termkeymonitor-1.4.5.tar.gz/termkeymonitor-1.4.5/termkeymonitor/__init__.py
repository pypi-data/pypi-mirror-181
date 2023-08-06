# system modules
import argparse
import collections
import functools
import json
import locale
import logging
import os
import re
import sys

# external modules
import evdev

# internal modules
from termkeymonitor.version import __version__

logger = logging.getLogger(__name__)


def find_input_devices():
    devices = [
        d
        for d in map(evdev.InputDevice, evdev.list_devices())
        if any(s in d.name.lower() for s in ("keyboard", "mouse", "touchpad"))
    ]
    if not devices:
        raise FileNotFoundError(
            "No keyboards/mice found. "
            "Specify input devices via --device. "
            "(try running 'python3 -m evdev.evtest') "
            "Also: Do you have permissions for e.g. /dev/input/...?"
        )
    return devices


def stop_on_keyboardinterrupt(decorated_fun):
    @functools.wraps(decorated_fun)
    def wrapper(*args, **kwargs):
        try:
            decorated_fun(*args, **kwargs)
        except KeyboardInterrupt:
            sys.exit(0)

    return wrapper


KEYMAPS = collections.defaultdict(
    lambda: {
        "BTN_LEFT": "MOUSE-LEFT",
        "BTN_MIDDLE": "MOUSE-MIDDLE",
        "BTN_RIGHT": "MOUSE-RIGHT",
        "BTN_EXTRA": "MOUSE-EXTRA",
        "BTN_SIDE": "MOUSE-SIDE",
        "REL_WHEEL_UP": "SCROLL-UP",
        "REL_WHEEL_DOWN": "SCROLL-DOWN",
    }
)

KEYMAPS["de"].update(
    {
        "KEY_Y": "Z",
        "KEY_Z": "Y",
        53: "MINUS",
        26: "Ü",
        27: "+",
        43: "#",
        12: "ß",
        41: "^",
        40: "Ä",
        39: "Ö",
        86: "<",
        13: "ACCENT",
    }
)


def key_pretty(
    name=None, code=None, show_code=False, keymap=KEYMAPS["default"]
):
    if name is None:
        name = next(
            filter(
                bool,
                (
                    getattr(evdev.ecodes, k, {}).get(code)
                    for k in ("KEY", "BTN")
                ),
            ),
            None,
        )
        if not isinstance(name, str):
            try:
                name = next(iter(name), None)
            except Exception:
                pass
    if show_code and (name is not None or code is not None):
        suffix = " ({})".format(
            " ".join(f"{x!r}" for x in (name, code) if x is not None)
        )
    else:
        suffix = ""
    if s := keymap.get(name):
        return f"{s}{suffix}"
    if s := keymap.get(code):
        return f"{s}{suffix}"
    if s := keymap.get(str(code)):
        return f"{s}{suffix}"
    if name:
        return f"{str(name).removeprefix('KEY_')}{suffix}"
    if code:
        return str(code)
    return "?"


def tryint(x):
    try:
        return int(x)
    except Exception:
        return x


def keymapargtype(value):
    try:
        if keymap := (KEYMAPS.get(value)):
            return keymap
        if os.path.exists(value):
            with open(value) as fh:
                keymap = json.load(fh)
        else:
            keymap = json.loads(value)
            return {**KEYMAPS["default"], **keymap}
        keymap = {tryint(k): str(v) for k, v in keymap.items()}
    except Exception as e:
        raise argparse.ArgumentTypeError(
            """Specify either a JSON object like {"89":"mykey"} """
            f"or a path to a file with such JSON (error: {e})"
        )
    return keymap


default_keymap_name = re.sub(r"_.*$", r"", locale.getdefaultlocale()[0])


def make_argparser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=r"""
 _                   _                              _  _
| |_  ___  _ _ _ __ | |_____  _  _ _ __   ___  _ _ (_)| |_  ___  _ _
|  _|/ -_)| '_| '  \| / / -_)| || | '  \ / _ \| ' \| ||  _|/ _ \| '_|
 \__|\___||_| |_|_|_|_\_\___| \_, |_|_|_|\___/|_||_|_| \__|\___/|_|
                              |__/

                 Show pressed keys in the terminal
useful e.g. to show key presses in an asciinema cast (https://asciinema.org)
"""
        f"""
version {__version__}
""",
    )
    parser.add_argument(
        "-d",
        "--device",
        dest="devices",
        nargs="+",
        help="Input devices to watch (e.g. /dev/input/event4)",
        type=evdev.InputDevice,
        default=[],
    )
    parser.add_argument(
        "-k",
        "--keymap",
        help="either directly JSON or path to "
        "JSON file with object mapping key "
        "codes or names to display strings "
        """(e.g. {"53":"MINUS","KEY_Z":"Y"}) """
        f"or the name of a build-in keymap ({' '.join(KEYMAPS)}). "
        f"Default locale name ({default_keymap_name}) is tried as default. "
        "(Tip: Add --show-code option or run "
        "'python -m evdev.evtest' to see codes and names)",
        type=keymapargtype,
        default=KEYMAPS.get(default_keymap_name, KEYMAPS["default"]),
    )
    parser.add_argument(
        "--show-code", help="Show keycode as well", action="store_true"
    )
    return parser
