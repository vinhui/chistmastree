from threading import Thread
from time import sleep

import config as cfg
from sequencePlaylist import SequencePlaylist
from color import Color
from sequence import Sequence


class SequencePlayer:
    def __init__(self):
        self.currentplaylist = None
        self.sequencethread = None

    def runsequence(self, sequence: Sequence):
        playlist = SequencePlaylist([sequence], sequence.name)
        self.runplaylist(playlist)

    def runplaylist(self, playlist: SequencePlaylist):
        if self.currentplaylist == playlist:
            return

        if cfg.VERBOSE_LOGGING:
            print("Running sequence {}".format(playlist.name))

        self.currentplaylist = playlist
        self.sequencethread = Thread(target=self.runthread)
        self.sequencethread.start()

    def stop(self):
        self.stopcurrentplaylist()
        sleep(2)
        self.clear()

    def runthread(self):
        playlist = self.currentplaylist
        loop = True
        while loop:
            sequence = playlist.getnext()

            if playlist != self.currentplaylist:
                break

            for x in sequence.data:
                if playlist != self.currentplaylist:
                    loop = False
                    break

                self.setrangecolor(x.startid, x.endid, x.color, x.delay > 2)
                if x.delay > 2:
                    sleep(max(x.delay, 10)/1000)

        if playlist == self.currentplaylist:
            self.sequencethread = None

    def stopcurrentplaylist(self):
        self.currentplaylist = None
        self.sequencethread = None
        print("Stopping running sequence")

    def clear(self):
        self.setrangecolor(0, cfg.LED_COUNT, Color.black())

    def setrangecolor(self, start, end, color, write=True):
        if start == end:
            self.setcolor(start, color, False)
        else:
            for i in range(min(start, end), min(max(start, end), cfg.LED_COUNT)):
                self.setcolor(i, color, False)

    def setcolor(self, led, color, write=True):
        pass
