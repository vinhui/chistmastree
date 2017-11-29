import os
import logging
from threading import Thread
from time import sleep
from random import randint
from color import Color
import config as cfg
if cfg.NO_PI:
    import tkinter
else:
    from neopixel import Adafruit_NeoPixel

class SequenceManager:
    def __init__(self):
        self.currentsequence = None
        self.sequencethread = None

        if cfg.NO_PI:
            self.closegui = False
            self.guiupdatebuffer = []

            self.guithread = Thread(target=self.createwindow)
            self.guithread.start()
        else:
            self.strip = Adafruit_NeoPixel(
                cfg.LED_COUNT,
                cfg.LED_DATA_PIN,
                cfg.LED_FREQ_HZ,
                cfg.LED_DMA,
                cfg.LED_INVERT,
                cfg.LED_BRIGHTNESS,
                cfg.LED_CHANNEL,
                cfg.LED_STRIP)
            self.strip.begin()

    def createwindow(self):
        itemsize = 30       # in pixels
        refreshrate = 10    # in ms

        windowcanvasleds = [None] * cfg.LED_COUNT

        window = tkinter.Tk()
        window.title("Christmas Tree DEBUG")
        windowcanvas = tkinter.Canvas(
            window,
            bd=0,
            highlightthickness=0,
            relief=tkinter.RIDGE,
            bg="black",
            width=cfg.LED_COUNT * itemsize,
            height=itemsize)

        for i in range(cfg.LED_COUNT):
            windowcanvasleds[i] = windowcanvas.create_rectangle(
                i * itemsize,       # X min
                0,                  # Y min
                (i + 1) * itemsize, # X max
                itemsize,           # Y max
                fill="black",
                outline="black")

        windowcanvas.pack()

        while not self.closegui:
            for item in self.guiupdatebuffer:
                windowcanvas.itemconfig(
                    windowcanvasleds[item['led']],
                    fill=item['color'].tohex())

            del self.guiupdatebuffer[:]

            window.update_idletasks()
            window.update()
            sleep(refreshrate / 1000)

        window.destroy()

    def stop(self):
        self.stopcurrentsequence()
        sleep(2)
        self.clear()
        if cfg.NO_PI:
            self.closegui = True

    def runsequence(self, sequence):
        if self.currentsequence == sequence:
            return

        print("Running sequence {}".format(sequence.name))
        self.currentsequence = sequence
        self.sequencethread = Thread(target=self.runthread)
        self.sequencethread.start()

    def stopcurrentsequence(self):
        self.currentsequence = None
        self.sequencethread = None

    def runthread(self):
        seq = self.currentsequence
        loop = True
        while loop:
            for x in seq.data:
                if seq != self.currentsequence:
                    loop = False
                    break

                self.setrangecolor(x.startid, x.endid, x.color, x.delay > 2)
                if x.delay > 2:
                    sleep(max(x.delay, 10)/1000)

        if seq == self.currentsequence:
            self.sequencethread = None

    def clear(self):
        self.setrangecolor(0, cfg.LED_COUNT, Color.black())

    def setrangecolor(self, start, end, color, write=True):
        if start == end:
            self.setcolor(start, color, False)
        else:
            for i in range(min(start, end), min(max(start, end), cfg.LED_COUNT)):
                self.setcolor(i, color, False)
        if write and not cfg.NO_PI:
            self.strip.show()

    def setcolor(self, led, color, write=True):
        if cfg.NO_PI and not self.closegui:
            self.guiupdatebuffer.append({'led': led, 'color': color})
        else:
            self.strip.setPixelColor(led, color.topixel())
            if write:
                self.strip.show()

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
    def parsefile(path):
        print("Parsing sequence file {}".format(path))
        file = open(path)
        seq = Sequence()
        seq.name = os.path.basename(os.path.splitext(path)[0])

        for i, line in enumerate(iter(file.readline, '')):
            line = line.strip()

            if line == "" or line.startswith("#") or line.startswith(";"):
                continue

            data = SequenceData.parseline(line)
            if data != None:
                seq.data.append(data)
            else:
                logging.error("Failed to parse line %s in file \\'%s\\'", i, path)

        return seq

    @staticmethod
    def parsestring(string):
        print("Parsing sequence string")
        seq = Sequence()
        seq.name = "String sequence " + str(randint(10000, 99999))

        for i, line in enumerate(iter(string.splitlines())):
            line = line.strip()

            if line == "" or line.startswith("#") or line.startswith(";"):
                continue

            data = SequenceData.parseline(line)
            if data != None:
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
    def parseline(line):
        items = line.split(",")
        if len(items) == 6:
            return SequenceData(
                int(items[0]),
                int(items[1]),
                Color(int(items[2]), int(items[3]), int(items[4])),
                int(items[5]))
        else:
            return None
