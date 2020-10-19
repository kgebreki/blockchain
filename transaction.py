from time import time
from collections import OrderedDict


class Transaction:
    def __init__(self, sender, recepient, amount, timestamp=time()):
        self.sender = sender
        self.recepient = recepient
        self.amount = amount
        self.timestamp = timestamp

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict(
            [
                ("sender", self.sender),
                ("recepient", self.recepient),
                ("amount", self.amount),
                ("timestamp", self.timestamp),
            ]
        )
