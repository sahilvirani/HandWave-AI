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
        baseOptions: { modelAssetPath: undefined }, // default lite model
        runningMode: 'IMAGE'
      });
    }

    const handLandmarker: HandLandmarker = (window as any).handLandmarker;
    const imageBitmap = await createImageBitmap(ctx.canvas);

    const results: HandLandmarkerResult = handLandmarker.detect(imageBitmap);
    if (results.landmarks.length) {
      console.log('Hands:', results.landmarks);
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
