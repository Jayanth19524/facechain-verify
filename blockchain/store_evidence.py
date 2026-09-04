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

pending_count = w3.eth.get_transaction_count(account.address, "pending")
latest_count = w3.eth.get_transaction_count(account.address, "latest")
pending_txs = pending_count - latest_count

if pending_txs > 0:
    print(f"Canceling {pending_txs} pending transaction(s)...")
    cancel_nonce = latest_count
    cancel_tx = w3.eth.account.sign_transaction(
        {
            "from": account.address,
            "to": account.address,
            "value": 0,
            "nonce": cancel_nonce,
            "gas": 21000,
            "gasPrice": int(w3.eth.gas_price * 1.5)
        },
        PRIVATE_KEY
    )
    cancel_hash = w3.eth.send_raw_transaction(cancel_tx.raw_transaction)
    print(f"Cancel tx: {cancel_hash.hex()}")
    try:
        w3.eth.wait_for_transaction_receipt(cancel_hash, timeout=120, poll_latency=10)
    except Exception:
        pass

nonce = w3.eth.get_transaction_count(account.address, "pending")

gas_price = int(w3.eth.gas_price * 1.5)

tx = contract.functions.storeEvidence(
    cid,
    evidence_hash
).build_transaction(
    {
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": gas_price
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
print(f"Nonce: {nonce}, Gas Price: {gas_price}")

receipt = w3.eth.wait_for_transaction_receipt(
    tx_hash,
    timeout=300,
    poll_latency=10
)

print("\nStored!")
print("TX:", tx_hash.hex())