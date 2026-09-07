import cv2
import numpy as np
from insightface.app import FaceAnalysis


class FaceService:
    def __init__(self, model_name: str = "buffalo_l", det_thresh: float = 0.3, det_size: tuple = (640, 640)):
        self.app = FaceAnalysis(name=model_name)
        self.app.prepare(ctx_id=0, det_thresh=det_thresh, det_size=det_size)

    def get_embedding(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise Exception(f"Could not read image: {image_path}")
        h, w = img.shape[:2]
        if max(h, w) > 1024:
            scale = 1024 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
        faces = self.app.get(img, max_num=1, det_metric="area")
        if not faces:
            raise Exception(f"No face found in {image_path}")
        return faces[0].embedding

    def verify_match(self, image1: str, image2: str) -> float:
        emb1 = self.get_embedding(image1)
        emb2 = self.get_embedding(image2)
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)