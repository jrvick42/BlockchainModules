// Joshua Vick
// Example Solidity Implementation

// Define the compiler versioning
pragma solidity >=0.6.0 <0.8.0;

contract registration {
    
    string message;
    mapping(address => bool) public user_paid;

    constructor() public {
        message = "Hello World! The contract is working!";
    }

    function payRegistration() payable public {
        // Check if the user has already registered
        if ( user_paid[msg.sender] == false ) {
            // User has not previously registered, so we log that they are now registered
            user_paid[msg.sender] = true;
        }
        else{
            // User has already registered so lets refund them
            msg.sender.send(10000000000000000000);
        }
    }

}