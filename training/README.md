# HandWave AI - Model Training

## Dataset Layout

The ASL Alphabet dataset must be downloaded and unzipped to the following structure:

```
training/
├── data/
│   └── asl_alphabet_train/
│       ├── A/
│       │   ├── 00001.png
│       │   ├── 00002.png
│       │   └── ...
│       ├── B/
│       │   └── ...
│       ├── C/
│       │   └── ...
│       └── ...
├── requirements.txt
├── extract_keypoints.py
├── split_dataset.py
└── README.md
```

## Dataset Source

Download the ASL Alphabet dataset from Kaggle:
- **Link**: https://www.kaggle.com/datasets/grassknoted/asl-alphabet
- **Size**: ~1.1GB
- **Content**: 29 classes (A-Z letters + space, delete, nothing)

## Usage

### 1. Setup Environment
```bash
# Activate virtual environment
source .venv/bin/activate

# Verify installation
python -c "import mediapipe; print('MediaPipe version:', mediapipe.__version__)"
```

### 2. Process Dataset
```bash
# Extract keypoints from all images (this takes ~10-30 minutes)
python extract_keypoints.py

# Split into train/validation sets
python split_dataset.py
```

### 3. Expected Output
- `keypoints.csv` - Raw feature data with 42 features per sample
- `train.npz` - Training set (80% of data)
- `val.npz` - Validation set (20% of data)
- `label_mapping.npy` - Label encoder mapping

## Notes

- Letters **J** and **Z** are skipped during processing as they require motion
- Each letter folder contains ~3000 images
- Images are 200x200 RGB PNG files
- MediaPipe requires realistic hand images (synthetic test images won't work)
- Processing time depends on your CPU speed and dataset size

## Troubleshooting

### "No valid samples found"
- Check that you have the correct dataset structure
- Verify images are in PNG format
- Ensure hands are clearly visible in the images

### "Dataset directory not found"
- Make sure you've downloaded and extracted the ASL Alphabet dataset
- Check the directory path matches the expected structure 