from flask import Flask, jsonify
from flask_cors import CORS

from models.wallet import Wallet
from models.blockchain import Blockchain


status_codes = {
    "SUCCESS": 200,
    "CREATED": 201,
    "CLIENT_ERROR": 400,
    "SERVER_ERROR": 500,
}


server = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(server)
host = "0.0.0.0"
port = 8000


@server.route("/", methods=["GET"])
def get_ui():
    return "Blockchain server!"


# TODO: get error objects so that clients have clear error messages
@server.route("/mine", methods=["POST"])
def mine_block():
    if blockchain.mine_block():
        block = blockchain.get_last_block()
        new_block = block.__dict__.copy()
        new_block["transactions"] = [tx.__dict__ for tx in new_block["transactions"]]
        return jsonify(new_block), status_codes["CREATED"]
    else:
        response = {"Message": "Mining unsuccessful."}
        return jsonify(response), status_codes["SERVER_ERROR"]


@server.route("/chain", methods=["GET"])
def get_blockchain():
    snapshot = blockchain.get_blockchain()
    snapshot_dict = [block.__dict__.copy() for block in snapshot]
    for block in snapshot_dict:
        block["transactions"] = [tx.__dict__ for tx in block["transactions"]]
    return jsonify(snapshot_dict), status_codes["SUCCESS"]


if __name__ == "__main__":
    server.run(host=host, port=port)