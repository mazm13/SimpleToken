import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
abi = json.load(open('abi.json', 'r'))
address = json.load(open('address.json', 'r'))['address']

# Initializing flask app
app = Flask(__name__)

@app.route("/blockchain/create_token", methods=['GET'])
def create_token():
    w3.eth.defaultAccount = w3.eth.accounts[0]
    user0 = w3.eth.accounts[0]
    # geth.personal.unlock_account(user, "456", 300)
    w3.geth.personal.unlock_account(user0, "123")
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(address), 
        abi=abi,
    )
    tx_hash = contract.functions.mint()
    tx_hash = tx_hash.transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    return "<p>successed</p>"
