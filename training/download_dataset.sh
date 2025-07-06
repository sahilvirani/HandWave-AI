#!/usr/bin/env bash
set -e

echo "📥 Downloading ASL Alphabet dataset..."
echo "🔍 Checking Kaggle CLI setup..."

# Check if kaggle CLI is installed
if ! command -v kaggle &> /dev/null; then
    echo "❌ Kaggle CLI not found. Installing..."
    pip install kaggle
fi

# Check if API key exists
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo "❌ Kaggle API key not found!"
    echo "📋 Please set up your Kaggle API key:"
    echo "1. Go to https://www.kaggle.com/account"
    echo "2. Click 'Create New API Token'"
    echo "3. Download kaggle.json"
    echo "4. Run: mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/"
    echo "5. Run: chmod 600 ~/.kaggle/kaggle.json"
    echo "6. Then run this script again"
    exit 1
fi

echo "✅ Kaggle CLI ready"
echo "🔽 Downloading dataset (this may take 5-10 minutes)..."

# Download and unzip
kaggle datasets download grassknoted/asl-alphabet -f asl_alphabet.zip --unzip

# Create directory structure
mkdir -p data
mv asl_alphabet_train data/

# Clean up
rm -f asl_alphabet.zip

echo "✅ Dataset ready under training/data/asl_alphabet_train"
echo "📊 Dataset statistics:"
echo "   - Total size: ~1.1GB"
echo "   - Letters: A-Z (excluding J, Z for motion)"
echo "   - Images per letter: ~3000"
echo "   - Image format: 200x200 PNG"

# Quick verification
if [ -d "data/asl_alphabet_train" ]; then
    letter_count=$(ls -1 data/asl_alphabet_train | wc -l)
    echo "   - Letter folders found: $letter_count"
    
    # Count images in A folder as sample
    if [ -d "data/asl_alphabet_train/A" ]; then
        a_count=$(ls -1 data/asl_alphabet_train/A/*.png 2>/dev/null | wc -l)
        echo "   - Sample (Letter A): $a_count images"
    fi
fi

echo ""
echo "🎯 Next steps:"
echo "1. Run: python extract_keypoints.py"
echo "2. Run: python split_dataset.py" 