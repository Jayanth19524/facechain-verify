import requests
import os
from dotenv import load_dotenv
from evidence.evidence_service import EvidenceService

load_dotenv()

class BlockchainService:
    def __init__(self):
        self.pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.headers = {"Authorization": f"Bearer {os.getenv('PINATA_JWT')}"}

    def upload_to_ipfs(self, file_path):
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(self.pinata_url, files=files, headers=self.headers)
            result = response.json()
            if result.get("IpfsHash") or result.get("cid"):
                return result.get("IpfsHash") or result.get("cid")
            raise Exception("IPFS upload failed")

    def store_on_chain(self, cid, evidence_hash):
        # This would interact with the Ethereum contract
        print(f"Storing on chain: CID={cid}, Hash={evidence_hash}")
        pass

    def get_evidence(self):
        # Retrieve evidence from chain
        pass