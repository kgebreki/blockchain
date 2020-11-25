from flask import Flask, jsonify
from flask_cors import CORS

from models.wallet import Wallet
from models.blockchain import Blockchain


status_codes = {"SUCCESS": 200, "FAILED": 400}


server = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(server)
host = "0.0.0.0"
port = 8000


@server.route("/", methods=["GET"])
def get_ui():
    return "This works!"


@server.route("/chain", methods=["GET"])
def get_blockchain():
    snapshot = blockchain.get_blockchain()
    snapshot_dict = [block.__dict__.copy() for block in snapshot]
    snapshot_dict = [
        tx.__dict__ for tx in block["transactions"] for block in snapshot_dict
    ]
    return jsonify(snapshot), status_codes["SUCCESS"]


if __name__ == "__main__":
    server.run(host=host, port=port)