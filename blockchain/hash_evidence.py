import argparse
import json
import hashlib
import os

parser = argparse.ArgumentParser()
parser.add_argument("--evidence-path", default="evidence/evidence.json")
parser.add_argument("--output-path", default="evidence/evidence_hash.txt")
args = parser.parse_args()

with open(args.evidence_path, "r") as f:
    evidence = json.load(f)

canonical_json = json.dumps(evidence, sort_keys=True)

evidence_hash = hashlib.sha256(canonical_json.encode()).hexdigest()

print("SHA256:")
print(evidence_hash)

os.makedirs(os.path.dirname(args.output_path) or ".", exist_ok=True)

with open(args.output_path, "w") as f:
    f.write(evidence_hash)

print("\nSaved:")
print(args.output_path)