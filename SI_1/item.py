from dataclasses import dataclass


@dataclass
class Item:
    index: int
    profit: int
    weight: int
    assigned_node_number: int

    def __gt__(self, other):
        return self.profit > other.profit
