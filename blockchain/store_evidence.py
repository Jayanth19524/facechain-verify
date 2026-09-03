from web3 import Web3
from dotenv import load_dotenv

import json
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

account = w3.eth.account.from_key(
    PRIVATE_KEY
)

with open(
    "blockchain/contract_info.json",
    "r"
) as f:
    contract_info = json.load(f)

contract_address = contract_info["address"]
abi = contract_info["abi"]

contract = w3.eth.contract(
    address=contract_address,
    abi=abi
)

with open(
    "evidence/ipfs_cid.txt",
    "r"
) as f:
    cid = f.read().strip()

with open(
    "evidence/evidence_hash.txt",
    "r"
) as f:
    evidence_hash = f.read().strip()

nonce = w3.eth.get_transaction_count(
    account.address
)

tx = contract.functions.storeEvidence(
    cid,
    evidence_hash
).build_transaction(
    {
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.eth.gas_price
    }
)

signed_tx = w3.eth.account.sign_transaction(
    tx,
    PRIVATE_KEY
)

tx_hash = w3.eth.send_raw_transaction(
    signed_tx.raw_transaction
)

print("Submitting...")

receipt = w3.eth.wait_for_transaction_receipt(
    tx_hash
)

print("\nStored!")
print("TX:", tx_hash.hex())