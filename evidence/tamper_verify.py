#!/usr/bin/env python3
"""
FaceChain Verify - Tamper Verification Demo.

Demonstrates both the ✅ (integrity matches) and ❌ (tampered) verification paths.
Core concept: SHA256 hash of evidence file → stored on-chain → any change
produces a different hash, which is cryptographically detected.
"""
import hashlib
import json
import os
import subprocess
import sys


def compute_sha256(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    evidence_path = "evidence/evidence.json"
    hash_path = "evidence/evidence_hash.txt"

    # Save original evidence for restoration later
    with open(evidence_path, "r") as f:
        original_evidence = f.read()

    try:
        # ==========================================
        # PATH 1: Original (✅ hash matches on-chain)
        # ==========================================
        print("=" * 60)
        print("PATH 1: Original evidence (integrity verified)")
        print("=" * 60)

        # Run blockchain verification script
        result1 = subprocess.run(
            [sys.executable, "blockchain/verify_blockchain.py"],
            cwd="/Users/jayanth-gvs/facechain-verify",
            capture_output=True,
            text=True,
        )
        print(result1.stdout)

        # ==========================================
        # PATH 2: Tampered evidence (❌ hash mismatch)
        # ==========================================
        print("\n" + "=" * 60)
        print("PATH 2: Tampered evidence (tamper detection)")
        print("=" * 60)

        # Alter the evidence JSON (change person name)
        with open(evidence_path, "r") as f:
            evidence = json.load(f)

        evidence["person_detected"] = "TAMPERED_Person"

        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)

        # Recompute SHA256 hash of altered evidence
        with open(evidence_path, "rb") as f:
            tampered_content = f.read()
        tampered_hash = hashlib.sha256(tampered_content).hexdigest()

        # Save the tampered hash
        with open(hash_path, "w") as f:
            f.write(tampered_hash)

        print(f"✅ Altered evidence.json: person_detected changed to 'TAMPERED_Person'")
        print(f"🔑 New SHA256 hash: {tampered_hash}")

        # Run blockchain verification - should show ❌ mismatch
        result2 = subprocess.run(
            [sys.executable, "blockchain/verify_blockchain.py"],
            cwd="/Users/jayanth-gvs/facechain-verify",
            capture_output=True,
            text=True,
        )
        print(result2.stdout)

        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("✅ Original: hash matches on-chain record (verified)")
        print("❌ Tampered: hash mismatch detected (tamper-proof!)")

    finally:
        # Restore original evidence
        with open(evidence_path, "w") as f:
            f.write(original_evidence)
        # Restore original hash
        with open(evidence_path, "rb") as f:
            original_content = f.read()
        restored_hash = hashlib.sha256(original_content).hexdigest()
        with open(hash_path, "w") as f:
            f.write(restored_hash)
        print(f"\n🔄 Restored original evidence.json and hash ({restored_hash})")


if __name__ == "__main__":
    main()