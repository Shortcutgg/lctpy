# lctpy

Unofficial Learning Curve Tracker Client (Shortcut) for Linux

http://shortcut.gg

# Usage

Python 2/3 Compatible.
The application must be run as root in order to hook the Shortcut/keyboard.

```
> sudo python lctpy.py --help

Usage: lctpy.py [OPTIONS]

Options:
  --server TEXT       Address of the server (default lc.shortcut.gg)
  --port INTEGER      Port on the server (default 8001)
  --email TEXT        Your Shortcut community email address
  --device TEXT       The device to hook (default /dev/input/by-id/usb-
                      qmkbuilder_keyboard-event-kbd)
  --interval INTEGER  Interval in seconds between uploads (default 900)
  --help              Show this message and exit.

```

To run, specify your Shortcut community email:
```
sudo python lctpy.py --email my@email.com
```
