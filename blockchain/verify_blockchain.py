from web3 import Web3
from dotenv import load_dotenv

import json
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")

w3 = Web3(
    Web3.HTTPProvider(RPC_URL)
)

with open(
    "blockchain/contract_info.json",
    "r"
) as f:
    contract_info = json.load(f)

contract = w3.eth.contract(
    address=contract_info["address"],
    abi=contract_info["abi"]
)

cid, evidence_hash, timestamp = (
    contract.functions.getEvidence().call()
)

print("\nBlockchain Record")
print("------------------")
print("CID:", cid)
print("Hash:", evidence_hash)
print("Timestamp:", timestamp)