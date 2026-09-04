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

python -m pipeline.run_pipeline --input "$INPUT_IMAGE" --verbose

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       ✅ PIPELINE COMPLETE — Verifying On-Chain Record    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

python blockchain/verify_blockchain.py

echo ""
echo "✅ Done!"