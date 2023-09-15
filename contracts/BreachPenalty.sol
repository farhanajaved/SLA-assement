// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BreachPenalty {
    
    uint256 public maxBreachValue;
    mapping(address => uint256) public consecutiveBreaches;
    
    constructor(uint256 _maxBreachValue) {
        maxBreachValue = _maxBreachValue;
    }
    
    function quadraticPenalty(uint256 breachValue) public view returns (uint256) {
        require(breachValue <= maxBreachValue, "Breach value exceeds the maximum allowed");
        return breachValue * breachValue;
    }

    function historyBasedPenalty(uint256 breachValue) public returns (uint256) {
        require(breachValue <= maxBreachValue, "Breach value exceeds the maximum allowed");
        consecutiveBreaches[msg.sender]++;
        return breachValue * consecutiveBreaches[msg.sender];
    }

    function resetConsecutiveBreaches() public {
        consecutiveBreaches[msg.sender] = 0;
    }
}
