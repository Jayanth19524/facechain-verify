import cv2
import json
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    providers=["CPUExecutionProvider"]
)

app.prepare(ctx_id=0)

image = cv2.imread("samples/face.jpg")

faces = app.get(image)

if len(faces) == 0:
    raise Exception("No face detected")

face = faces[0]

embedding = face.embedding

print(f"Faces found: {len(faces)}")
print(f"Embedding length: {len(embedding)}")

np.save("samples/embedding.npy", embedding)

metadata = {
    "faces_found": len(faces),
    "embedding_length": len(embedding)
}

with open("samples/embedding.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Embedding saved")
