# ERC721 based Simple-Token for Goods Trace
## Enviroments
The whole project runs under macOS, thus the following instructions apply to the macOS system, which of course can be refered to by other systems.
### Requirements
#### Ethereum, 1.9.14-stable
Our project is based on Ethereum, which means you need to install Ethereum firstly. By far the easiest way to install go-ethereum is to use Homebrew tap. Detailed instructions is [here](https://github.com/ethereum/go-ethereum/wiki/Installation-Instructions-for-Mac). 
```
brew tap ethereum/ethereum
brew install ethereum
```
#### npm, 6.14.4
```
brew install npm
```
with npm you can instal some usable package for JavaScript programming language, such as `truffle`, actually I just use truffle to flatten my contract so that I can debug my solidity contract on [Remix](https://remix.ethereum.org/) easilier. Install `truffle-flatten`(version 6.14.4) as blow: 
```
npm install -g truffle-flatten
```
Out contract is under ERC721, download corresponding modules here
```
npm install @openzeppelin/contracts
```
#### Python 3.7.4
The project use Python to contact with Ethereum node and deploy APIs. The following Python packages are necessary.
* web3.py 5.9.0
* flask, 1.1.1
* (optional) py-solc, 3.2.0
```
pip install web3, flask, py-solc
```
`py-solc` is used for compile your Ethereum solidity contract and deploy it in Python code, before that you need to install `solc`.
```
brew install solc
```
Since I use Remix complie the contract and deploy it in Javascript console instead of Python(because of version problems), it is optional.
### Useage
#### Run Ethereum node
Firstly, you need to create the genesis block as follows
```
mkdir -p blockdata
geth --datadir blockdata init blockconfig/genesis.json
```
Then run the Ethereum node
```
geth console --datadir blockdata \
    --networkid 65535 \
    --rpc \
    --rpcaddr 127.0.0.1 \
    --rpcport 8545 \
    --rpcapi="db,eth,net,web3,personal,web3" \
    --allow-insecure-unlock
```
parameters details
* networkid, for other nodes commucating with it.
* rpc(/addr/port/api), for other nodes(web3 etc.) can invoke geth apis
* allow-insecure-unlock, for you can unlock account in the console for deploying contract and doing transactions.
Then you enter Javascript console, add some accounts here(replace \_passphrase)
```
personal.newAccount(_passphrase)
```
start or stop mining
```
miner.start()
miner.stop()
```
The default account is the first account you created.
#### Deploy contract
The contract is in `contracts/SimpleToken.sol`, flatten it to `output.sol`
```
truffle-flatten contracts/SimpleToken.sol > output.sol
```
then copy content in `output.sol` to [Remix](https://remix.ethereum.org/), set solidity version to `0.4.24`. Copy ABI in Compilation Details to `FlaskRestfulAPI/abi.json`. 
Start a new console, enter the node
```
geth --datadir blockdata --networdid 65535 --allow-insecure-unlock attach
```
Unlock the first created account
```
personal.unlockAccount(eth.accounts[0], _passphrase, 300)
```
MAKE SURE the miner is working(run `miner.start()` in the other console), then copy WEB3DEPLOY from Remix Compilation Details to the console. The contract is deployed if seeing contract address. Copy the address to `FlaskRestfulAPI/address.json`.
#### Startup HTTP API with Flask
```
cd FlaskRestfulAPI
FLASK_APP=app.py flask run
```
Now you can invoke HTTP API with port 5000! :smile:
#### API
We implement those APIs, with which you can commucate with Ethereum node.
* https://localhost:5000/blockchain/accounts
    - methods: GET
    - Function: list all accounts address
    - Parameter: None
    - Return: a list of accounts address
* https://localhost:5000/blockchain/create_token
    - methods: POST
    - Function: create token
    - Parameter: `{'address': account_address, 'passphrase': passphrase}`
    - Return: a dict of created token and transact hash
* https://localhost:5000/blockchain/balance_of
    - methods: POST
    - Function: get balance of the account
    - Parameter: `{'address': account_address}`
    - Return: the number of tokens the account owns
* https://localhost:5000/blockchain/owned_tokens
    - methods: POST
    - Function: get all tokens the account owns
    - Parameter: `{'address': account_address}`
    - Return: a list tokens the account owns
* https://localhost:5000/blockchain/transer_from
    - methods: POST
    - Function: transfer tokens from seller to buyer
    - Parameter: `{'_from': seller_address, 'passphrase': seller_passphrase, '_to': buyer_address, '_token_id': token_id}`
    - Return: a dict of succeed info and transaction hash
* https://localhost:5000/blockchain/select_transaction_with_tokenId
    - methods: POST
    - Function: look up all transactions recored with token id
    - Parameter: `{'_token_id': token_id}`
    - Return: a list of all transaction recored relevant to the token id
* https://localhost:5000/blockchain/select_transaction_with_address
    - methods: POST
    - Function: look up all transactions record with account address
    - Parameter: `{'address': account_address}`
    - Return: a list of all transaction recored relevant to the account address