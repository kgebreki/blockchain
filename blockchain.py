gen_block = {"hash": "", "index": 0, "transactions": []}
blockchain = [gen_block]
outstanding_transactions = []
owner = "Kaleb"


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recepient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recepient": recepient, "amount": amount}
    outstanding_transactions.append(transaction)


def mine_block():
    last_block = get_last_blockchain_value()

    last_block_hash = ""
    for key in last_block:
        last_block_hash += str(last_block[key])

    new_block = {
        "hash": last_block_hash,
        "index": int(last_block["index"]) + 1,
        "transactions": outstanding_transactions,
    }

    blockchain.append(new_block)


def get_transaction_details():
    recepient = input("Please enter recepient: ")
    amount = float(input("Enter transaction amount: "))
    return (recepient, amount)


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
        add_transaction(recepient, amount=amount)
        print(outstanding_transactions)
    elif user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "q":
        break

print("Have a good day")
