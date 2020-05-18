import json
from web3 import Web3, geth

# 首先确保节点已经运行起来了
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

abi = json.load(open('abi.json', 'r'))
address = json.load(open('address.json', 'r'))['address']

user = w3.eth.contract(
    address=Web3.toChecksumAddress(address), 
    abi=abi,
)

w3.eth.defaultAccount = w3.eth.accounts[1]
user1 = w3.eth.accounts[1]
# geth.personal.unlock_account(user, "456", 300)
w3.geth.personal.unlock_account(user1, "456")

tx_hash = user.functions.mint()
tx_hash = tx_hash.transact()
w3.eth.waitForTransactionReceipt(tx_hash)

print(user.functions.totalSupply().call())
