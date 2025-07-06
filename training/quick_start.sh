#!/usr/bin/env bash

echo "🚀 HandWave AI - Quick Start Pipeline"
echo "====================================="
echo ""

# Step 1: Setup verification
echo "🔍 Step 1: Verifying setup..."
python verify_setup.py
if [ $? -ne 0 ]; then
    echo "❌ Setup verification failed. Please check your environment."
    exit 1
fi

echo ""
echo "⏱️  Estimated time: 20-40 minutes total"
echo "💾 Required space: ~1.5GB"
echo ""

# Step 2: Download dataset
echo "📥 Step 2: Downloading dataset..."
./download_dataset.sh
if [ $? -ne 0 ]; then
    echo "❌ Dataset download failed. Please check your Kaggle setup."
    exit 1
fi

echo ""
echo "🤖 Step 3: Extracting keypoints (this is the longest step)..."
python extract_keypoints.py
if [ $? -ne 0 ]; then
    echo "❌ Keypoint extraction failed."
    exit 1
fi

echo ""
echo "🔄 Step 4: Creating train/val splits..."
python split_dataset.py
if [ $? -ne 0 ]; then
    echo "❌ Data splitting failed."
    exit 1
fi

echo ""
echo "✅ Step 5: Verifying results..."
./verify_artifacts.sh

echo ""
echo "🎉 PIPELINE COMPLETE!"
echo "===================="
echo "✅ All artifacts generated successfully"
echo "🎯 Ready for Sprint 5: Model Training!"
echo ""
echo "📊 Generated files:"
echo "  - keypoints.csv (raw features)"
echo "  - train.npz (training set)"
echo "  - val.npz (validation set)"
echo "  - label_mapping.npy (class mapping)" 