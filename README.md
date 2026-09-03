# FaceChain Verify

FaceChain Verify is an end-to-end proof-of-concept pipeline that combines face recognition, web discovery, and blockchain verification.

The system accepts a face image as input, searches the web for visually matching content, verifies the discovered content using face similarity, generates an evidence package, and stores a tamper-evident record on the blockchain.

---

## Status

### Current Stage

✅ Face Detection  
✅ Face Embedding Generation  
✅ Web Discovery (Google Cloud Vision)  
✅ Candidate Image Collection  
✅ Face Verification  
✅ Evidence Generation

### Next Stage

⬜ Evidence Hashing (SHA-256)  
⬜ IPFS Upload (Pinata)  
⬜ Ethereum Sepolia Smart Contract  
⬜ On-Chain Verification  
⬜ Streamlit UI

---

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
Candidate Image Download
    ↓
InsightFace Verification
    ↓
Evidence JSON
    ↓
SHA256 Hash
    ↓
IPFS (Pinata)
    ↓
Ethereum Sepolia
    ↓
Verification
```

---

## Features

### Face Recognition

- Detect faces from images
- Generate 512-dimensional facial embeddings
- Compare two faces using cosine similarity
- Verify discovered images against the original face

### Web Discovery

- Search the web using Google Cloud Vision Web Detection
- Extract matching pages
- Extract matching images
- Discover candidate social media content

### Evidence Generation

- Create a structured evidence package
- Store metadata about discovered content
- Record similarity scores
- Prepare evidence for blockchain attestation

### Blockchain (Planned)

- Hash evidence package
- Upload evidence to IPFS
- Store CID + hash on Ethereum Sepolia
- Verify evidence integrity against on-chain record

---

## Project Structure

```text
facechain-verify/

├── face/
│   ├── __init__.py
│   ├── encode.py
│   └── verify_match.py
│
├── search/
│   ├── __init__.py
│   ├── vision_search.py
│   └── download_image.py
│
├── pipeline/
│   ├── __init__.py
│   └── run_pipeline.py
│
├── evidence/
│   └── evidence.json
│
├── blockchain/
│
├── samples/
│   ├── face.jpg
│   ├── candidate.jpg
│   ├── face1.jpg
│   ├── face2.jpg
│   ├── embedding.npy
│   └── embedding.json
│
├── credentials/
│   └── gcp-key.json
│
├── requirements.txt
└── README.md
```

---

## Installation

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
pip install requests
pip install google-cloud-vision
pip install web3
```

Or:

```bash
pip install -r requirements.txt
```

---

## Google Cloud Vision Setup

### 1. Create a Google Cloud Project

Create a new Google Cloud project.

### 2. Enable Vision API

Enable:

```text
Cloud Vision API
```

### 3. Create Service Account

Create a service account and download credentials.

Store the key:

```text
credentials/
└── gcp-key.json
```

### 4. Set Environment Variable

```bash
export GOOGLE_APPLICATION_CREDENTIALS=credentials/gcp-key.json
```

Verify setup:

```bash
python search/vision_search.py
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

Example (same person):

```text
MATCH
Similarity: 0.6911
```

Example (different people):

```text
NO MATCH
Similarity: -0.0139
```

---

## Web Discovery

### Search Using Google Cloud Vision

```bash
python search/vision_search.py
```

Example output:

```text
=== WEB ENTITIES ===

Bobby Deol
Actor
Gentleman

=== PAGES WITH MATCHING IMAGES ===

https://www.instagram.com/...
https://www.youtube.com/...
```

Returned information:

```json
{
  "person_detected": "Bobby Deol",
  "matched_page": "https://www.instagram.com/...",
  "candidate_image": "https://images.news18.com/..."
}
```

---

## End-to-End Pipeline

Run the complete pipeline:

```bash
python -m pipeline.run_pipeline
```

Pipeline flow:

```text
Input Face
    ↓
Google Cloud Vision Search
    ↓
Candidate Image Discovery
    ↓
Image Download
    ↓
InsightFace Verification
    ↓
Evidence Generation
```

Example output:

```json
{
  "person_detected": "Bobby Deol",
  "matched_page": "https://www.youtube.com/watch?v=X82HkkPZJ4o",
  "candidate_image": "https://images.news18.com/...",
  "similarity": 0.9699,
  "verified": true,
  "timestamp": "2026-09-03T15:24:25.420010"
}
```

Generated file:

```text
evidence/
└── evidence.json
```

---

## Evidence Format

Current generated evidence:

```json
{
  "person_detected": "Bobby Deol",
  "matched_page": "https://www.youtube.com/watch?v=X82HkkPZJ4o",
  "candidate_image": "https://images.news18.com/...",
  "similarity": 0.9699,
  "verified": true,
  "timestamp": "2026-09-03T15:24:25.420010"
}
```

Future blockchain evidence:

```json
{
  "person_detected": "Bobby Deol",
  "matched_page": "...",
  "candidate_image": "...",
  "similarity": 0.9699,
  "verified": true,
  "evidence_hash": "sha256_hash",
  "ipfs_cid": "Qm...",
  "blockchain_tx": "0x...",
  "timestamp": "2026-09-03T15:24:25.420010"
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
SHA256 Hash
    ↓
IPFS Upload
    ↓
Ethereum Attestation
    ↓
Future Verification
```

---

## Technologies

### Face Recognition

- InsightFace
- ONNX Runtime
- OpenCV
- NumPy

### Search Layer

- Google Cloud Vision API
- Web Detection API

### Storage

- JSON Evidence Package
- Pinata IPFS (planned)

### Blockchain

- Ethereum Sepolia
- Web3.py
- Solidity (planned)

---

## Roadmap

### Phase 1 — Face Recognition

- [x] Face detection
- [x] Face embedding generation
- [x] Face similarity verification

### Phase 2 — Web Discovery

- [x] Google Cloud Vision integration
- [x] Candidate image discovery
- [x] Candidate image download
- [x] Face validation against discovered images

### Phase 3 — Evidence Generation

- [x] Evidence JSON creation
- [x] End-to-end pipeline execution

### Phase 4 — Blockchain

- [ ] SHA256 evidence hashing
- [ ] Pinata IPFS upload
- [ ] Ethereum Sepolia deployment
- [ ] Smart contract integration
- [ ] Verification workflow

### Phase 5 — User Interface

- [ ] Streamlit dashboard
- [ ] Upload interface
- [ ] Verification viewer

---

## Known Limitations

- Depends on Google Cloud Vision search results
- Current implementation evaluates only the top discovered candidate image
- Social media results depend on Google's indexing
- No blockchain integration yet
- No user interface yet

---

## License

MIT License
