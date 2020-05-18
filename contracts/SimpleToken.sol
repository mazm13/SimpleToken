pragma solidity ^0.4.24;

import 'zeppelin-solidity/contracts/token/ERC721/ERC721Token.sol';

contract SimpleToken is ERC721Token {
    
    uint private nonce = 0;
    
    constructor() ERC721("GameItem", "ITM") public { }

    function random() public returns(uint) {
        nonce += 1;
        return uint(keccak256(abi.encodePacked(nonce)));
    }

    function mint() public {
        _mint(_msgSender(), random());
    }
}