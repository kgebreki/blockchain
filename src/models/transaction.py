from time import time
from collections import OrderedDict


class Transaction:
    def __init__(self, sender, recepient, amount, signature, timestamp=time()):
        self.sender = sender
        self.recepient = recepient
        self.amount = amount
        self.signature = signature
        self.timestamp = timestamp

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict(
            [
                ("sender", self.sender),
                ("recepient", self.recepient),
                ("amount", self.amount),
                ("signature", self.signature),
                ("timestamp", self.timestamp),
            ]
        )
