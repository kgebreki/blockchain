MINING_REWARD = 10
gen_block = {"hash": "", "index": 0, "transactions": []}
blockchain = [gen_block]
outstanding_transactions = []
owner = "Kaleb"
participants = {owner}


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recepient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recepient": recepient, "amount": amount}

    if verify_transaction(transaction):
        outstanding_transactions.append(transaction)
        participants.add(sender)
        participants.add(recepient)
        return True
    else:
        return False

def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    print(transaction["sender"], sender_balance)
    return sender_balance >= transaction["amount"]


def mine_block():
    global outstanding_transactions

    mining_reward_transaction = {"sender": None, "recepient": owner, "amount": MINING_REWARD}
    outstanding_transactions.append(mining_reward_transaction)

    last_block = get_last_blockchain_value()
    new_block = {
        "hash": hash_block(last_block),
        "index": int(last_block["index"]) + 1,
        "transactions": outstanding_transactions,
    }

    outstanding_transactions = []
    blockchain.append(new_block)


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def verify_blockchain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["hash"] != hash_block(blockchain[index - 1]):
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


def get_transaction_details():
    recepient = input("Please enter recepient: ")
    amount = float(input("Enter transaction amount: "))
    return recepient, amount


def get_user_choice():
    return input("Your choice: ")


def print_blockchain_elements():
    for block in blockchain:
        print("Outputting Block")
        print(block)


while True:
    print("Hello, please choose: ")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == "1":
        tx_details = get_transaction_details()
        recepient, amount = tx_details
        if add_transaction(recepient, amount=amount):
            print("Transaction Successful!")
        else:
            print("Transaction Failed! Insufficient funds.")
    elif user_choice == "2":
        mine_block()
        if not verify_blockchain():
            print("Invalid blockchain!")
            break
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "q":
        break


print(blockchain)