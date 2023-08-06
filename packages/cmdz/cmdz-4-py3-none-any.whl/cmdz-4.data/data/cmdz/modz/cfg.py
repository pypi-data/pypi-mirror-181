# This file is placed in the Public Domain


from cmdz import Cfg, last, printable, keys, edit, write


def cfg(event):
    last(Cfg)
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()
