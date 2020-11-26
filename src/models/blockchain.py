import json

from util.hash_util import hash_block
from models.block import Block
from models.transaction import Transaction
from util.verification import Verification

MINING_REWARD = 10
MINING_SENDER = "MINING"

"""
    Participant pool (which is currently a dict where key is name of participant and value is always true) to keep track 
    of how much money each person has at a given time -- might go away later
"""
participants = dict()


class Blockchain:
    def __init__(self, hosting_node_id):
        gen_block = Block("", 0, [], 0, 0)
        self.__node = hosting_node_id
        self.__chain = [gen_block]
        self.__outstanding_transactions = []
        self.load_data()

    def get_last_block(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def get_blockchain(self):
        return self.__chain

    def get_outstanding_transactions(self):
        return self.__outstanding_transactions

    def add_transaction(self, sender, recepient, amount, signature):
        global participants
        transaction = Transaction(sender, recepient, amount, signature)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__outstanding_transactions.append(transaction)
            participants[sender] = True
            participants[recepient] = True
            self.save_data()
            return True
        return False

    def get_proof_of_work(self):
        proof_of_work = 0

        while not Verification.valid_proof_of_work(
            hash_block(self.get_last_block()),
            self.__outstanding_transactions,
            proof_of_work,
        ):
            proof_of_work += 1
        return proof_of_work

    def mine_block(self):
        proof_of_work = self.get_proof_of_work()
        mining_reward_transaction = Transaction(
            MINING_SENDER, self.__node, MINING_REWARD, None
        )
        self.__outstanding_transactions.append(mining_reward_transaction)

        new_block = Block(
            hash_block(self.get_last_block()),
            int(self.get_last_block().index) + 1,
            self.__outstanding_transactions,
            proof_of_work,
        )
        self.__chain.append(new_block)

        # Check to see if any outstanding transactions have been tampered with after being saved
        for txn in self.__outstanding_transactions:
            if not Verification.verify_transaction(txn, self.get_balance):
                return False

        if Verification.verify_blockchain(self.__chain):
            global participants
            self.__outstanding_transactions = []
            participants[self.__node] = True
            self.save_data()
            return True

        self.__chain.pop()
        self.__outstanding_transactions.pop()
        return False

    def get_balance(self, participant):
        amount_sent = 0.0
        amount_received = 0.0

        for block in self.__chain:
            for transaction in block.transactions:
                if transaction.sender == participant:
                    amount_sent += transaction.amount
                elif transaction.recepient == participant:
                    amount_received += transaction.amount

        for transaction in self.__outstanding_transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount
        return float(amount_received - amount_sent)

    def print_participant_balance(self):
        global participants
        if len(participants) < 1:
            print("------Empty participants pool------")
        else:
            for participant in participants:
                print("{}  {:6.2f}".format(participant, self.get_balance(participant)))

    def save_data(self):
        try:
            with open("../target/blockchain.txt", mode="w") as file:
                reconstructed_blockchain = [
                    block.__dict__
                    for block in [
                        Block(
                            block_el.prev_hash,
                            block_el.index,
                            [tx.__dict__ for tx in block_el.transactions],
                            block_el.proof_of_work,
                            block_el.timestamp,
                        )
                        for block_el in self.__chain
                    ]
                ]
                file.write(json.dumps(reconstructed_blockchain))
                file.write("\n")
                reconstructed_outstanding_transactions = [
                    txn.__dict__ for txn in self.__outstanding_transactions
                ]
                file.write(json.dumps(reconstructed_outstanding_transactions))
                file.write("\n")
                global participants
                file.write(json.dumps(participants))
        except IOError:
            ("------Saving failed------")

    def load_data(self):
        try:
            with open("../target/blockchain.txt", mode="r") as file:
                print("------Loading existing blockchain------")
                file_content = file.readlines()
                blockchain = json.loads(file_content[0][:-1])
                outstanding_transactions = json.loads(file_content[1][:-1])
                updated_blockchain = []
                updated_outstanding_transactions = []

                for block in blockchain:
                    updated_block = Block(
                        block["prev_hash"],
                        block["index"],
                        [
                            Transaction(
                                tx["sender"],
                                tx["recepient"],
                                tx["amount"],
                                tx["signature"],
                                tx["timestamp"],
                            )
                            for tx in block["transactions"]
                        ],
                        block["proof_of_work"],
                        block["timestamp"],
                    )
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain

                for txn in outstanding_transactions:
                    updated_txn = Transaction(
                        txn["sender"],
                        txn["recepient"],
                        txn["amount"],
                        txn["signature"],
                        txn["timestamp"],
                    )
                    updated_outstanding_transactions.append(updated_txn)
                self.__outstanding_transactions = updated_outstanding_transactions
                global participants
                participants = json.loads(file_content[2])
        except (IOError, IndexError):
            print("------Initializing new blockchain with genesis block------")