# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0703,W0201,R0902,R0903,W0613,R0201


"list of listeners"


from cmdz.object import Object


class Bus(Object):

    objs = []

    @staticmethod
    def add(obj):
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for obj in Bus.objs:
            obj.announce(txt)

    @staticmethod
    def byorig(orig):
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig, channel, txt):
        bot = Bus.byorig(orig)
        if bot:
            bot.say(channel, txt)
