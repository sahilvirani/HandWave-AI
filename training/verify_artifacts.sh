#!/usr/bin/env bash

echo "🔍 Verifying generated artifacts..."
echo "=================================="

# Check if files exist
files=("keypoints.csv" "train.npz" "val.npz" "label_mapping.npy")
all_exist=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        all_exist=false
    fi
done

if [ "$all_exist" = true ]; then
    echo ""
    echo "📊 File sizes:"
    echo "=============="
    ls -lh keypoints.csv train.npz val.npz label_mapping.npy
    
    echo ""
    echo "📈 Quick statistics:"
    echo "==================="
    
    # Check keypoints.csv
    if [ -f "keypoints.csv" ]; then
        lines=$(wc -l < keypoints.csv)
        echo "📄 keypoints.csv: $lines samples"
    fi
    
    # Check label mapping
    if [ -f "label_mapping.npy" ]; then
        echo "🏷️  label_mapping.npy: Contains class names"
    fi
    
    echo ""
    echo "✅ All artifacts verified successfully!"
    echo "🎯 Ready for Sprint 5: Model Training!"
else
    echo ""
    echo "❌ Some artifacts are missing. Please run:"
    echo "1. python extract_keypoints.py"
    echo "2. python split_dataset.py"
fi 