/* eslint-disable */
// @ts-nocheck
import React, { useCallback, useRef, useState, useEffect } from 'react';
import * as tf from '@tensorflow/tfjs';
import {
  HandLandmarker,
  FilesetResolver,
  HandLandmarkerResult
} from '@mediapipe/tasks-vision';
import WebcamFeed from './components/WebcamFeed';
import HandOverlay from './components/HandOverlay';
import './App.css';

const WIDTH = 640;
const HEIGHT = 480;

// Uncomment for debugging TF.js version
// console.info('TensorFlow.js version:', tf.version.tfjs);

function App() {
  const overlayRef = useRef<HTMLCanvasElement>(null);
  const [model, setModel] = useState<any>(null);
  const [labels, setLabels] = useState<string[]>([]);
  const [prediction, setPrediction] = useState<string>('');
  const [confidence, setConfidence] = useState<number>(0);

  // Load TensorFlow.js model and labels
  useEffect(() => {
    const loadModel = async () => {
      try {
        console.log('Loading TensorFlow.js model...');
        const loadedModel = await tf.loadLayersModel('/model/model.json');
        setModel(loadedModel);
        
        // Load label mapping
        const response = await fetch('/model/label_mapping_20250706-2339.json');
        const labelData = await response.json();
        setLabels(labelData);
        
        console.log('✅ Model and labels loaded successfully');
      } catch (error) {
        console.error('❌ Error loading model:', error);
      }
    };
    
    loadModel();
  }, []);

  // Extract hand landmarks as feature vector
  const extractFeatures = (landmarks: any[]) => {
    if (!landmarks || landmarks.length === 0) return null;
    
    // Use the first hand detected
    const hand = landmarks[0];
    const features = [];
    
    // Extract x, y coordinates for all 21 landmarks (42 features total)
    for (let i = 0; i < 21; i++) {
      if (hand[i]) {
        features.push(hand[i].x, hand[i].y);
      } else {
        features.push(0, 0); // Pad with zeros if landmark missing
      }
    }
    
    return features;
  };

  // Predict ASL letter from landmarks
  const predictASL = async (landmarks: any[]) => {
    if (!model || !labels || landmarks.length === 0) return;
    
    const features = extractFeatures(landmarks);
    if (!features) return;
    
    try {
      // Convert to tensor and predict
      const inputTensor = tf.tensor2d([features]);
      const predictions = await model.predict(inputTensor) as tf.Tensor;
      const probabilities = await predictions.data();
      
      // Find the class with highest probability
      const maxIndex = probabilities.indexOf(Math.max(...probabilities));
      const predictedLabel = labels[maxIndex];
      const confidenceScore = probabilities[maxIndex];
      
      setPrediction(predictedLabel);
      setConfidence(confidenceScore);
      
      // Clean up tensors
      inputTensor.dispose();
      predictions.dispose();
    } catch (error) {
      console.error('Prediction error:', error);
    }
  };

  const handleFrame = useCallback(async (ctx: CanvasRenderingContext2D) => {
    // lazy-init MediaPipe model
    if (!(window as any)._handLm) {
      const fileset = await (FilesetResolver as any).forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
      );
      (window as any)._handLm = await HandLandmarker.createFromOptions(fileset, {
        baseOptions: {
          modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
        },
        runningMode: 'IMAGE',
        numHands: 2
      });
    }
    const handLm: any = (window as any)._handLm;

    // convert the current frame to an ImageBitmap MediaPipe can read
    const bitmap = await createImageBitmap(ctx.canvas);
    const res: any = handLm.detect(bitmap);
    bitmap.close();

    // draw landmarks
    const oCanvas = overlayRef.current;
    if (!oCanvas) return;
    const oCtx = oCanvas.getContext('2d')!;
    oCtx.clearRect(0, 0, WIDTH, HEIGHT);

    (res.landmarks as any[]).forEach((hand: any) => {
      oCtx.fillStyle = '#00FF55';
      hand.forEach(({ x, y }: { x: number; y: number }) => {
        oCtx.beginPath();
        oCtx.arc(x * WIDTH, y * HEIGHT, 4, 0, Math.PI * 2);
        oCtx.fill();
      });
    });

    // Predict ASL letter if model is loaded
    if (res.landmarks && res.landmarks.length > 0) {
      await predictASL(res.landmarks);
    } else {
      setPrediction('');
      setConfidence(0);
    }
  }, [overlayRef, model, labels]);

  return (
    <div className="App" style={{ position: 'relative', width: WIDTH, height: HEIGHT }}>
      <h1>HandWave AI – ASL Recognition</h1>
      <div style={{ marginBottom: '10px' }}>
        <strong>Status:</strong> {model ? '✅ Model Loaded' : '⏳ Loading Model...'}
      </div>
      {prediction && (
        <div style={{ 
          marginBottom: '10px', 
          padding: '10px', 
          backgroundColor: '#f0f0f0', 
          borderRadius: '5px',
          fontSize: '18px',
          fontWeight: 'bold'
        }}>
          <div>Prediction: <span style={{ color: '#0066cc' }}>{prediction}</span></div>
          <div>Confidence: <span style={{ color: '#0066cc' }}>{(confidence * 100).toFixed(1)}%</span></div>
        </div>
      )}
      <WebcamFeed width={WIDTH} height={HEIGHT} onFrame={handleFrame} />
      <HandOverlay ref={overlayRef} width={WIDTH} height={HEIGHT} />
    </div>
  );
}

export default App;
