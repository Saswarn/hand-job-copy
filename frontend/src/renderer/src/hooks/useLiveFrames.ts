import { type RefObject, useEffect, useState } from 'react'
import { connectBackend } from '../services/backendSocket'

/**
 * Draws the backend's live JPEG frames (boxes already drawn by the backend) onto `canvasRef`.
 * Frames stay out of React state: decode off the main thread, keep only the newest bitmap,
 * draw once per animation frame. Returns whether the backend is connected.
 */
export function useLiveFrames(canvasRef: RefObject<HTMLCanvasElement | null>): boolean {
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas?.getContext('2d')
    if (!canvas || !ctx) return

    let pending: ImageBitmap | null = null
    let raf = 0
    let received = 0
    let shown = 0
    let disposed = false

    const draw = (): void => {
      raf = 0
      if (!pending) return
      if (canvas.width !== pending.width || canvas.height !== pending.height) {
        canvas.width = pending.width
        canvas.height = pending.height
      }
      ctx.drawImage(pending, 0, 0)
      pending.close()
      pending = null
    }

    const onFrame = async (jpeg: Blob): Promise<void> => {
      const seq = ++received
      let bitmap: ImageBitmap
      try {
        bitmap = await createImageBitmap(jpeg)
      } catch {
        return // corrupt frame: skip it
      }
      if (disposed || seq < shown) {
        bitmap.close() // an older frame finished decoding after a newer one
        return
      }
      shown = seq
      pending?.close()
      pending = bitmap
      if (!raf) raf = requestAnimationFrame(draw)
    }

    const close = connectBackend({ onFrame, onStatus: setConnected })
    return () => {
      disposed = true
      close()
      cancelAnimationFrame(raf)
      pending?.close()
    }
  }, [canvasRef])

  return connected
}
