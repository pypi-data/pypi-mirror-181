# This file is placed in the Public Domain.
# pylint: disable=C0116,C0413,W0212,C0301,W0613


"shell"


import time


from cmdz import Cfg, Command, Console, printable, setcompleter


def shl(event):
    setcompleter(Command.cmd)
    date = time.ctime(time.time()).replace("  ", " ")
    print("CMDZ started at %s %s" % (date, printable(Cfg, "console,debug,verbose,wait", plain=True)))
    cli = Console()
    cli.start()
