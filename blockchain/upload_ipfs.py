import argparse
import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")

parser = argparse.ArgumentParser()
parser.add_argument("--evidence-path", default="evidence/evidence.json")
args = parser.parse_args()

url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

headers = {
    "Authorization": f"Bearer {PINATA_JWT}"
}

with open(args.evidence_path, "rb") as f:
    files = {
        "file": (os.path.basename(args.evidence_path), f)
    }

    response = requests.post(
        url,
        files=files,
        headers=headers
    )

result = response.json()

print("\nUpload Result:")
print(json.dumps(result, indent=2))

cid = (
    result.get("IpfsHash")
    or result.get("cid")
)

if cid:
    evidence_dir = os.path.dirname(args.evidence_path)
    with open(os.path.join(evidence_dir, "ipfs_cid.txt"), "w") as f:
        f.write(cid)

    print("\nSaved CID:")
    print(f"{evidence_dir}/ipfs_cid.txt")
    print(cid)