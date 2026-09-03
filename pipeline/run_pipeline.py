from search.download_image import download_image
from search.vision_search import search_image
from face.verify_match import verify_match

from datetime import datetime
import json
import os


INPUT_IMAGE = "samples/face.jpg"


# Step 1: Search web for matching content
search_result = search_image(INPUT_IMAGE)

print("Search Result:")
print(json.dumps(search_result, indent=2))


# Step 2: Download candidate image
candidate_path = download_image(
    search_result["candidate_image"],
    "samples/candidate.jpg"
)


# Step 3: Verify face match
similarity = verify_match(
    INPUT_IMAGE,
    candidate_path
)

print(f"Similarity: {similarity:.4f}")


# Step 4: Build evidence
evidence = {
    "person_detected": search_result["person_detected"],
    "matched_page": search_result["matched_page"],
    "candidate_image": search_result["candidate_image"],
    "similarity": similarity,
    "verified": similarity > 0.60,
    "timestamp": datetime.utcnow().isoformat()
}


# Step 5: Save evidence
os.makedirs("evidence", exist_ok=True)

with open("evidence/evidence.json", "w") as f:
    json.dump(evidence, f, indent=2)

print("\nEvidence saved to evidence/evidence.json")

print("\nEvidence:")
print(json.dumps(evidence, indent=2))