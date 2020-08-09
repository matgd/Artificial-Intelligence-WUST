from dataclasses import dataclass


@dataclass
class Node:
    index: int
    x: float
    y: float

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        """ Needed when sorting tuple score, node """
        return self.index < other.index
