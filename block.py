from time import time


class Block:
    def __init__(self, prev_hash, index, transactions, proof_of_work, timestamp=time()):
        self.prev_hash = prev_hash
        self.index = index
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.timestamp = timestamp