import tkinter
from threading import Thread
from time import sleep

import config as cfg
from sequencePlayer import SequencePlayer


class SequencePlayerWindow(SequencePlayer):
    def __init__(self):
        super().__init__()

        self.guithread = Thread(target=self.createwindow)
        self.guiupdatebuffer = []
        self.closegui = False
        self.guithread.start()

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
        super().stop()
        self.closegui = True

    def setcolor(self, led, color, write=True):
        if not self.closegui:
            self.guiupdatebuffer.append({'led': led, 'color': color})
