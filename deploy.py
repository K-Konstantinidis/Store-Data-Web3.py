import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

# Look and import the .env file
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()  # Read our contract

# Install_solcx
print("Installing solc version 0.6.0 ...")
install_solc("0.6.0")

# Code to compile our Solidity Contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)  # Store the compiled_sol in a json file

# Get the Bytecode of our contract (to deploy the sol contract)
# From the compiled_code.json file we created before we need to get the bytecode
# so follow the path contracts->SimpleStorage.sol->...->bytecode->object
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get the ABI of our contract (to deploy the sol contract)
# From the compiled_code.json file we created before we need to get the abi
# so follow the path contracts->SimpleStorage.sol->...->bytecode->object
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# -----Connect to Ganache Local Blockchain-----

# Get the provider (Test net(e.g. Ganache/Goerli), Main net)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# Get the Chain ID (Network ID) [The Blockchain ID]
chain_id = 1337
# Get the address from where you will deploy
my_address = "0x73b7636298146479a275859CA3E10163675cc97f"
# Get the address private key to sign the transactions (add '0x' at the front)
# 3 ways to do it:

# 1) DO NOT DO THIS
# Hardcode the key. This key is fake:
# private_key = "0xabcdefghijklmnopqrstuvwxyz1234567890thisisafakekey1234567890xxxx"

# 2) If you want the key stored on your PC, set it as an environment variable
# os->Library for the software, getenv()->To get environment var
# private_key = os.getenv("PRIVATE_KEY")

# 3) Best way
# Create a .env file. A file to store environment variables
# Get the private key from that file
# DO NOT push the .env file to Github etc.
# Add it in a .gitignore file to be sure you won't push it
# Insert this line in the .env: export PRIVATE_KEY = 0xYour_Key_Code
private_key = os.getenv("PRIVATE_KEY")

# -----Deploy our contract-----

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
# nonce of an account is a hash number that shows the number of transactions this acc has made
nonce = w3.eth.getTransactionCount(my_address)
# ----1. Build a transaction----
# SimpleStorage doesn't have a constructor, so the constructor is just blank
# We have to pass some transaction parameters
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# ----2. Sign a transaction----
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract...")
# ----3. Send the transaction on the blockchain----
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to '{tx_receipt.contractAddress}'")

# Working with deployed Contracts. We always need:
# Contract Address
# Contract ABI

# -----Retrieve the value-----

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call:     Simulate making a call and getting a return value (Won't make a change to the blockchain)
# Transact: Actually making a state change to the blockchain
# This is our initial value of favourite number in SimpleStorage.sol
print(f"Initial Stored Value: {simple_storage.functions.retrieve().call()}")

# ----1. Create a transaction----
store_transaction = simple_storage.functions.store(10).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# ----2. Sign a transaction----
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating Contract...")
# ----3. Send the transaction----
tx_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Waiting for transaction to finish")
# Wait for the transaction to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)
print(f"Updated stored Value: {simple_storage.functions.retrieve().call()}")
