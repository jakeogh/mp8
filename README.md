**mp8**: (**m**)essage(**p**)ack utf(**8**)


#### Description:
```
writing each arg to stdout:
    messagepack(arg) IF sys.stdout.isatty(); ELSE repr(arg):

You are using a terminal.

IF stdout is not a terminal:
    convert each arg passed to mpp:
        from: the terminal input encoding
        to:   messagepack(arg)
ELSE:
    convert each arg passed to mpp:
        from: the terminal input encoding
        to:   repr(arg)

Messagepack will preserve it's type for other applications that assume messagepacked stdin;

In most setups, this means you enter unicode and write it's UTF-8 byte
representation (messagepacked) to the pipe, or it's unicode repr() back to the terminal.
```

#### pyPsudocode:
```
stdin: not read from, explicitely closed on startup
env (`man 1p export`): not explicitly used
args: N <= `getconf ARG_MAX`
stdout:
    for arg in args:
        if tty:
            print(repr(arg))
        else:
            print(messagepack(arg))
```
#### Examples:
```
$ mp8

$ # if stdout is a tty (aka terminal):
$ mp8 'a'
'a'

$ # if stdout is not a tty:
$ mp8 'a' | od -tx1 -v
0000000 a1 61
0000002

$ # where a1 61 is:
$ #  a1: fixstr https://github.com/msgpack/msgpack/blob/master/spec.md#str-format-family
$ #  61: a

$ # compared to:
$ echo -n 'a' | od -tx1 -v
0000000 61
0000001

```
