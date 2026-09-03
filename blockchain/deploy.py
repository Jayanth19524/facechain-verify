from solcx import compile_source, install_solc
from web3 import Web3
from dotenv import load_dotenv

import json
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

account = w3.eth.account.from_key(PRIVATE_KEY)

print("Connected:", w3.is_connected())
print("Wallet:", account.address)

install_solc("0.8.20")

with open(
    "blockchain/contracts/EvidenceRegistry.sol",
    "r"
) as f:
    contract_source = f.read()

compiled = compile_source(
    contract_source,
    solc_version="0.8.20"
)

contract_id, contract_interface = compiled.popitem()

bytecode = contract_interface["bin"]
abi = contract_interface["abi"]

EvidenceRegistry = w3.eth.contract(
    abi=abi,
    bytecode=bytecode
)

nonce = w3.eth.get_transaction_count(
    account.address
)

tx = EvidenceRegistry.constructor().build_transaction(
    {
        "from": account.address,
        "nonce": nonce,
        "gas": 3000000,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_tx = w3.eth.account.sign_transaction(
    tx,
    PRIVATE_KEY
)

tx_hash = w3.eth.send_raw_transaction(
    signed_tx.raw_transaction
)

print("Deploying...")
print("TX:", tx_hash.hex())

receipt = w3.eth.wait_for_transaction_receipt(
    tx_hash
)

print("\nContract Address:")
print(receipt.contractAddress)

with open(
    "blockchain/contract_info.json",
    "w"
) as f:
    json.dump(
        {
            "address": receipt.contractAddress,
            "abi": abi
        },
        f,
        indent=2
    )

print("\nSaved:")
print("blockchain/contract_info.json")