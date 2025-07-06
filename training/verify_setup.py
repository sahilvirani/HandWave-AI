#!/usr/bin/env python
"""
Verify that all dependencies are installed and working correctly.
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe: {mp.__version__}")
    except ImportError as e:
        print(f"❌ MediaPipe import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ Pandas: {pd.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn: {sklearn.__version__}")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import tqdm
        print(f"✅ tqdm: {tqdm.__version__}")
    except ImportError as e:
        print(f"❌ tqdm import failed: {e}")
        return False
    
    return True

def test_mediapipe_hands():
    """Test MediaPipe Hands initialization."""
    print("\n🤖 Testing MediaPipe Hands...")
    
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        detector = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            model_complexity=0
        )
        print("✅ MediaPipe Hands initialized successfully")
        return True
    except Exception as e:
        print(f"❌ MediaPipe Hands initialization failed: {e}")
        return False

def check_scripts():
    """Check that required scripts exist."""
    print("\n📄 Checking script files...")
    
    scripts = ['extract_keypoints.py', 'split_dataset.py']
    all_exist = True
    
    for script in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} not found")
            all_exist = False
    
    return all_exist

def main():
    print("🚀 HandWave AI - Training Setup Verification")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test MediaPipe
    mediapipe_ok = test_mediapipe_hands()
    
    # Check scripts
    scripts_ok = check_scripts()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if imports_ok and mediapipe_ok and scripts_ok:
        print("✅ All tests passed! Setup is ready for Sprint 5.")
        print("\n📥 Next steps:")
        print("1. Download ASL Alphabet dataset from Kaggle")
        print("2. Extract to training/data/asl_alphabet_train/")
        print("3. Run: python extract_keypoints.py")
        print("4. Run: python split_dataset.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 