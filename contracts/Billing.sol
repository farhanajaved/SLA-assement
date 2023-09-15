// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Penalty.sol";  // Make sure you correctly import the Penalty contract.

contract Billing {
    address public owner;
    Penalty public penaltyContract;  // An instance of the Penalty contract.
    uint256 public PENALTY_RATE_IN_USD = 1;  // 1 penalty point = 1 USD

    mapping(address => uint256) public balances;

    event FundsRequested(address indexed consumer, uint256 amount);
    event FundsTransferred(address indexed provider, address indexed consumer, uint256 amount);

    constructor(address _penaltyContractAddress) {
        owner = msg.sender;
        penaltyContract = Penalty(_penaltyContractAddress);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function calculateTotalPenalty(address _provider) public view returns (uint256) {
        (, uint256 totalPenalty) = penaltyContract.getProviderData(_provider);
        return totalPenalty * PENALTY_RATE_IN_USD;
    }

    function requestFunds(address consumer, uint256 amount) public onlyOwner {
        emit FundsRequested(consumer, amount);
    }

    function depositFunds() public payable {
        balances[msg.sender] += msg.value;
    }

    function transferFunds(address provider, address consumer, uint256 serviceCost) public onlyOwner {
        uint256 penaltyAmount = calculateTotalPenalty(provider);
        require(serviceCost >= penaltyAmount, "Penalty exceeds service cost");

        uint256 finalAmount = serviceCost - penaltyAmount;

        // Emitting event for testing purposes, no actual transfer
        emit FundsTransferred(provider, consumer, finalAmount);
    }

    function withdrawFunds(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
