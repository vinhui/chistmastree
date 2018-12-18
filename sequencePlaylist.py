from sequence import Sequence


class SequencePlaylist:
    def __init__(self, sequences: [], name: str):
        self.name = name
        self.sequences = sequences
        self.currentindex = -1

    def getnext(self) -> Sequence:
        self.currentindex = (self.currentindex + 1) % len(self.sequences)
        return self.sequences[self.currentindex]

    def peeknext(self) -> Sequence:
        return self.sequences[self.currentindex + 1]
