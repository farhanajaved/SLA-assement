// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UserRegistry {

    struct UserInfo {
        address userAddress;
        string providerID;
        string consumerID;
    }

    mapping(address => UserInfo) public users;
    uint8 public registeredUsersCount = 0;
    uint8 constant MAX_USERS = 50;

    event UserRegistered(address userAddress);
    event TokenAssigned(address userAddress, string providerID, string consumerID);

    function register() public returns (uint) {
        uint initialGas = gasleft();

        require(registeredUsersCount < MAX_USERS, "Max user limit reached");
        require(users[msg.sender].userAddress == address(0), "User already registered");

        // User registration
        registeredUsersCount++;
        emit UserRegistered(msg.sender);

        // Token assignment
        UserInfo memory newUser = UserInfo({
            userAddress: msg.sender,
            providerID: string(abi.encodePacked("P", uintToString(registeredUsersCount))),
            consumerID: string(abi.encodePacked("C", uintToString(registeredUsersCount)))
        });
        users[msg.sender] = newUser;
        emit TokenAssigned(msg.sender, newUser.providerID, newUser.consumerID);

        return initialGas - gasleft();
    }

    function uintToString(uint8 _uint) internal pure returns(string memory) {
        if (_uint == 0) {
            return "0";
        }
        uint8 j = _uint;
        uint8 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bStr = new bytes(len);
        int8 k = int8(len) - 1;
        while (_uint != 0) {
            bStr[uint8(k)] = bytes1(uint8(48 + _uint % 10));
            _uint /= 10;
            k--;
        }
        return string(bStr);
    }
}
