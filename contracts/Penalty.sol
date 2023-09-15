// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Penalty {
    address public owner;
    uint256 public constant MAX_BREACHES = 100; // Set an arbitrary limit to the maximum number of breaches

    // Provider struct to keep track of breaches, total penalties, and the latest penalties for both methods
    struct Provider {
        uint256 totalBreaches;
        uint256 totalPenalty;
        uint256 lastQuadraticPenalty;
        uint256 lastHistoryBasedPenalty;
    }

    mapping(address => Provider) public providers;

    event BreachLogged(address indexed provider, uint256 quadraticPenalty, uint256 historyBasedPenalty);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function recordBreach(address _provider) public onlyOwner returns (uint256) {
        require(providers[_provider].totalBreaches < MAX_BREACHES, "Max breaches reached for this provider");

        uint256 quadraticPenalty = (providers[_provider].totalBreaches + 1) ** 2;
        uint256 historyBasedPenalty = quadraticPenalty * (100 - providers[_provider].totalBreaches) / 100;

        providers[_provider].totalBreaches += 1;
        providers[_provider].totalPenalty += historyBasedPenalty; // Using the history-based penalty for the total penalty
        providers[_provider].lastQuadraticPenalty = quadraticPenalty;
        providers[_provider].lastHistoryBasedPenalty = historyBasedPenalty;

        emit BreachLogged(_provider, quadraticPenalty, historyBasedPenalty);

        return quadraticPenalty;
    }

    function getProviderData(address _provider) public view returns (uint256 totalBreaches, uint256 totalPenalty) {
        return (providers[_provider].totalBreaches, providers[_provider].totalPenalty);
    }

    function getQuadraticPenalty(address _provider) public view returns (uint256) {
        return providers[_provider].lastQuadraticPenalty;
    }

    function getHistoryBasedPenalty(address _provider) public view returns (uint256) {
        return providers[_provider].lastHistoryBasedPenalty;
    }
}
