blockchain = []


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(last_transaction, transaction_amount):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])
    

def get_transaction_amount():
    return float(input('Enter transaction amount: '))


def get_user_choice():
    return input('Your choice: ')


def print_blockchain_elements():
    for block in blockchain:
        print('Outputting Block')
        print(block)


def is_blockchain_empty():
    return len(blockchain) < 1


while(True):
    print('Hello, please choose: ')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('q: Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_amount = get_transaction_amount()
        add_transaction(get_last_blockchain_value(), tx_amount)
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'q':
        break

print(blockchain)
print('Have a good day')