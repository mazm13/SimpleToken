import json
import csv
from datetime import datetime

from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3


DATABASE_FILE = '.database.csv'

def record_transaction(timestamp, _from, _to, _token_id, tx_hash):
    with open(DATABASE_FILE, 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([timestamp, _from, _to, _token_id, tx_hash])


def read_transaction():
    tx_records = []
    with open(DATABASE_FILE, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            tx_records.append(row)
    return tx_records


def select_record_with_token_id(token_id):
    tx_records = read_transaction()
    filtered_records = []
    for r in tx_records:
        timestamp, _from, _to, _token_id, tx_hash = r
        if _token_id == token_id:
            filtered_records.append(r)
    return filtered_records


def select_record_with_address(address, filter_field=['_from', '_to']):
    tx_records = read_transaction()
    filtered_records = []
    for r in tx_records:
        timestamp, _from, _to, _token_id, tx_hash = r
        if '_from' in filter_field and _from == address:
            filtered_records.append(r)
        elif '_to' in filter_field and _to == address:
            filtered_records.append(r)
    return filtered_records


def format_record(records):
    formated_record = []
    for r in records:
        timestamp, _from, _to, _token_id, tx_hash = r
        formated_record.append(','.format(r))
    return formated_record


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
    created_token = str(created_token)

    timestamp = datetime.strftime(datetime.now(), '%m/%d/%Y, %H:%M:%S.%f')
    record_transaction(timestamp, '_CREATE', address, created_token, tx_hash)

    return jsonify({'token': created_token, 'transact_hash': str(tx_hash)}), 200


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


@app.route("/blockchain/owned_tokens", methods=['POST'])
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
        token = contract.functions.tokenOfOwnerByIndex(address, i).call()
        tokens.append(str(token))

    return jsonify(tokens), 200


@app.route("/blockchain/transfer_from", methods=['POST'])
def transfer_from():
    _from = request.form.get('_from', None)
    _to = request.form.get('_to', None)
    _token_id = request.form.get('_token_id', None)
    if _from is None or _from not in w3.eth.accounts:
        return jsonify({'error': "Invalid _from address."}), 422

    passphrase = request.form.get('passphrase', None)
    if passphrase is None:
        return jsonify({'error': "No passphrase provided."}), 422
    try:
        w3.geth.personal.unlock_account(_from, passphrase)
    except:
        return jsonify({'error': "Invalid passphrase."}), 422

    if _to is None or _to not in w3.eth.accounts:
        return jsonify({'error': "Invalid _to address."}), 422
    if _token_id is None:
        return jsonify({'error': "No _token_id provided."}), 422
    _token_id = int(_token_id)
    
    w3.eth.defaultAccount = _from
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(contract_address), 
        abi=abi,
    )

    tx_hash = contract.functions.transferFrom(_from, _to, _token_id).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    timestamp = datetime.strftime(datetime.now(), '%m/%d/%Y, %H:%M:%S.%f')
    record_transaction(timestamp, _from, _to, _token_id, tx_hash)

    return jsonify({'info': "transact succeed.", 'transact_hash': str(tx_hash)})


@app.route("/blockchain/select_transaction_with_tokenId", methods=['POST'])
def select_token_id():
    _token_id = request.form.get('_token_id', None)
    records = select_record_with_token_id(_token_id)
    return jsonify(records), 200


@app.route("/blockchain/select_transaction_with_address", methods=['POST'])
def select_address():
    address = request.form.get('address', None)
    if address is None or address not in w3.eth.accounts:
        return jsonify({'error': "invalid address."}), 422

    records = select_record_with_address(address)
    return jsonify(records), 200


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
