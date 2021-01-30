// Version Specification
pragma solidity >=0.7.4;

// Example Contract
contract hello {

    // Structs
    struct account {
        address addr;
        string username;
        enum account_type { individual, joint };
    }

    // Variables
    string message = "Hello World";
    bool allowed;
    int count;

    mapping ( string => account ) public user_accounts;

    // Constructor
    constructor( bool b, int i ) {
        allowed = b;
        count = i;
    }

    // Modifier
    modifier if_allowed() {
        require( allowed == true, "You are not allowed to perform this action" );
        _;
    }

    // Functions
    function inc_or_dec() public {
        if ( allowed == true ) {
            count += 1;
        }
        else if ( allowed == false ){
            count -= 1;
        }
    }

    function get_message() public if_allowed view returns ( string memory ) {
        return message;
    }

    function add_account( address u_addr, string memory u_name ) public {
        user_accounts[ u_name ] = account( u_addr, u_name);
    }
}


