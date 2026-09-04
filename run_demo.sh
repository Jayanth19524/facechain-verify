#!/bin/bash
# FaceChain Verify - One-command demo runner
# Usage: ./run_demo.sh [input_image]

set -e

INPUT_IMAGE="${1:-samples/face.jpg}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       FaceChain Verify - Full Pipeline Demo              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Input: $INPUT_IMAGE"
echo ""

if [ ! -f "$INPUT_IMAGE" ]; then
    echo "❌ Input image not found: $INPUT_IMAGE"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example and fill in your keys."
    exit 1
fi

echo "▶ Step 1: Face search & verification"
python -m pipeline.run_pipeline --input "$INPUT_IMAGE" --verbose
echo ""

echo "▶ Step 2: Generate SHA256 hash"
python evidence/hash_evidence.py
echo ""

echo "▶ Step 3: Upload evidence to IPFS"
python blockchain/upload_ipfs.py
echo ""

echo "▶ Step 4: Deploy smart contract"
python blockchain/deploy.py
echo ""

echo "▶ Step 5: Store evidence on blockchain"
python blockchain/store_evidence.py
echo ""

echo "▶ Step 6: Verify blockchain record"
python blockchain/verify_blockchain.py
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       ✅ FULL PIPELINE COMPLETE                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
