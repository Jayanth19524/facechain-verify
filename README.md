# FaceChain Verify

FaceChain Verify is a proof-of-concept pipeline that combines face recognition, web discovery, and blockchain verification.

The goal is to take a face image as input, discover matching content on the web, verify the discovered content using face similarity, and create a tamper-evident blockchain record of the evidence.

## Architecture

```text
Input Face
    ↓
InsightFace
    ↓
Google Cloud Vision Web Detection
    ↓
Matching Pages / Images
    ↓
InsightFace Similarity Verification
    ↓
Evidence JSON
    ↓
IPFS (Pinata)
    ↓
Ethereum Sepolia
    ↓
Verification
```

## Current Progress

### Completed

- [x] Face detection using InsightFace
- [x] Face embedding generation
- [x] Face similarity comparison
- [x] Local testing pipeline
- [x] Playwright research for reverse image search

### In Progress

- [ ] Google Cloud Vision Web Detection integration
- [ ] Candidate image collection
- [ ] Similarity-based validation pipeline

### Planned

- [ ] Evidence package generation
- [ ] IPFS upload via Pinata
- [ ] Ethereum Sepolia smart contract
- [ ] On-chain verification
- [ ] Streamlit demo UI

---

## Project Structure

```text
facechain-verify/
│
├── face/
│   ├── encode.py
│   └── compare.py
│
├── search/
│   └── vision_search.py
│
├── evidence/
│
├── blockchain/
│
├── samples/
│   ├── face.jpg
│   ├── face1.jpg
│   ├── face2.jpg
│   ├── embedding.npy
│   └── embedding.json
│
├── credentials/
│
├── requirements.txt
└── README.md
```

---

## Face Recognition

### Generate Face Embedding

```bash
python face/encode.py
```

Example output:

```text
Faces found: 1
Embedding length: 512
Embedding saved
```

Generated files:

```text
samples/
├── embedding.npy
└── embedding.json
```

---

### Compare Two Faces

```bash
python face/compare.py
```

Example:

```text
MATCH
Similarity: 0.6911
```

Different people:

```text
NO MATCH
Similarity: -0.0139
```

---

## Technologies

### Face Recognition

- InsightFace
- ONNX Runtime
- OpenCV
- NumPy

### Search Layer

- Google Cloud Vision API (Web Detection)

### Storage

- Pinata IPFS

### Blockchain

- Ethereum Sepolia
- Web3.py

---

## Setup

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install insightface
pip install onnxruntime
pip install opencv-python
pip install numpy
pip install google-cloud-vision
pip install web3
pip install requests
```

---

## Google Cloud Vision Setup

1. Create a Google Cloud Project
2. Enable Cloud Vision API
3. Create a Service Account
4. Download service account credentials

Store credentials:

```text
credentials/
└── gcp-key.json
```

Set environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=credentials/gcp-key.json
```

---

## Future Evidence Format

```json
{
  "matched_post_url": "https://example.com/post",
  "candidate_image_url": "https://example.com/image.jpg",
  "similarity_score": 0.6911,
  "image_hash": "sha256_hash",
  "timestamp": "2026-09-03T00:00:00Z",
  "source": "google_cloud_vision"
}
```

---

## Verification Flow

```text
Face Image
    ↓
Google Cloud Vision
    ↓
Candidate URLs
    ↓
Image Download
    ↓
InsightFace Verification
    ↓
Evidence JSON
    ↓
IPFS Upload
    ↓
Ethereum Attestation
    ↓
Future Verification
```

---

## Known Limitations

- Search layer not yet fully implemented
- Currently verifies only downloaded candidate images
- Depends on Google Cloud Vision Web Detection results
- Smart contract deployment not yet completed

---

## License

MIT License
