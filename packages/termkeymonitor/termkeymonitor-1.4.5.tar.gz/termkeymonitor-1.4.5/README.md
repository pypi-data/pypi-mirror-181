# ⌨️  Terminal Key Monitor 📟

Show pressed keys in the terminal. Useful e.g. when recording [asciinema screencasts](https://asciinema.org).

`termkeymonitor` connects directly to a local input device using `evdev`.

# 📥 Installation

```bash
# from PyPI
pip install termkeymonitor
# directly from GitLab
pip install git+https://gitlab.com/nobodyinperson/termkeymonitor.git
```

# ❓ Usage

```bash
# use any of the below commands to invoke
termkeymonitor
python -m termkeymonitor
python3 -m termkeymonitor
```

## 🎥 Screencast

[![asciicast](https://asciinema.org/a/544131.svg)](https://asciinema.org/a/544131)

## ⚠️ Caveats

- no Windows and MacOS support (Apparently `evdev` only works on Linux... 😔, might need to use some other backend like [`pynput`](https://pypi.org/project/pynput/) in the future)
- needs a local keyboard connected so doesn't work as expected on remote machines (e.g. via SSH)
- Make sure you have permissions to access the `/dev/input/event*` files (this normally means you need to add yourself to the `input` group)
