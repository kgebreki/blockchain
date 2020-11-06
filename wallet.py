from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
import Cryptodome.Random
import binascii


class Wallet:
    def __init__(self):
        private_key, public_key = self.generate_key_pair()
        self.private_key = private_key
        self.public_key = public_key
        self.save_keys()

    def save_keys(self):
        try:
            with open("wallet.txt", mode="w") as f:
                f.write(self.private_key)
                f.write("\n")
                f.write(self.public_key)
        except (IOError, IndexError):
            print("Saving wallet failed!")
            

    def load_keys(self):
        try:
            with open("wallet.txt", mode="r") as f:
                keys = f.realines()
                self.private_key = keys[0][:-1]
                self.public_key = keys[1]
        except (IOError, IndexError):
            print("Loading wallet failed!")

    def generate_key_pair(self):
        private_key = RSA.generate(1024, Cryptodome.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.exportKey(format="DER")).decode("ascii"),
            binascii.hexlify(public_key.exportKey(format="DER")).decode("ascii"),
        )

    def sign_transaction(self, sender, recepient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        payload = SHA256.new((str(sender) + str(recepient) + str(amount)).encode("utf8"))
        signature = signer.sign(payload)
        return binascii.hexlify(signature).decode("ascii")
