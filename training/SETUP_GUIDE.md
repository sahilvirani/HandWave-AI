# 🚀 HandWave AI - Dataset Processing Guide

## Overview
This guide walks you through downloading the ASL Alphabet dataset and processing it into ML-ready features.

**⏱️ Time Required**: 20-40 minutes
**💾 Space Required**: ~1.5GB

## 📋 Prerequisites

1. **Virtual Environment Active**:
   ```bash
   cd training
   source .venv/bin/activate
   ```

2. **Verify Setup**:
   ```bash
   python verify_setup.py
   ```

## 🔄 Complete Workflow

### Step 1: Setup Kaggle CLI (One-time setup)

```bash
# Install Kaggle CLI
pip install kaggle

# Create config directory
mkdir -p ~/.kaggle

# Download your API key from https://www.kaggle.com/account
# Move the downloaded kaggle.json to ~/.kaggle/
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set permissions
chmod 600 ~/.kaggle/kaggle.json
```

### Step 2: Download Dataset (~5-10 minutes)

```bash
# Run the download script
./download_dataset.sh
```

**Expected output**:
```
📥 Downloading ASL Alphabet dataset...
✅ Kaggle CLI ready
🔽 Downloading dataset (this may take 5-10 minutes)...
✅ Dataset ready under training/data/asl_alphabet_train
📊 Dataset statistics:
   - Total size: ~1.1GB
   - Letters: A-Z (excluding J, Z for motion)
   - Images per letter: ~3000
   - Letter folders found: 29
   - Sample (Letter A): 3000 images
```

### Step 3: Extract Keypoints (~10-30 minutes)

```bash
# Process all images with MediaPipe
python extract_keypoints.py
```

**Expected output**:
```
📁 Found dataset directory: /path/to/training/data/asl_alphabet_train
🔤 Processing letter 'A' (3000 images)
Letter A: 100%|████████████████████| 3000/3000 [00:45<00:00, 65.43it/s]
🔤 Processing letter 'B' (3000 images)
...
✅ Success! Wrote 87000 samples to keypoints.csv
📊 Processed: 87000 images
❌ Failed: 0 images
📈 Success rate: 100.0%
```

### Step 4: Create Train/Val Splits (~1 minute)

```bash
# Split into training and validation sets
python split_dataset.py
```

**Expected output**:
```
train: (69600, 42) (69600,)
val: (17400, 42) (17400,)
```

### Step 5: Verify Results

```bash
# Check all artifacts were created
./verify_artifacts.sh
```

**Expected output**:
```
🔍 Verifying generated artifacts...
✅ keypoints.csv exists
✅ train.npz exists  
✅ val.npz exists
✅ label_mapping.npy exists

📊 File sizes:
-rw-r--r-- 1 user staff  52M keypoints.csv
-rw-r--r-- 1 user staff  40M train.npz
-rw-r--r-- 1 user staff  10M val.npz
-rw-r--r-- 1 user staff 324B label_mapping.npy

📈 Quick statistics:
📄 keypoints.csv: 87000 samples
🏷️  label_mapping.npy: Contains class names

✅ All artifacts verified successfully!
🎯 Ready for Sprint 5: Model Training!
```

## 🎯 Output Files

| File | Description | Size |
|------|-------------|------|
| `keypoints.csv` | Raw feature data (42 features per sample) | ~50MB |
| `train.npz` | Training set (80% of data) | ~40MB |
| `val.npz` | Validation set (20% of data) | ~10MB |
| `label_mapping.npy` | Class name mapping | <1KB |

## 🚨 Troubleshooting

### "Kaggle API key not found"
- Download `kaggle.json` from https://www.kaggle.com/account
- Place in `~/.kaggle/kaggle.json`
- Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### "No valid samples found"
- Verify dataset structure: `ls data/asl_alphabet_train/`
- Check if images exist: `ls data/asl_alphabet_train/A/ | head -5`

### "Import errors" in IDE
- Restart Cursor/VS Code
- Check `.vscode/settings.json` points to correct Python path

## ✅ Success Criteria

You're ready for Sprint 5 when:
- [ ] All 4 artifact files exist
- [ ] `keypoints.csv` has ~87,000 samples
- [ ] File sizes match expected ranges
- [ ] No error messages in final verification

## 🎉 Next Steps

Once complete, you're ready for **Sprint 5: Model Training**! 