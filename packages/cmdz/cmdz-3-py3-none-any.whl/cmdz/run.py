# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413,W0212


"runtime"


import atexit
import importlib
import importlib.util
import os
import readline
import rlcompleter
import sys
import termios
import time
import traceback


from cmdz.event import Event, Parsed
from cmdz.handler import Handler, Command, scan
from cmdz.object import Default, update
from cmdz.thread import launch


def __dir__():
    return (
            "Cfg",
            "CLI",
            "Completer",
            "Console",
            "boot",
            "command",
            "daemon",
            "importer",
            "initer",
            "parse",
            "print_exc",
            "setcompleter",
            "Scandir",
            "wait",
            "wrap"
           )


Cfg = Default()


class CLI(Handler):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)
        sys.stdout.flush()


class Console(CLI):

    def handle(self, event):
        Command.handle(event)
        event.wait()

    def poll(self):
        event = Event()
        event.txt = input("> ")
        event.orig = repr(self)
        return event


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
        self.matches = []
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [
                                s for s in self.options
                                if s and s.startswith(text)
                               ]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None




def boot(txt):
    parse(txt)
    if "c" in Cfg.opts:
        Cfg.console = True
    if "d" in Cfg.opts:
        Cfg.daemon = True
    if "v" in Cfg.opts:
        Cfg.verbose = True
    if "w" in Cfg.opts:
        Cfg.wait = True
    if "x" in Cfg.opts:
        Cfg.exec = True


def command(cli, txt, event=None):
    evt = (event() if event else Event())
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    evt.wait()
    return evt


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open("/dev/null", 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    if not Cfg.verbose:
        sos = open("/dev/null", 'a+')
        ses = open("/dev/null", 'a+')
        os.dup2(sos.fileno(), sys.stdout.fileno())
        os.dup2(ses.fileno(), sys.stderr.fileno())


def importer(pname, mname, path=None):
    if not path:
        path = pname
    mod = None
    spec = importlib.util.spec_from_file_location(mname, path)
    if spec:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scan(mod)
    return mod


def initer(pname, mname, path=None):
    mod = importer(pname, mname, path)
    if "init" in dir(mod):
        launch(mod.init)
    return mod


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    if "c" in prs.opts:
        prs.console = True
    if "d" in prs.opts:
        prs.debug = True
    if "v" in prs.opts:
        prs.verbose = True
    if "x" in prs.opts:
        prs.exec = True
    if "w" in prs.opts:
        prs.wait = True
    update(Cfg, prs)
    return prs


def print_exc(ex):
    traceback.print_exception(type(ex), ex, ex.__traceback__)


def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        try:
            pname = fnm.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = fnm.split(os.sep)[-1][:-3]
        path2 = os.path.join(path, fnm)
        res.append(func(pname, mname, path2))
    return res


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def wait():
    while 1:
        time.sleep(1.0)


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    readline.redisplay()
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
        for evt in Command.errors:
            print_exc(evt.__exc__)
