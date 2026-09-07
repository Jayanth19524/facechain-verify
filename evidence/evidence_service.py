import hashlib
import json
import os

class EvidenceService:
    def save_evidence(self, evidence_data, evidence_dir="evidence"):
        os.makedirs(evidence_dir, exist_ok=True)
        evidence_path = os.path.join(evidence_dir, "evidence.json")
        with open(evidence_path, "w") as f:
            json.dump(evidence_data, f, indent=2)
        return evidence_path

    def hash_evidence(self, evidence_path):
        with open(evidence_path, "rb") as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()

    def save_hash(self, evidence_hash, output_dir="evidence"):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "evidence_hash.txt"), "w") as f:
            f.write(evidence_hash)
        return os.path.join(output_dir, "evidence_hash.txt")