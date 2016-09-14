# stdlib imports
import json
import logging
import time

from mopidy.core import CoreListener

import pykka
from lol import log_dict
from threading import Timer


from listener import CommandListener


logger = logging.getLogger(__name__)

class NextListener(CommandListener):

    def __init__(self,core,counter):
        self.core = core
        self.counter = counter

    def command(self):
        return '/next'

    def action(self, msg):
        if len(self.counter.nexts) == 0:
            Timer(15.0,self.change_song).start()
            self.counter.add_next(msg['mucnick'])
            return 'In 10 seconds song will be next'

        self.counter.add_next(msg['mucnick'])
        return 'Currently {} nexts and {} keeps'.format(len(self.counter.nexts),len(self.counter.keeps))

    def change_song(self):
        if len(self.counter.nexts) > len(self.counter.keeps):
            self.core.playback.next()

class NextCounter():

    def __init__(self):
        self.reset()

    def add_next(self,user):
        self.nexts.add(user)

    def add_keep(self,user):
        self.keeps.add(user)

    def reset(self):
        self.nexts = set()
        self.keeps = set()
