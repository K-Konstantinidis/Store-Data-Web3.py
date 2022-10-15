// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

struct People {
    uint256 favoriteNumber;
    string name;
}

contract SimpleStorage {
    uint256 favoriteNumber; //This will be a zero

    People[] public people; //Array of people
    mapping(string => uint256) public nameTofvNumber; //Map a person to their favourite number

    /*
        memory & storage
        memory:     Data will only be stored during excecution of function/contract
        storage:    Data will stay even after the excecution
        string:     Not a value type, it is an array of bytes so we should decide 
                    whether we want to store it in memory or storage
    */
    // Add a person & their favourite number in an array
    function addPerson(string memory name, uint256 fv) public {
        people.push(People(fv, name));
        nameTofvNumber[name] = fv;
    }

    /*  Store the favourite number (Retrieve it with retrieve())
        Initialized stored value = 0 */
    function store(uint256 fv) public {
        favoriteNumber = fv;
    }

    /*
        view & pure: Won't change the state of the blockchain (not making a transaction)
        view:  Reads a state of the blockchain without changing it
        pure:  Does purely math without saving the state somewhere
    */
    // Retrieve the favourite number of a person
    // Initialized retrieve value = 0
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }
}
