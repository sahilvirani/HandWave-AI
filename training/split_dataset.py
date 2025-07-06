#!/usr/bin/env python
import numpy as np, pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from pathlib import Path

root = Path(__file__).parent
df   = pd.read_csv(root / "keypoints.csv", header=None)
X    = df.iloc[:, :-1].to_numpy(dtype=np.float32)
y    = df.iloc[:,  -1].to_numpy()

le = LabelEncoder()
y_enc = le.fit_transform(y)              # 0-based ints for A…Y (excluding J,Z)

X_train, X_val, y_train, y_val = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

np.savez_compressed(root / "train.npz", X=X_train, y=y_train)
np.savez_compressed(root / "val.npz",   X=X_val, y=y_val)

# keep the label mapping for later
np.save(root / "label_mapping.npy", le.classes_)
print("train:", X_train.shape, "val:", X_val.shape) 