import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")

url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

headers = {
    "Authorization": f"Bearer {PINATA_JWT}"
}

with open("evidence/evidence.json", "rb") as f:
    files = {
        "file": ("evidence.json", f)
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
    with open("evidence/ipfs_cid.txt", "w") as f:
        f.write(cid)

    print("\nSaved CID:")
    print("evidence/ipfs_cid.txt")
    print(cid)