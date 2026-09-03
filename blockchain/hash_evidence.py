import json
import hashlib
import os

with open("evidence/evidence.json", "r") as f:
    evidence = json.load(f)

canonical_json = json.dumps(
    evidence,
    sort_keys=True
)

evidence_hash = hashlib.sha256(
    canonical_json.encode()
).hexdigest()

print("SHA256:")
print(evidence_hash)

os.makedirs("evidence", exist_ok=True)

with open("evidence/evidence_hash.txt", "w") as f:
    f.write(evidence_hash)

print("\nSaved:")
print("evidence/evidence_hash.txt")