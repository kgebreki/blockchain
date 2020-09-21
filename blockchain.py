from blockchain_util import sha256, hash_block, get_transaction_details, get_user_choice
from collections import OrderedDict

MINING_REWARD = 10
gen_block = {"prev_hash": "", "index": 0, "transactions": [], "proof_of_work": 0}
blockchain = [gen_block]
outstanding_transactions = []
owner = "Kaleb"
participants = {owner}


def get_last_block():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recepient, sender=owner, amount=1.0):
    transaction = OrderedDict(
        [("sender", sender), ("recepient", recepient), ("amount", amount)]
    )

    if verify_transaction(transaction):
        outstanding_transactions.append(transaction)
        participants.add(sender)
        participants.add(recepient)
        return True
    else:
        return False


def valid_proof_of_work(prev_hash, outstanding_transactions, proof_of_work):
    guess = (
        str(prev_hash) + str(outstanding_transactions) + str(proof_of_work)
    ).encode()
    return sha256(guess)[0:2] == "00"


def get_proof_of_work():
    proof_of_work = 0

    while not valid_proof_of_work(
        hash_block(get_last_block()), outstanding_transactions, proof_of_work
    ):
        proof_of_work += 1
    return proof_of_work


def verify_transaction(transaction):
    if transaction["sender"] == transaction["recepient"]:
        return False
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def mine_block():
    global outstanding_transactions
    proof_of_work = get_proof_of_work()

    mining_reward_transaction = OrderedDict(
        [("sender", None), ("recepient", owner), ("amount", MINING_REWARD)]
    )
    outstanding_transactions.append(mining_reward_transaction)

    new_block = {
        "prev_hash": hash_block(get_last_block()),
        "index": int(get_last_block()["index"]) + 1,
        "transactions": outstanding_transactions,
        "proof_of_work": proof_of_work,
    }
    outstanding_transactions = []
    blockchain.append(new_block)


def verify_blockchain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["prev_hash"] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof_of_work(
            block["prev_hash"], block["transactions"][:-1], block["proof_of_work"]
        ):
            print("Proof of work not valid!")
            return False
    return True


def get_balance(participant):
    amount_sent = 0.0
    amount_received = 0.0

    for block in blockchain:
        for transaction in block["transactions"]:
            if transaction["sender"] == participant:
                amount_sent += transaction["amount"]
            elif transaction["recepient"] == participant:
                amount_received += transaction["amount"]

    for transaction in outstanding_transactions:
        if transaction["sender"] == participant:
            amount_sent += transaction["amount"]
    return float(amount_received - amount_sent)


def print_participant_balance():
    for participant in participants:
        print("{}  {:6.2f}".format(participant, get_balance(participant)))


while True:
    print("Hello, please choose: ")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Print blockchain")
    print("4: Get balance for participants")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == "1":
        tx_details = get_transaction_details()
        recepient, amount = tx_details
        if add_transaction(recepient, amount=amount):
            print("Transaction Successful!")
        else:
            print("Transaction Failed!")
    elif user_choice == "2":
        mine_block()
        if not verify_blockchain():
            print("Invalid blockchain!")
            break
    elif user_choice == "3":
        print(blockchain)
    elif user_choice == "4":
        print_participant_balance()
    elif user_choice == "q":
        break
