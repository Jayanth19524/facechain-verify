import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    providers=["CPUExecutionProvider"]
)

app.prepare(ctx_id=0)

def get_embedding(image_path):
    image = cv2.imread(image_path)

    faces = app.get(image)

    if not faces:
        raise Exception(f"No face found in {image_path}")

    return faces[0].embedding

emb1 = get_embedding("samples/face1.jpg")
emb2 = get_embedding("samples/face2.jpg")

similarity = np.dot(
    emb1,
    emb2
) / (
    np.linalg.norm(emb1)
    * np.linalg.norm(emb2)
)

if similarity >= 0.60:
    print("MATCH")
elif similarity >= 0.30:
    print("POSSIBLE MATCH")
else:
    print("NO MATCH")

print(f"Similarity: {similarity:.4f}")
