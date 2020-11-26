from flask import Flask, jsonify, request
from flask_cors import CORS
from argparse import ArgumentParser

from models.wallet import Wallet
from models.blockchain import Blockchain


status_codes = {
    "SUCCESS": 200,
    "CREATED": 201,
    "CLIENT_ERROR": 400,
    "SERVER_ERROR": 500,
}


server = Flask(__name__)
CORS(server)
host = "0.0.0.0"


@server.route("/", methods=["GET"])
def get_ui():
    return "Blockchain implementation from scratch!"


@server.route("/chain", methods=["GET"])
def get_blockchain():
    snapshot = blockchain.get_blockchain()
    snapshot_dict = [block.__dict__.copy() for block in snapshot]
    for block in snapshot_dict:
        block["transactions"] = [tx.__dict__ for tx in block["transactions"]]
    return jsonify(snapshot_dict), status_codes["SUCCESS"]


@server.route("/transactions", methods=["GET"])
def get_outstanding_transactions():
    snapshot = blockchain.get_outstanding_transactions()
    snapshot_dict = [tx.__dict__ for tx in snapshot]
    return jsonify(snapshot_dict), status_codes["SUCCESS"]


@server.route("/node", methods=["GET"])
def get_nodes():
    nodes = list(blockchain.get_peer_nodes())
    response = {"Nodes": nodes}
    return jsonify(response), status_codes["SUCCESS"]


# TODO: get error objects and display them in UI so that clients have clear error messages
@server.route("/mine", methods=["POST"])
def mine_block():
    if blockchain.mine_block():
        block = blockchain.get_last_block()
        new_block = block.__dict__.copy()
        new_block["transactions"] = [tx.__dict__ for tx in new_block["transactions"]]
        response = {"Message": "Mining successful.", "Block": new_block}
        return jsonify(response), status_codes["CREATED"]
    else:
        response = {"Message": "Mining unsuccessful."}
        return jsonify(response), status_codes["SERVER_ERROR"]


@server.route("/transaction", methods=["POST"])
def add_transaction():
    tx_details = request.get_json()
    if not tx_details:
        response = {"Message": "No request body found"}
        return response, status_codes["CLIENT_ERROR"]
    # Check if incoming data has required fields
    required_fields = ["recepient", "amount"]
    if not all(field in tx_details for field in required_fields):
        response = {"Message": "Request missing required fields"}
        return response, status_codes["CLIENT_ERROR"]

    sender = wallet.public_key
    recepient = tx_details["recepient"]
    amount = tx_details["amount"]
    signature = wallet.sign_transaction(sender, recepient, amount)

    if blockchain.add_transaction(sender, recepient, amount, signature):
        transaction = blockchain.get_outstanding_transactions()[-1]
        transaction = transaction.__dict__
        response = {"Message": "Transaction successful", "Transaction": transaction}
        return jsonify(response), status_codes["CREATED"]
    else:
        response = {"Message": "Transaction unsuccessful."}
        return jsonify(response), status_codes["SERVER_ERROR"]


@server.route("/node", methods=["POST"])
def add_node():
    node_details = request.get_json()
    if not node_details:
        response = {"Message": "No request body found"}
        return response, status_codes["CLIENT_ERROR"]
    if "node" not in node_details:
        response = {"Message": "Node data invalid"}
        return response, status_codes["CLIENT_ERROR"]
    node = node_details["node"]
    blockchain.add_peer_node(node)
    response = {
        "Message": "Node added successfully.",
        "Nodes": list(blockchain.get_peer_nodes()),
    }
    return jsonify(response), status_codes["CREATED"]


@server.route("/node/<node_url>", methods=["DELETE"])
def remove_node(node_url):
    if node_url == "" or node_url == None:
        response = {"Message": "Invalid node url"}
        return jsonify(response), status_codes["CLIENT_ERROR"]
    blockchain.remove_peer_node(node_url)
    response = {
        "Message": "Node removed successfully",
        "Nodes": list(blockchain.get_peer_nodes()),
    }
    return jsonify(response), status_codes["SUCCESS"]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(node=port)
    blockchain = Blockchain(wallet.public_key + '-' + str(port))
    server.run(host=host, port=port)