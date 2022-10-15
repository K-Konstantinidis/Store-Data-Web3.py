# Store-Data-Web3.py

## SimpleStorage.sol
A smart contract to:
- Store and retrieve a value.
- Store a person and their favourite number

## Deploy.py
A python script to: 
- Compile our contract
- Connect to a Blockchain `(Test Net e.g. Goerli, Ganache)`
- Get the private key of an account in a **safe** way ( .env file check <a href="https://github.com/K-Konstantinidis/Store-Data-Web3.py/blob/master/deploy.py">code</a> for more info [Lines 61-75] )
- Deploy our contract:
  - Create a transaction
  - Sign the transaction
  - Send the transaction
- Retrieve the initial stored value
- Create a new transaction to update the stored value
- Retrieve the new stored value

## Help with the project
To run the code there are some requirements. You must install: 

### pip or pipx 
If you’re using a new version of Python, pip will be automatically installed.

Check if _pip_ is already installed by running the following on the command line: `pip --version`

For more information check <a href="https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/">Install pip</a>

### py-solc-x
Install _py-solc-x_ by running the following on the command line: `pip install py-solc-x`

More information: https://pypi.org/project/py-solc-x/

### web3
Install _web3_ by running the following on the command line: `pip install web3`

More information: https://web3py.readthedocs.io/en/stable/quickstart.html

### dotenv
Install _dotenv_ by running the following on the command line: `pip install python-dotenv`

More information: https://pypi.org/project/python-dotenv/

This is the Lesson 4 of the <a href="https://www.youtube.com/c/Freecodecamp">freeCodeCamp.org</a> tutorial: https://www.youtube.com/watch?v=M576WGiDBdQ with more comments.
