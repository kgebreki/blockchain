class Node:
    def __init__(self):
        self.blockchain = []

    def get_transaction_details(self):
        recepient = input("Please enter recepient: ")
        amount = float(input("Enter transaction amount: "))
        return recepient, amount

    def get_user_choice(self):
        return input("Your choice: ")

    def print_participant_balance(self, participants, get_balance):
        for participant in participants:
            print("{}  {:6.2f}".format(participant, get_balance(participant)))

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
                if add_transaction(recepient, amount=amount):
                    print("Transaction successful!")
                else:
                    print("Transaction failed due to insufficient funds!")
            elif user_choice == "2":
                if not mine_block():
                    print("Mining failed!")
                    break
                print("Mining successful!")
            # elif user_choice == "3":
            #     self.print_participant_balance()
            elif user_choice == "4":
                print(self.blockchain)
            elif user_choice == "q":
                break