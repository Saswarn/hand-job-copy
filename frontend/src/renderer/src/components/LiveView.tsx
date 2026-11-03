import { useRef } from 'react'
import { useLiveFrames } from '../hooks/useLiveFrames'
import ConnectingOverlay from './ConnectingOverlay'

/** Live camera view from the backend, scaled to fit its box. Shows "กำลังเชื่อมต่อ…" while disconnected. */
export default function LiveView(): React.JSX.Element {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const connected = useLiveFrames(canvasRef)

  return (
    <div className="relative h-full w-full bg-black">
      <canvas ref={canvasRef} className="h-full w-full object-contain" />
      {connected ? null : <ConnectingOverlay />}
    </div>
  )
}
