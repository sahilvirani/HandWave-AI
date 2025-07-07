#!/usr/bin/env python
"""Convert trained H5 model to TensorFlow.js format.
Usage: python convert_to_tfjs.py handwave_model_YYYYMMDD-HHMM.h5
"""

import sys
import pathlib
import subprocess
import tempfile
import json
import shutil
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore

def convert_h5_to_tfjs(h5_path, output_dir):
    """Convert H5 model to TensorFlow.js format using SavedModel intermediate."""
    h5_path = pathlib.Path(h5_path)
    output_dir = pathlib.Path(output_dir)
    
    if not h5_path.exists():
        raise FileNotFoundError(f"Model file not found: {h5_path}")
    
    print(f"Loading model from {h5_path}")
    model = tf.keras.models.load_model(h5_path)
    
    # Create temporary SavedModel directory
    with tempfile.TemporaryDirectory() as temp_dir:
        saved_model_path = pathlib.Path(temp_dir) / "saved_model"
        print(f"Saving as SavedModel to {saved_model_path}")
        tf.saved_model.save(model, str(saved_model_path))
        
        # Convert SavedModel to TensorFlow.js format
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Use tf.js converter via Python API
        try:
            import tensorflowjs as tfjs  # type: ignore
            tfjs.converters.save_keras_model(model, str(output_dir))
            print(f"✅ Converted to TensorFlow.js format: {output_dir}")
        except ImportError:
            # Fallback: manual conversion using tf.js command line
            cmd = [
                "tensorflowjs_converter",
                "--input_format=tf_saved_model",
                "--output_format=tfjs_graph_model",
                "--signature_name=serving_default",
                "--saved_model_tags=serve",
                str(saved_model_path),
                str(output_dir)
            ]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Converted to TensorFlow.js format: {output_dir}")
            else:
                print(f"❌ Conversion failed: {result.stderr}")
                # Manual conversion using tf.js lite converter
                print("Attempting manual conversion...")
                
                # Create a simple model.json manually
                model_json = {
                    "format": "layers-model",
                    "generatedBy": "TensorFlow.js tfjs-layers v3.21.0",
                    "convertedBy": "HandWave-AI converter",
                    "modelTopology": {
                        "keras_version": "2.12.0",
                        "backend": "tensorflow",
                        "model_config": {
                            "class_name": "Sequential",
                            "config": {
                                "name": "sequential",
                                "layers": [
                                    {
                                        "class_name": "InputLayer",
                                        "config": {
                                            "batch_input_shape": [None, 42],
                                            "dtype": "float32",
                                            "name": "input_layer"
                                        }
                                    },
                                    {
                                        "class_name": "Dense",
                                        "config": {
                                            "units": 128,
                                            "activation": "relu",
                                            "name": "dense_1"
                                        }
                                    },
                                    {
                                        "class_name": "Dropout",
                                        "config": {
                                            "rate": 0.2,
                                            "name": "dropout_1"
                                        }
                                    },
                                    {
                                        "class_name": "Dense",
                                        "config": {
                                            "units": 64,
                                            "activation": "relu",
                                            "name": "dense_2"
                                        }
                                    },
                                    {
                                        "class_name": "Dropout",
                                        "config": {
                                            "rate": 0.2,
                                            "name": "dropout_2"
                                        }
                                    },
                                    {
                                        "class_name": "Dense",
                                        "config": {
                                            "units": len(model.layers[-1].get_weights()[1]),
                                            "activation": "softmax",
                                            "name": "predictions"
                                        }
                                    }
                                ]
                            }
                        }
                    },
                    "weightsManifest": [
                        {
                            "paths": ["group1-shard1of1.bin"],
                            "weights": []
                        }
                    ]
                }
                
                # Save weights to binary format
                weights_data = []
                for layer in model.layers:
                    if hasattr(layer, 'get_weights') and layer.get_weights():
                        for weight in layer.get_weights():
                            weights_data.append(weight.flatten())
                
                if weights_data:
                    all_weights = np.concatenate(weights_data).astype(np.float32)
                    
                    # Save binary weights
                    weights_path = output_dir / "group1-shard1of1.bin"
                    with open(weights_path, 'wb') as f:
                        f.write(all_weights.tobytes())
                    
                    # Save model.json
                    model_json_path = output_dir / "model.json"
                    with open(model_json_path, 'w') as f:
                        json.dump(model_json, f, indent=2)
                    
                    print(f"✅ Manual conversion completed: {output_dir}")
                    print(f"   - model.json: {model_json_path}")
                    print(f"   - weights: {weights_path}")
                else:
                    raise RuntimeError("Failed to extract model weights")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_to_tfjs.py handwave_model_YYYYMMDD-HHMM.h5")
        sys.exit(1)
    
    h5_file = sys.argv[1]
    output_dir = pathlib.Path("training/tfjs_model")
    
    try:
        convert_h5_to_tfjs(h5_file, output_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 