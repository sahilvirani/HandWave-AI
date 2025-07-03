import React, { useCallback } from 'react';
import * as tf from '@tensorflow/tfjs';
import { HandLandmarker, FilesetResolver, HandLandmarkerResult } from '@mediapipe/tasks-vision';
import WebcamFeed from './components/WebcamFeed';
import './App.css';

console.log('TensorFlow.js version:', tf.version.tfjs);

function App() {
  const handleFrame = useCallback(async (ctx: CanvasRenderingContext2D) => {
    // lazy-load the model once
    if (!(window as any).handLandmarker) {
      const fileset = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
      );
      (window as any).handLandmarker = await HandLandmarker.createFromOptions(fileset, {
        baseOptions: { 
          modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/int8/1/hand_landmarker.task'
        },
        runningMode: 'IMAGE',
        numHands: 2
      });
    }

    const handLandmarker: HandLandmarker = (window as any).handLandmarker;
    const bitmap = await createImageBitmap(ctx.canvas);

    const results: HandLandmarkerResult = handLandmarker.detect(bitmap);
    bitmap.close(); // free memory
    
    if (results.landmarks.length) {
      console.log('Hands detected:', results.landmarks.length);
      console.log('Hand landmarks:', results.landmarks);
    }
  }, []);

  return (
    <div className="App">
      <h1>HandWave AI – live demo</h1>
      <WebcamFeed onFrame={handleFrame} />
    </div>
  );
}

export default App;
