# FaceChain Verify

FaceChain Verify is an end-to-end proof-of-concept pipeline that combines face recognition, web discovery, evidence generation, IPFS storage, and blockchain verification.

The system accepts a face image as input, searches the web for visually matching content, verifies the discovered content using face similarity, generates a cryptographically verifiable evidence package, stores the evidence on IPFS, and records its fingerprint on the Ethereum blockchain for future verification.

---

# Current Status

## Completed

- ✅ Face Detection
- ✅ Face Embedding Generation
- ✅ Web Discovery (Google Cloud Vision)
- ✅ Candidate Image Collection
- ✅ Face Verification
- ✅ Evidence JSON Generation
- ✅ SHA256 Evidence Hashing
- ✅ IPFS Upload (Pinata)
- ✅ Ethereum Sepolia Smart Contract Deployment
- ✅ On-Chain Evidence Storage
- ✅ Blockchain Evidence Retrieval

## Remaining

- ⬜ End-to-End Tamper Verification Script
- ⬜ Streamlit Demo UI
- ⬜ Multi-Evidence Smart Contract Support

---

# Architecture

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
IPFS Upload (Pinata)
    ↓
CID
    ↓
Ethereum Sepolia Smart Contract
    ↓
Verification
```

---

# Features

## Face Recognition

- Face detection using InsightFace
- 512-dimensional facial embeddings
- Cosine similarity verification
- Face matching against discovered web images

## Web Discovery

- Google Cloud Vision Web Detection
- Matching image discovery
- Matching page discovery
- Reverse-image-search style workflow

## Evidence Generation

- Structured JSON evidence package
- Verification metadata
- Similarity score recording
- Timestamp generation

## Cryptographic Verification

- SHA256 evidence hashing
- Tamper detection
- Immutable fingerprint generation

## Decentralized Storage

- Upload evidence to IPFS
- Generate permanent CID
- Content-addressable storage

## Blockchain Verification

- Ethereum Sepolia deployment
- Smart contract storage
- On-chain hash verification
- Blockchain evidence retrieval

---

# Project Structure

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
│   ├── evidence.json
│   ├── evidence_hash.txt
│   └── ipfs_cid.txt
│
├── blockchain/
│   ├── contracts/
│   │   └── EvidenceRegistry.sol
│   │
│   ├── deploy.py
│   ├── store_evidence.py
│   ├── verify_blockchain.py
│   └── contract_info.json
│
├── samples/
│   ├── face.jpg
│   └── candidate.jpg
│
├── credentials/
│   └── gcp-key.json
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

```text
insightface
onnxruntime
opencv-python
numpy
requests
google-cloud-vision
web3
python-dotenv
py-solc-x
```

---

# Configuration

## Google Cloud Vision

```bash
export GOOGLE_APPLICATION_CREDENTIALS=credentials/gcp-key.json
```

## Environment Variables

Create `.env`

```env
PINATA_JWT=YOUR_PINATA_JWT

RPC_URL=https://eth-sepolia.g.alchemy.com/v2/XXXX

PRIVATE_KEY=YOUR_WALLET_PRIVATE_KEY
```

---

# Running The Pipeline

## Step 1 – Face Search & Verification

```bash
python -m pipeline.run_pipeline
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

Generated:

```text
evidence/evidence.json
```

---

## Step 2 – Generate SHA256 Hash

```bash
python evidence/hash_evidence.py
```

Generated:

```text
evidence/evidence_hash.txt
```

---

## Step 3 – Upload Evidence To IPFS

```bash
python blockchain/upload_ipfs.py
```

Example:

```json
{
  "IpfsHash": "Qmf7DZE32tDxWwNNFDJBcE4evpUk3SnbvqXZVsYyfKC7Q7"
}
```

Generated:

```text
evidence/ipfs_cid.txt
```

---

## Step 4 – Deploy Smart Contract

```bash
python blockchain/deploy.py
```

Example:

```text
Connected: True

Deploying...

Contract Address:
0x4d4Bb04288232...
```

Generated:

```text
blockchain/contract_info.json
```

---

## Step 5 – Store Evidence On Blockchain

```bash
python blockchain/store_evidence.py
```

Example:

```text
Stored!

TX:
0xd062d...
```

---

## Step 6 – Verify Blockchain Record

```bash
python blockchain/verify_blockchain.py
```

Example:

```text
Blockchain Record

CID:
Qmf7DZE32tDxWwNNFDJBcE4evpUk3SnbvqXZVsYyfKC7Q7

Hash:
7c205501c80...

Timestamp:
1788457380
```

---

# Smart Contract

Current contract stores:

```solidity
struct Evidence {
    string cid;
    string evidenceHash;
    uint256 timestamp;
}
```

Stored on:

```text
Ethereum Sepolia Testnet
```

---

# Example Evidence Record

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

---

# Verification Flow

```text
Face Image
    ↓
Google Cloud Vision
    ↓
Matching Content
    ↓
Face Verification
    ↓
Evidence JSON
    ↓
SHA256 Hash
    ↓
IPFS Upload
    ↓
CID
    ↓
Ethereum Storage
    ↓
Future Verification
```

---

# Technologies

## Face Recognition

- InsightFace
- ONNX Runtime
- OpenCV
- NumPy

## Search Layer

- Google Cloud Vision API
- Web Detection API

## Storage

- JSON Evidence Package
- IPFS
- Pinata

## Blockchain

- Ethereum Sepolia
- Solidity
- Web3.py
- Alchemy RPC

---

# Known Limitations

- Depends on Google Cloud Vision search results.
- Currently evaluates only the first discovered candidate image.
- Stores a single evidence record on-chain.
- Social media discovery depends on Google's indexing.
- No UI yet.
- Verification currently uses one candidate image rather than multiple corroborating sources.

---

# Hackathon Deliverable Coverage

- ✅ Face identification
- ✅ Genuine web discovery
- ✅ Matching content retrieval
- ✅ Face verification
- ✅ Evidence generation
- ✅ SHA256 hashing
- ✅ IPFS upload
- ✅ Blockchain storage
- ✅ Blockchain retrieval
- ✅ Tamper-evident verification architecture

---

# License

MIT License
