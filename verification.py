from blockchain_util import hash_block, sha256


class Verification:
    def valid_proof_of_work(self, prev_hash, outstanding_transactions, proof_of_work):
        guess = (
            str(prev_hash)
            + str([tx.to_ordered_dict for tx in outstanding_transactions])
            + str(proof_of_work)
        ).encode()
        return sha256(guess)[0:2] == "00"

    def verify_blockchain(self, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.prev_hash != hash_block(blockchain[index - 1]):
                print(
                    "Blockchain may have split. There is a block that is out of order"
                )
                return False
            if not self.valid_proof_of_work(
                block.prev_hash, block.transactions[:-1], block.proof_of_work
            ):
                print("Proof of work not valid!")
                return False
        return True

    def verify_transaction(self, transaction, get_balance):
        if transaction.sender == transaction.recepient:
            return False
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount