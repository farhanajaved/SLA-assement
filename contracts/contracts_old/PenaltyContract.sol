// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract PenaltyContract {

    uint256 constant BASE_PENALTY = 100;

    struct BreachDetail {
        uint256 timestamp;
        uint256 penaltyAmount;
    }

    mapping(address => BreachDetail[]) public breachHistory;

    event SLABreach(address indexed domain, uint256 timestamp, uint256 penaltyAmount);

    modifier onlyAdmin() {
        // For this example, we assume only the contract owner is an admin
        require(msg.sender == owner, "Only admin can call this function");
        _;
    }

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function reportBreach(address domain, uint256 severity) public onlyAdmin {
        uint256 penalty = calculatePenalty(domain, severity);
        
        breachHistory[domain].push(BreachDetail({
            timestamp: block.timestamp,
            penaltyAmount: penalty
        }));
        
        emit SLABreach(domain, block.timestamp, penalty);
    }

    function calculatePenalty(address domain, uint256 severity) internal view returns (uint256) {
        uint256 consecutiveBreaches = breachHistory[domain].length;
        return BASE_PENALTY * (1 + consecutiveBreaches) * severity;
    }

    function getBreachHistory(address domain) public view returns (BreachDetail[] memory) {
        return breachHistory[domain];
    }
}
