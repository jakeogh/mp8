#!/bin/sh

# if stdout is a tty (aka terminal):
#tty:
mp8 'a'

# if stdout is not a tty:
mp8 'a' | od -tx1 -v

# where a1 61 is:
#  a1: fixstr https://github.com/msgpack/msgpack/blob/master/spec.md#str-format-family
#  61: a
# <br>
# compared to:
echo -n 'a' | od -tx1 -v
