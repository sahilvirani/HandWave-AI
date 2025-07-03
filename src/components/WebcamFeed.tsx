import React, { useEffect, useRef } from 'react';

type Props = {
  width?: number;
  height?: number;
  onFrame?: (ctx: CanvasRenderingContext2D) => void;
};

const WebcamFeed: React.FC<Props> = ({ width = 640, height = 480, onFrame }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const start = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      const render = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (video && canvas) {
          const ctx = canvas.getContext('2d')!;
          
          // Mirror the image so it feels natural
          ctx.save();
          ctx.scale(-1, 1);
          ctx.translate(-width, 0);
          ctx.drawImage(video, 0, 0, width, height);
          ctx.restore();
          
          onFrame?.(ctx);
        }
        requestAnimationFrame(render);
      };
      render();
    };

    start().catch(console.error);
  }, [onFrame, width, height]);

  return (
    <>
      <video ref={videoRef} style={{ display: 'none' }} />
      <canvas ref={canvasRef} width={width} height={height} />
    </>
  );
};

export default WebcamFeed; 