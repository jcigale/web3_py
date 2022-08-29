from solcx import compile_standard, install_solc
install_solc("0.6.0")
import json
from web3 import Web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*" : {"*" : ["abi","metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


#connect to ganache blockchain
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x03a16847aFb8ED99d1d277421C088deB894eb937"
private_key = "0x4bddb215b26b838250fbcbd352bbb652cd9e18ff51d4568df3fb900cb3135a29"

#Create contract with python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#Get the latest transaction/nonce
nonce = w3.eth.getTransactionCount(my_address)

#Create transaction
transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce})

#Sign Transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#Send signedd transaction
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)