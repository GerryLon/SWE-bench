#!/bin/bash
# Script to build and push Docker images to Tencent Cloud Registry
# This script only builds images without running evaluation

set -e

echo "=========================================="
echo "Building and Pushing SWE-bench Images"
echo "=========================================="
echo ""
echo "This script will build and push:"
echo "  1. Base images (Java, Python, etc.)"
echo "  2. Environment images"
echo "  3. Instance images (one per instance)"
echo ""

# Check if logged in to Docker registry
if ! docker info | grep -q "mirrors.tencent.com"; then
    echo "⚠️  Please login to Docker registry first:"
    echo "   docker login mirrors.tencent.com"
fi

pred_json="$(realpath ./pred_gold_1.json)"

# Run build-only mode
python -m swebench.harness.run_evaluation \
    -d SWE-bench/SWE-bench_Multilingual \
    -p "${pred_json}" \
    --max_workers 8 \
    --clean=True \
    -id build_images_$(date +%Y%m%d_%H%M%S) \
    --build_only true

echo ""
echo "=========================================="
echo "✅ All images built and pushed successfully!"
echo "=========================================="
