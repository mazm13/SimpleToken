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
