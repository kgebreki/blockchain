from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.id =  self.wallet.public_key
        self.blockchain = Blockchain(self.id)

    def get_transaction_details(self):
        recepient = input("Please enter recepient: ")
        amount = float(input("Enter transaction amount: "))
        return recepient, amount

    def get_user_choice(self):
        return input("Your choice: ")

    def listen_for_input(self):
        while True:
            print("Hello, please choose: ")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Get balance for participants")
            print("4: Print blockchain")
            print("q: Quit")
            user_choice = self.get_user_choice()

            if user_choice == "1":
                tx_details = self.get_transaction_details()
                recepient, amount = tx_details
                signature = self.wallet.sign_transaction(self.id, recepient, amount)
                if self.blockchain.add_transaction(self.id, recepient, amount, signature):
                    print("------Transaction successful------")
                else:
                    print("------Transaction failed ------")
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("------Mining failed------")
                    break
                print("------Mining successful------")
            elif user_choice == "3":
                self.blockchain.print_participant_balance()
            elif user_choice == "4":
                print(self.blockchain)
            elif user_choice == "q":
                break


Node().listen_for_input()