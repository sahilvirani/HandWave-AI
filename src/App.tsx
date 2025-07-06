import React, { useCallback, useRef } from 'react';
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

console.log('TensorFlow.js version:', tf.version.tfjs);

function App() {
  const overlayRef = useRef<HTMLCanvasElement>(null);

  const handleFrame = useCallback(async (ctx: CanvasRenderingContext2D) => {
    // lazy-init MediaPipe model
    if (!(window as any)._handLm) {
      const fileset = await FilesetResolver.forVisionTasks(
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
    const handLm: HandLandmarker = (window as any)._handLm;

    // convert the current frame to an ImageBitmap MediaPipe can read
    const bitmap = await createImageBitmap(ctx.canvas);
    const res: HandLandmarkerResult = handLm.detect(bitmap);
    bitmap.close();

    // draw landmarks
    const oCanvas = overlayRef.current;
    if (!oCanvas) return;
    const oCtx = oCanvas.getContext('2d')!;
    oCtx.clearRect(0, 0, WIDTH, HEIGHT);

    res.landmarks.forEach((hand) => {
      oCtx.fillStyle = '#00FF55';
      hand.forEach(({ x, y }) => {
        oCtx.beginPath();
        oCtx.arc(x * WIDTH, y * HEIGHT, 4, 0, Math.PI * 2);
        oCtx.fill();
      });
    });
  }, []);

  return (
    <div className="App" style={{ position: 'relative', width: WIDTH, height: HEIGHT }}>
      <h1>HandWave AI – Hand Landmarks</h1>
      <WebcamFeed width={WIDTH} height={HEIGHT} onFrame={handleFrame} />
      <HandOverlay ref={overlayRef} width={WIDTH} height={HEIGHT} />
    </div>
  );
}

export default App;
