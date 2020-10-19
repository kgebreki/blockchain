from blockchain_util import hash_block, get_transaction_details, get_user_choice
import json
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10
blockchain = []
outstanding_transactions = []
owner = "Kaleb"
participants = {owner}


def get_last_block():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recepient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recepient, amount)
    print(transaction.timestamp)

    if Verification().verify_transaction(transaction, get_balance):
        outstanding_transactions.append(transaction)
        participants.add(sender)
        participants.add(recepient)
        save_data()
        return True
    return False


def get_proof_of_work():
    proof_of_work = 0

    while not Verification().valid_proof_of_work(
        hash_block(get_last_block()), outstanding_transactions, proof_of_work
    ):
        proof_of_work += 1
    return proof_of_work


def mine_block():
    global outstanding_transactions
    proof_of_work = get_proof_of_work()

    mining_reward_transaction = Transaction(None, owner, MINING_REWARD)
    print(mining_reward_transaction.timestamp)
    outstanding_transactions.append(mining_reward_transaction)

    new_block = Block(
        hash_block(get_last_block()),
        int(get_last_block().index) + 1,
        outstanding_transactions,
        proof_of_work,
    )

    if Verification().verify_blockchain(blockchain):
        blockchain.append(new_block)
        outstanding_transactions = []
        save_data()
        return True

    # Mining unsuccessful so don't add minging reward
    outstanding_transactions.pop()
    return False


def get_balance(participant):
    amount_sent = 0.0
    amount_received = 0.0

    for block in blockchain:
        for transaction in block.transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount
            elif transaction.recepient == participant:
                amount_received += transaction.amount

    for transaction in outstanding_transactions:
        if transaction.sender == participant:
            amount_sent += transaction.amount
    return float(amount_received - amount_sent)


def save_data():
    try:
        with open("blockchain.txt", mode="w") as file:
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
                    for block_el in blockchain
                ]
            ]
            file.write(json.dumps(reconstructed_blockchain))
            file.write("\n")
            reconstructed_outstanding_transactions = [
                txn.__dict__ for txn in outstanding_transactions
            ]
            file.write(json.dumps(reconstructed_outstanding_transactions))
            # file.write("\n")
            # file.write(json.dumps(participants))
    except IOError:
        ("Saving failed!")


def load_data():
    global blockchain, outstanding_transactions  # , participants
    try:
        with open("blockchain.txt", mode="r") as file:
            file_content = file.readlines()
            blockchain = json.loads(file_content[0][:-1])
            outstanding_transactions = json.loads(file_content[1])
            updated_blockchain = []
            updated_outstanding_transactions = []

            # Necessary reconstruction due to the fact that json bytestream doesn't store OrderedDict
            for block in blockchain:
                updated_block = Block(
                    block["prev_hash"],
                    block["index"],
                    [
                        Transaction(
                            tx["sender"], tx["recepient"], tx["amount"], tx["timestamp"]
                        )
                        for tx in block["transactions"]
                    ],
                    block["proof_of_work"],
                    block["timestamp"],
                )
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            for txn in outstanding_transactions:
                updated_txn = Transaction(
                    txn["sender"], txn["recepient"], txn["amount"], txn["timestamp"]
                )
                updated_outstanding_transactions.append(updated_txn)
            outstanding_transactions = updated_outstanding_transactions
            # participants = json.loads(file_content[2])
    except (IOError, IndexError):
        gen_block = Block("", 0, [], 0, 0)
        blockchain.append(gen_block)
        outstanding_transactions = []


load_data()