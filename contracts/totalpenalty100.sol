// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HybridModel {
    mapping(address => uint256) public breaches;
    mapping(address => uint256) public totalPenalty;
    uint256 public maxBreaches = 100;
    uint256 w1 = 50; // weight for P_Q in percentage (range from 0 to 100)
    uint256 w2 = 50; // weight for P_H in percentage (range from 0 to 100)

    function registerBreach(uint256 numBreaches) public {
        breaches[msg.sender] += numBreaches;
        totalPenalty[msg.sender] += calculatePenalty(msg.sender);
    }

    function calculatePenalty(address user) public view returns (uint256) {
        uint256 bn = breaches[user];
        if (bn >= maxBreaches) {
            return 0;
        }
        
        uint256 pq = (bn + 1) ** 2;
        uint256 ph = pq * (maxBreaches - bn) / maxBreaches;
        
        uint256 pFinal = (w1 * pq + w2 * ph) / 100;
        
        return pFinal / 100;  // F_breach = 0.01 * P_final
    }
}
