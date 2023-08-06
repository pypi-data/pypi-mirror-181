# system modules
import sys
import asyncio
import os

# external modules
import evdev
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

# internal modules
import termkeymonitor
from termkeymonitor import (
    KEYMAPS,
    find_input_devices,
    key_pretty,
    make_argparser,
    stop_on_keyboardinterrupt,
)

console = Console()


@stop_on_keyboardinterrupt
def cli():
    parser = make_argparser()
    args = parser.parse_args()
    console.log(args)

    layout = Layout(name="root")
    with Live(
        layout,
        screen=True,
        transient=True,
        refresh_per_second=sys.float_info.min,
        console=console,
    ) as live:

        def update(text):
            c = Align(
                Text(text, justify="center", style="bold"),
                align="center",
                vertical="middle",
            )
            layout["root"].update(
                c
                if os.get_terminal_size().lines < 3
                else Panel(
                    c,
                    title="   ".join(
                        v
                        for k, v in {
                            "keyboard": " Keyboard",
                            "mouse": "Mouse",
                            "touchpad": "Touchpad",
                        }.items()
                        if any(k in d.name.lower() for d in args.devices)
                    ),
                )
            )
            live.refresh()

        if not args.devices:
            update("🔎 Searching for input devices...")
            args.devices = find_input_devices()
        update(
            f"✅ Using input devices:{chr(10)}"
            f"{chr(10).join([d.path+' ('+d.name+')' for d in args.devices])}",
        )

        active_keys = set()

        def show_active_keys():
            update(
                " ".join(
                    key_pretty(
                        code=code,
                        keymap=args.keymap,
                        show_code=args.show_code,
                    )
                    for code in active_keys
                )
            )

        async def handle_events(device):
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    if event.value > 0:
                        active_keys.add(event.code)
                    elif event.code in active_keys:
                        active_keys.remove(event.code)
                    for key in ("REL_WHEEL_UP", "REL_WHEEL_DOWN"):
                        if key in active_keys:
                            active_keys.remove(key)
                    show_active_keys()
                if event.type == evdev.ecodes.EV_REL:
                    if event.code == evdev.ecodes.REL_WHEEL:
                        if event.value > 0:
                            active_keys.add("REL_WHEEL_UP")
                            if "REL_WHEEL_DOWN" in active_keys:
                                active_keys.remove("REL_WHEEL_DOWN")
                        else:
                            active_keys.add("REL_WHEEL_DOWN")
                            if "REL_WHEEL_UP" in active_keys:
                                active_keys.remove("REL_WHEEL_UP")
                        show_active_keys()

        for device in args.devices:
            asyncio.ensure_future(handle_events(device))

        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    cli()
