#!/usr/bin/env python3
"""
FaceChain Verify - Generate SHA256 hash of evidence file.
Outputs to evidence/evidence_hash.txt
"""

import hashlib
import os
import sys


def compute_sha256(filepath: str) -> str:
    with open(filepath, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()


def main():
    evidence_path = "evidence/evidence.json"
    output_path = "evidence/evidence_hash.txt"

    if not os.path.exists(evidence_path):
        print(f"❌ Evidence file not found: {evidence_path}")
        print("Run the pipeline first: python -m pipeline.run_pipeline")
        sys.exit(1)

    evidence_hash = compute_sha256(evidence_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(evidence_hash)

    print(f"✅ Evidence hash generated: {evidence_hash}")
    print(f"📄 Saved to: {output_path}")


if __name__ == "__main__":
    main()