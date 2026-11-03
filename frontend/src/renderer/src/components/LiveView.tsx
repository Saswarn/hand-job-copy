import { useRef } from 'react'
import { useLiveFrames } from '../hooks/useLiveFrames'

/** Live camera view from the backend (crop and AI boxes already drawn), scaled to fit its box. */
export default function LiveView(): React.JSX.Element {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  useLiveFrames(canvasRef)
  return <canvas ref={canvasRef} className="h-full w-full bg-surface object-contain" />
}
