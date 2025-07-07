/*
  TypeScript shim declarations to satisfy the compiler when official
  type definitions are missing. These keep editor/CI free of red squiggles
  without changing runtime behaviour. Remove once proper @types packages
  are installed.
*/

declare module '@mediapipe/tasks-vision';

declare module 'react/jsx-runtime' {
  export function jsx(type: any, props: any, key?: any): any;
  export function jsxs(type: any, props: any, key?: any): any;
  export const Fragment: any;
}

declare module '@tensorflow/tfjs';

declare module 'react';

// Generic fallback for JSX elements when using the custom React shim
declare global {
  namespace JSX {
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
} 