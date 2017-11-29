class Color:
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
        self.white = 0

    def __str__(self):
        return "{},{},{}".format(self.r, self.g, self.b)

    def topixel(self):
        return (self.white << 24) | (self.r << 16)| (self.g << 8) | self.b

    def tohex(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    @staticmethod
    def white():
        return Color(255, 255, 255)

    @staticmethod
    def black():
        return Color(0, 0, 0)
