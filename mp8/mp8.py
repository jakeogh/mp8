#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=useless-suppression             # [I0021]
# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-param-doc               # [W9015]
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

# code style:
#   avoid guessing on spelling, just write the word out
#   dont_makedirs -> no_makedirs
#   no guessing on case: local vars, functions and methods are lower case. classes are ThisClass(). Globals are THIS.
#   del vars explicitely ASAP, assumptions are buggy
#   rely on the compiler, code verbosity and explicitness can only be overruled by benchamrks (are really compiler bugs)
#   no tabs. code must display the same independent of viewer
#   no recursion, recursion is undecidiable, randomly bounded, and hard to reason about
#   each elementis the same, no special cases for the first or last elemetnt:
#       [1, 2, 3,] not [1, 2, 3]
#       def this(*.
#                a: bool,
#                b: bool,
#               ):
#
#   expicit loop control is better than while (condition):
#       while True:
#           # continue/break explicit logic
#   only computer generated commit messages _should_ start with a cap letter


# TODO:
#   https://github.com/kvesteri/validators
import os
import sys
import click
import time
import sh
from clicktool import click_add_options, click_global_options
from click_auto_help import AHGroup
from signal import signal, SIGPIPE, SIG_DFL
from pathlib import Path
#from with_sshfs import sshfs
#from with_chdir import chdir
from mptool import output
from clicktool import tv
from asserttool import validate_slice
from eprint import eprint
from asserttool import ic
from retry_on_exception import retry_on_exception
#from collections import defaultdict
#from prettyprinter import cpprint
#from prettyprinter import install_extras
#install_extras(['attrs'])
from timetool import get_timestamp
#from configtool import click_read_config
#from configtool import click_write_config_entry

#from asserttool import not_root
#from pathtool import path_is_block_special
#from pathtool import write_line_to_file
#from getdents import files
#from prettytable import PrettyTable
#output_table = PrettyTable()

from mptool import unmp
##from typing import Tuple
from collections.abc import Sequence
#from typing import Generator
from typing import Iterable
#from typing import ByteString

sh.mv = None  # use sh.busybox('mv'), coreutils ignores stdin read errors

# click-command-tree
#from click_plugins import with_plugins
#from pkg_resources import iter_entry_points

# import pdb; pdb.set_trace()
# #set_trace(term_size=(80, 24))
# from pudb import set_trace; set_trace(paused=False)

##def log_uncaught_exceptions(ex_cls, ex, tb):
##   eprint(''.join(traceback.format_tb(tb)))
##   eprint('{0}: {1}'.format(ex_cls, ex))
##
##sys.excepthook = log_uncaught_exceptions

#this should be earlier in the imports, but isort stops working
signal(SIGPIPE, SIG_DFL)


#@with_plugins(iter_entry_points('click_command_tree'))
#@click.group(no_args_is_help=True, cls=AHGroup)
#@click_add_options(click_global_options)
#@click.pass_context
#def cli(ctx,
#        verbose: bool | int | float,
#        verbose_inf: bool,
#        dict_input: bool,
#        ) -> None:
#
#    tty, verbose = tv(ctx=ctx,
#                      verbose=verbose,
#                      verbose_inf=verbose_inf,
#                      )


# update setup.py if changing function name
#@click.argument("slice_syntax", type=validate_slice, nargs=1)
@click.command()
@click.argument("paths", type=str, nargs=-1)
@click.argument("sysskel",
                type=click.Path(exists=False,
                                dir_okay=True,
                                file_okay=False,
                                allow_dash=False,
                                path_type=Path,),
                nargs=1,
                required=True,)
@click.option('--ipython', is_flag=True)
@click_add_options(click_global_options)
@click.pass_context
def cli(ctx,
        paths: Sequence[str],
        sysskel: Path,
        ipython: bool,
        verbose: bool | int | float,
        verbose_inf: bool,
        dict_input: bool,
        ) -> None:

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )

    if paths:
        iterator = paths
    else:
        iterator = unmp(valid_types=[bytes,], verbose=verbose)
    del paths

    index = 0
    for index, _path in enumerate(iterator):
        path = Path(os.fsdecode(_path)).resolve()
        if verbose:
            ic(index, path)

        with open(path, 'rb') as fh:
            path_bytes_data = fh.read()

        output(path, reason=None, dict_input=dict_input, tty=tty, verbose=verbose)

#        if ipython:
#            import IPython; IPython.embed()

if __name__ == '__main__':
    # pylint: disable=E1120
    cli()

#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
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
        print("Usage: mpp [PATH]...", file=sys.stderr)
        sys.exit(1)

    tty = sys.stdout.isatty()
    # https://docs.python.org/3/library/os.html#python-utf-8-mode
    # https://vstinner.github.io/pep-383.html
    # https://github.com/python/cpython/blob/3.10/Lib/os.py#L804
    # def fsencode():
    #  filename.encode(encoding, errors)
    #  filename.encode('utf8', 'surrogateescape')

    # argvb = list(map(os.fsencode, sys.argv[1:]))
    argvb = map(os.fsencode, sys.argv[1:])
    found_arg = False
    for arg in argvb:
        if len(arg) == 0:
            continue
        found_arg = True
        if tty:
            sys.stdout.write(repr(arg) + "\n")
            continue
        sys.stdout.buffer.write(msgpack.packb(arg))
    return not found_arg
