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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-path", default="evidence/evidence.json")
    parser.add_argument("--output-path", default="evidence/evidence_hash.txt")
    opts = parser.parse_args()

    evidence_path = opts.evidence_path
    output_path = opts.output_path

    if not os.path.exists(evidence_path):
        print(f"❌ Evidence file not found: {evidence_path}")
        sys.exit(1)

    evidence_hash = compute_sha256(evidence_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(evidence_hash)

    print(f"✅ Evidence hash generated: {evidence_hash}")
    print(f"📄 Saved to: {output_path}")


if __name__ == "__main__":
    main()