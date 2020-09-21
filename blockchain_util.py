import hashlib, json


def get_transaction_details():
    recepient = input("Please enter recepient: ")
    amount = float(input("Enter transaction amount: "))
    return recepient, amount


def get_user_choice():
    return input("Your choice: ")


def sha256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    return sha256(json.dumps(block, sort_keys=True).encode())