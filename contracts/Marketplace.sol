// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Marketplace {
    struct User {
        string providerProfile;
        string consumerProfile;
    }
    
    struct Service {
        address provider;
        string serviceDescription;
    }

    mapping(address => User) public users;
    mapping(address => Service[]) public services;  // Dynamic array of services for each user

    event UserRegistered(address indexed user);
    event ServiceAdded(address indexed user, string serviceDescription);
    event ServiceSelected(address indexed consumer, address indexed provider, string serviceDescription);
    
    function registerUser(string memory providerProfile, string memory consumerProfile) public {
        require(bytes(users[msg.sender].providerProfile).length == 0, "User already registered");
        
        users[msg.sender] = User(providerProfile, consumerProfile);
        
        emit UserRegistered(msg.sender);
    }
    
    function addService(string memory serviceDescription) public {
        require(bytes(users[msg.sender].providerProfile).length > 0, "User not registered");
        require(services[msg.sender].length < 5, "Exceeded max services per user");
        
        services[msg.sender].push(Service(msg.sender, serviceDescription));
        
        emit ServiceAdded(msg.sender, serviceDescription);
    }
    
    function selectService(address provider, uint serviceIndex) public {
        require(bytes(users[msg.sender].consumerProfile).length > 0, "User not registered as consumer");
        require(serviceIndex < services[provider].length, "Invalid service index");
        
        Service memory selectedService = services[provider][serviceIndex];
        
        emit ServiceSelected(msg.sender, selectedService.provider, selectedService.serviceDescription);
    }

    // Add this function to your existing Marketplace contract
    function getServiceCount(address provider) public view returns (uint) {
    return services[provider].length;
}
}
