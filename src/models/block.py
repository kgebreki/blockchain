from time import time


class Block:
    def __init__(self, prev_hash, index, transactions, proof_of_work, timestamp=time()):
        self.prev_hash = prev_hash
        self.index = index
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.timestamp = timestamp

    def __repr__(self):
        return "prev_hash: {}, index: {}, transactions: {}, proof_of_work: {}, timestamp: {}".format(
            self.prev_hash,
            self.index,
            self.transactions,
            self.proof_of_work,
            self.timestamp,
        )
