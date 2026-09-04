from web3 import Web3
from dotenv import load_dotenv
import requests
import hashlib

import json
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

with open("blockchain/contract_info.json", "r") as f:
    contract_info = json.load(f)

contract = w3.eth.contract(address=contract_info["address"], abi=contract_info["abi"])

cid, evidence_hash, timestamp = contract.functions.getEvidence().call()

print("\nBlockchain Record")
print("------------------")
print("CID:", cid)
print("Hash:", evidence_hash)
print("Timestamp:", timestamp)

print("\n--- Re-verifying ---")

pinata_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
print(f"Downloading from IPFS: {pinata_url}")

response = requests.get(pinata_url, timeout=15)
if response.status_code != 200:
    print(f"❌ Failed to download from IPFS. Status code: {response.status_code}")
    exit(1)

downloaded_content = response.content
computed_hash = hashlib.sha256(downloaded_content).hexdigest()

print(f"Downloaded size: {len(downloaded_content)} bytes")
print(f"Computed hash:   {computed_hash}")
print(f"On-chain hash:   {evidence_hash}")

if computed_hash == evidence_hash:
    print("\n✅ DATA IS TAMPER-PROOF — Hash matches on-chain record")
else:
    print("\n❌ DATA HAS BEEN TAMPERED WITH — Hash mismatch")
