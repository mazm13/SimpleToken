import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
abi = json.load(open('abi.json', 'r'))
contract_address = json.load(open('address.json', 'r'))['address']

# Initializing flask app
app = Flask(__name__)

@app.route("/blockchain/accounts", methods=['GET'])
def accounts():
    accounts = w3.eth.accounts
    return jsonify(accounts), 200


@app.route("/blockchain/create_token", methods=['POST'])
def create_token():
    address = request.form.get('address', None)
    if address is None or address not in w3.eth.accounts:
        return jsonify({'error': "Invalid address."}), 422

    passphrase = request.form.get('passphrase', None)
    if passphrase is None:
        return jsonify({'error': "No passphrase provided."}), 422

    w3.eth.defaultAccount = address
    try:
        w3.geth.personal.unlock_account(address, passphrase)
    except:
        return jsonify({'error': "Invalid passphrase."}), 422

    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(contract_address), 
        abi=abi,
    )
    tx_hash = contract.functions.mint()
    tx_hash = tx_hash.transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    token_counts = contract.functions.balanceOf(address).call()
    created_token = contract.functions.tokenOfOwnerByIndex(address, token_counts - 1).call()

    return jsonify({'token': created_token}), 200


@app.route("/blockchain/balance_of", methods=['POST'])
def balance_of():
    address = request.form.get('address', None)
    if address is None or address not in w3.eth.accounts:
        return jsonify({'error': "invalid address."}), 422

    w3.eth.defaultAccount = address
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(contract_address), 
        abi=abi,
    )
    balance_of = contract.functions.balanceOf(address).call()
    return str(balance_of)


@app.route("/bloackchain/owned_tokens", methods=['POST'])
def owned_tokens():
    address = request.form.get('address', None)
    if address is None or address not in w3.eth.accounts:
        return jsonify({'error': "invalid address."}), 422

    w3.eth.defaultAccount = address
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(contract_address), 
        abi=abi,
    )
    token_counts = contract.functions.balanceOf(address).call()

    tokens = []
    for i in range(token_counts):
        tokens.append(contract.functions.tokenOfOwnerByIndex(address, i).call())

    return jsonify(tokens), 200


@app.route('/blockchain/testing', methods=['POST'])
def testing():
    # if 'address' not in request.form:
    #     return jsonify({'error': 'No user address provided.'}), 422
    # if 'password' not in request.form:
    #     return jsonify({'error': 'No user password provided.'}), 422
    address = request.form['address']
    password = request.form['password']

    print(type(address))
    print(type(password))
    print(w3.eth.accounts[0])
    print(address)
    print(address == w3.eth.accounts[0])

    print(address)
    print(password)

    w3.geth.personal.unlock_account(address, password)
    # if address not in w3.eth.accounts:
    #     return jsonify({'error': 'User address not in accounts list.'}), 422

    # w3.eth.defaultAccount = address
    # try:
        
    # except:
    #     return jsonify({'error': 'Unable to unlock the account'}), 422

    return jsonify({'address':address, 'password':password}), 200
