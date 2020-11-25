from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256

import binascii

from util.hash_util import hash_block, sha256


class Verification:
    @staticmethod
    def valid_proof_of_work(prev_hash, outstanding_transactions, proof_of_work):
        guess = (
            str(prev_hash)
            + str([tx.to_ordered_dict() for tx in outstanding_transactions])
            + str(proof_of_work)
        ).encode()
        return sha256(guess)[0:2] == "00"

    @classmethod
    def verify_blockchain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.prev_hash != hash_block(blockchain[index - 1]):
                print(
                    "Blockchain may have split. There is a block that is out of order"
                )
                return False
            if not cls.valid_proof_of_work(
                block.prev_hash, block.transactions[:-1], block.proof_of_work
            ):
                print("Proof of work not valid!")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        if (transaction.sender) == "MINING":
            return True
        if transaction.sender == transaction.recepient:
            return False
        sender_balance = get_balance(transaction.sender)
        if sender_balance < transaction.amount:
            return False
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(
            (
                str(transaction.sender)
                + str(transaction.recepient)
                + str(transaction.amount)
            ).encode("utf8")
        )
        return verifier.verify(h, binascii.unhexlify(transaction.signature))