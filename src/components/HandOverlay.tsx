// @ts-nocheck
import React, { forwardRef } from 'react';

interface Props {
  width: number;
  height: number;
}

const HandOverlay = forwardRef<HTMLCanvasElement, Props>(function HandOverlay({ width, height }, ref) {
  return (
    <canvas
      ref={ref}
      width={width}
      height={height}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        pointerEvents: 'none' // allow clicks through
      }}
    />
  );
});

HandOverlay.displayName = 'HandOverlay';

export default HandOverlay; 