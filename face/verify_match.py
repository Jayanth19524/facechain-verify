import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_thresh=0.3, det_size=(640, 640))

def get_embedding(image_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    if max(h, w) > 1024:
        scale = 1024 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    faces = app.get(img, max_num=1, det_metric="area")

    if not faces:
        raise Exception(f"No face found in {image_path}")

    return faces[0].embedding

def verify_match(image1, image2):
    face1 = get_embedding(image1)
    face2 = get_embedding(image2)
    similarity = np.dot(face1, face2) / (
        np.linalg.norm(face1) * np.linalg.norm(face2)
    )
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