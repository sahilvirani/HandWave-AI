#!/usr/bin/env python
"""Train a simple dense neural network on ASL hand-keypoint features.
Outputs a timestamped .h5 model and the accompanying label mapping JSON.
Run: python train_model.py
"""

import datetime
import json
import pathlib
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore
from tensorflow import keras  # type: ignore
from tensorflow.keras import layers  # type: ignore

root = pathlib.Path(__file__).parent

# Load data
with np.load(root / "train.npz") as data:
    X_train, y_train = data["X"], data["y"]
with np.load(root / "val.npz") as data:
    X_val, y_val = data["X"], data["y"]
classes = np.load(root / "label_mapping.npy", allow_pickle=True)
num_classes = len(classes)

# Build model
model = keras.Sequential(
    [
        layers.Input(shape=(42,)),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

# Compile model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

# Train model
print("Starting training...")
history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=256,
    validation_data=(X_val, y_val),
    verbose=1,
)

# Save model and label mapping with timestamp
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
model_path = root / f"handwave_model_{stamp}.h5"
label_path = root / f"label_mapping_{stamp}.json"

model.save(model_path)
with open(label_path, "w") as f:
    json.dump(classes.tolist(), f)

print(f"✅ Saved model & label map: {stamp}")
print(f"Model: {model_path}")
print(f"Labels: {label_path}")

# Print final validation accuracy
final_val_acc = history.history["val_accuracy"][-1]
print(f"Final validation accuracy: {final_val_acc:.1%}") 