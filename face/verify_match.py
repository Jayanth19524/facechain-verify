import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

def get_embedding(image_path):
    img = cv2.imread(image_path)

    faces = app.get(img)

    if not faces:
        raise Exception(f"No face found in {image_path}")

    return faces[0].embedding

face1 = get_embedding("samples/face.jpg")
face2 = get_embedding("samples/candidate.jpg")

similarity = np.dot(face1, face2) / (
    np.linalg.norm(face1) * np.linalg.norm(face2)
)

def verify_match(image1, image2):
    ...
    return float(similarity)
if __name__ == "__main__":
    similarity = verify_match(
        "samples/face.jpg",
        "samples/candidate.jpg"
    )

    print(similarity)

if similarity > 0.60:
    print("MATCH")
else:
    print("NO MATCH")