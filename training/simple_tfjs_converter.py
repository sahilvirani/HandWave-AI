#!/usr/bin/env python
"""Simple TensorFlow.js converter for Keras models.
Usage: python simple_tfjs_converter.py handwave_model_YYYYMMDD-HHMM.h5
"""

import sys
import pathlib
import json
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore

def keras_to_tfjs(model_path, output_dir):
    """Convert Keras H5 model to TensorFlow.js format."""
    model_path = pathlib.Path(model_path)
    output_dir = pathlib.Path(output_dir)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract model architecture
    config = model.get_config()
    
    # Get all weights
    weights = model.get_weights()
    
    # Create weight manifest
    weight_specs = []
    weight_data = []
    
    for i, weight in enumerate(weights):
        weight_specs.append({
            "name": f"weight_{i}",
            "shape": list(weight.shape),
            "dtype": "float32"
        })
        weight_data.append(weight.flatten().astype(np.float32))
    
    # Concatenate all weights
    all_weights = np.concatenate(weight_data) if weight_data else np.array([], dtype=np.float32)
    
    # Create model.json
    model_json = {
        "format": "layers-model",
        "generatedBy": "HandWave-AI tfjs-converter",
        "convertedBy": "TensorFlow.js 3.21.0",
        "modelTopology": {
            "keras_version": "2.12.0",
            "backend": "tensorflow",
            "model_config": config
        },
        "weightsManifest": [
            {
                "paths": ["group1-shard1of1.bin"],
                "weights": weight_specs
            }
        ]
    }
    
    # Save files
    model_json_path = output_dir / "model.json"
    weights_path = output_dir / "group1-shard1of1.bin"
    
    # Write model.json
    with open(model_json_path, 'w') as f:
        json.dump(model_json, f, indent=2)
    
    # Write weights binary
    with open(weights_path, 'wb') as f:
        f.write(all_weights.tobytes())
    
    print(f"✅ Conversion complete!")
    print(f"   - Model JSON: {model_json_path} ({model_json_path.stat().st_size:,} bytes)")
    print(f"   - Weights: {weights_path} ({weights_path.stat().st_size:,} bytes)")
    
    return output_dir

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python simple_tfjs_converter.py handwave_model_YYYYMMDD-HHMM.h5")
        sys.exit(1)
    
    h5_file = sys.argv[1]
    output_dir = pathlib.Path("training/tfjs_model")
    
    try:
        keras_to_tfjs(h5_file, output_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 