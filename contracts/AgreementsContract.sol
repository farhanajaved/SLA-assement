// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract AgreementsContract {

    uint256 constant BASE_PENALTY = 100;
event DebugAgreement(bytes32 agreementId, uint256 createdAt);

    struct Agreement {
        address party1;
        address party2;
        uint256 createdAt;
    }

    struct BreachDetail {
        uint256 timestamp;
        uint256 penaltyAmount;
    }

    mapping(bytes32 => Agreement) public agreements;
    mapping(bytes32 => BreachDetail[]) public breachHistory;

    // Create an agreement between two users
    function createAgreement(address party2) public {
        bytes32 agreementId = createAgreementId(msg.sender, party2);

        agreements[agreementId] = Agreement({
            party1: msg.sender,
            party2: party2,
            createdAt: block.timestamp
        });
    }

    // Create an agreement ID based on the two user addresses
    function createAgreementId(address user1, address user2) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(user1, user2));
    }

// ... inside reportBreach before the require statement

    // Report a breach for an agreement
    function reportBreach(address party2, uint256 severity) public {
    bytes32 agreementId = createAgreementId(msg.sender, party2);
    
    emit DebugAgreement(agreementId, agreements[agreementId].createdAt);
    
    require(agreements[agreementId].createdAt != 0, "Agreement doesn't exist");

        uint256 penalty = calculatePenalty(agreementId, severity);
        
        breachHistory[agreementId].push(BreachDetail({
            timestamp: block.timestamp,
            penaltyAmount: penalty
        }));
    }

    function calculatePenalty(bytes32 agreementId, uint256 severity) internal view returns (uint256) {
        uint256 consecutiveBreaches = breachHistory[agreementId].length;
        return BASE_PENALTY * (1 + consecutiveBreaches) * severity;
    }

    // Helper function to retrieve the breach count
    function getBreachCount(address party1, address party2) public view returns (uint256) {
        bytes32 agreementId = createAgreementId(party1, party2);
        return breachHistory[agreementId].length;
    }
}
