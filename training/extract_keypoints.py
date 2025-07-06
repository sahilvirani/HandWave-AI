#!/usr/bin/env python
"""
Generate a CSV with 42 normalised (x,y) coords per image + label column.
Letters J and Z are skipped because they require motion.
"""
import cv2, mediapipe as mp, pandas as pd, numpy as np
from pathlib import Path
from tqdm import tqdm
import sys

ROOT = Path(__file__).parent / "data" / "asl_alphabet_train"
OUT  = Path(__file__).parent / "keypoints.csv"
SKIP = {"J", "Z"}                       # motion letters

# Check if dataset directory exists
if not ROOT.exists():
    print(f"❌ Dataset directory not found: {ROOT}")
    print("\n📥 Please download the ASL Alphabet dataset:")
    print("1. Go to: https://www.kaggle.com/datasets/grassknoted/asl-alphabet")
    print("2. Download and extract the dataset")
    print(f"3. Place the 'asl_alphabet_train' folder in: {ROOT.parent}")
    print("\nExpected structure:")
    print("training/")
    print("├── data/")
    print("│   └── asl_alphabet_train/")
    print("│       ├── A/")
    print("│       ├── B/")
    print("│       └── ...")
    sys.exit(1)

print(f"📁 Found dataset directory: {ROOT}")

mp_hands = mp.solutions.hands
detector = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=0)

rows = []
total_processed = 0
total_failed = 0

IMAGE_EXTS = ["*.png", "*.jpg", "*.jpeg", "*.JPG", "*.JPEG", "*.PNG"]

def get_all_images(letter_dir):
    images = []
    for ext in IMAGE_EXTS:
        images.extend(letter_dir.glob(ext))
    return images

for letter_dir in sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name not in SKIP):
    label = letter_dir.name
    letter_images = get_all_images(letter_dir)
    
    if not letter_images:
        print(f"⚠️  No image files found in {letter_dir}")
        continue
    
    print(f"🔤 Processing letter '{label}' ({len(letter_images)} images)")
    
    for img_path in tqdm(letter_images, desc=f"Letter {label}"):
        img = cv2.imread(str(img_path))
        if img is None:
            total_failed += 1
            continue
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = detector.process(img_rgb)
        
        if not result.multi_hand_landmarks:
            total_failed += 1
            continue

        # take first detected hand
        landmarks = result.multi_hand_landmarks[0].landmark
        xy = np.array([[lm.x, lm.y] for lm in landmarks])  # shape (21,2)

        # simple normalisation: translate so wrist (landmark 0) is origin,
        # then divide by max |coord| so all coords ∈ [-1,1]
        xy -= xy[0]                       # wrist at (0,0)
        max_abs = np.abs(xy).max()
        if max_abs == 0:                  # avoid /0
            total_failed += 1
            continue
        xy /= max_abs

        rows.append(np.concatenate([xy.flatten(), [label]]))
        total_processed += 1

if rows:
    pd.DataFrame(rows).to_csv(OUT, index=False, header=False)
    print(f"\n✅ Success! Wrote {len(rows)} samples to {OUT}")
    print(f"📊 Processed: {total_processed} images")
    print(f"❌ Failed: {total_failed} images")
    print(f"📈 Success rate: {(total_processed/(total_processed+total_failed)*100):.1f}%")
else:
    print("\n❌ No valid samples found! Check your dataset structure.")
    sys.exit(1) 