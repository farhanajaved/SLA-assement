// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TraditionalModel {
    mapping(address => uint256) public breaches;

    function registerBreach(uint256 numBreaches) public {
        breaches[msg.sender] += numBreaches;
    }

    function calculatePenalty(address user) public view returns (uint256) {
        return breaches[user] * 0.1 ether;
    }
}

contract HybridModel1 {
    mapping(address => uint256) public breaches;

    function registerBreach(uint256 numBreaches) public {
        breaches[msg.sender] += numBreaches;
    }

    function calculatePenalty(address user) public view returns (uint256) {
        uint256 pq = (breaches[user] + 1) ** 2;
        uint256 ph = pq * (100 - breaches[user]) / 100;
        return (pq + ph) / 2;
    }
}
