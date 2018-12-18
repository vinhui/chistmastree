import logging
import os
from random import randint

from color import Color


class Sequence:
    def __init__(self):
        self.name = ""
        self.data = []

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.name == other.name

    def __str__(self):
        return self.name

    @staticmethod
    def parsefile(path: str):
        print("Parsing sequence file {}".format(path))
        file = open(path)
        name = os.path.basename(os.path.splitext(path)[0])

        seq = Sequence.parsestring(file.read(), name, False)

        file.close()
        return seq

    @staticmethod
    def parsestring(string: str, name: str = None, logtext: bool = True):
        if logtext:
            print("Parsing sequence string")

        seq = Sequence()
        if name is None:
            seq.name = "String sequence " + str(randint(10000, 99999))
        else:
            seq.name = name

        for i, line in enumerate(iter(string.splitlines())):
            line = line.strip()

            if line == "" or line.startswith("#") or line.startswith(";"):
                continue

            data = SequenceData.parseline(line)
            if data is not None:
                seq.data.append(data)
            else:
                logging.error("Failed to parse line %s (%s)", i, line)

        return seq


class SequenceData:
    def __init__(self, startID, endID, color, delay):
        self.startid = startID
        self.endid = endID
        self.color = color
        self.delay = int(delay)

    def __str__(self):
        return "{},{},{},{}".format(self.startid, self.endid, str(self.color), self.delay)

    @staticmethod
    def parseline(line: str):
        items = line.split(",")
        if len(items) == 6:
            return SequenceData(
                int(items[0]),
                int(items[1]),
                Color(int(items[2]), int(items[3]), int(items[4])),
                int(items[5]))
        else:
            return None
