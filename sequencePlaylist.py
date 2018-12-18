import os
from random import randint

import config as cfg
from sequence import Sequence


class SequencePlaylist:
    def __init__(self, sequences: [], name: str):
        self.name = name
        self.sequences = sequences
        self.currentindex = -1

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.name == other.name

    def __str__(self):
        return self.name

    def getnext(self) -> Sequence:
        self.currentindex = (self.currentindex + 1) % len(self.sequences)
        return self.sequences[self.currentindex]

    def peeknext(self) -> Sequence:
        return self.sequences[self.currentindex + 1]

    @staticmethod
    def parsefile(path: str):
        print("Parsing playlist file {}".format(path))
        file = open(path)
        name = os.path.basename(os.path.splitext(path)[0])

        playlist = SequencePlaylist.parsestring(file.read(), name, False)

        file.close()
        return playlist

    @staticmethod
    def parsestring(string: str, name: str = None, logtext: bool = True):
        if logtext:
            print("Parsing playlist string")

        if name is None:
            name = "String playlist " + str(randint(10000, 99999))

        sequences = []

        for line in string.splitlines():
            line = line.strip()

            if line == "" or line.startswith("#") or line.startswith(";"):
                continue

            path = os.path.join(cfg.SEQUENCE_DIR, line)
            sequences.append(Sequence.parsefile(path))

        if len(sequences) == 0:
            return None

        return SequencePlaylist(sequences, name)
