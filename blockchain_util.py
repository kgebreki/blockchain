import hashlib, json


def get_transaction_details():
    recepient = input("Please enter recepient: ")
    amount = float(input("Enter transaction amount: "))
    return recepient, amount


def print_object(blockchain):
    for block in blockchain:
        print("prev_hash: {}, index: {}, transactions: {}, proof_of_work: {}, timestamp: {}".format(block.prev_hash, block.index, block.transactions, block.proof_of_work, block.timestamp))


def get_user_choice():
    return input("Your choice: ")


def sha256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    return sha256(json.dumps(hashable_block, sort_keys=True).encode())