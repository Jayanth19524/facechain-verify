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

evidence_count = contract.functions.getEvidenceCount().call()

print("\nBlockchain Records")
print("==================")
print(f"Total records stored: {evidence_count}")

for i in range(1, int(evidence_count) + 1):
    cid, evidence_hash, timestamp, person_detected = contract.functions.getEvidence(i).call()
    print(f"\nRecord {i}:")
    print(f"  CID: {cid}")
    print(f"  Hash: {evidence_hash}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Person: {person_detected}")

print("\n--- Re-verifying latest record ---")

latest_id = int(evidence_count)
cid, evidence_hash, timestamp, person_detected = contract.functions.getEvidence(latest_id).call()

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