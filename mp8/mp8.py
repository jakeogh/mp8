#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import msgpack

signal(SIGPIPE, SIG_DFL)
sys.stdin.close()


# since this is py3.8+, sys.argv: list[str]
def main():
    if len(sys.argv) < 2:
        print("Usage: mp8 [str]...", file=sys.stderr)
        sys.exit(1)

    tty = sys.stdout.isatty()
    found_arg = False
    for arg in sys.argv[1:]:
        if len(arg) == 0:
            continue
        found_arg = True
        if tty:
            sys.stdout.write(repr(arg) + "\n")
            continue
        sys.stdout.buffer.write(msgpack.packb(arg))
    return not found_arg
