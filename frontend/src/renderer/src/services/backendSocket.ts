// WebSocket to the backend. Contract: systems/api.md
export const BACKEND_WS_URL = 'ws://localhost:8000/ws'
const RETRY_MS = 1000

type Handlers = {
  onFrame: (jpeg: Blob) => void
  onStatus: (connected: boolean) => void
}

/**
 * Keeps one WebSocket to the backend open and reconnects every second when it drops.
 * Returns a function that closes it for good (the backend then turns every UV channel off).
 */
export function connectBackend({ onFrame, onStatus }: Handlers): () => void {
  let ws: WebSocket | null = null
  let retry: ReturnType<typeof setTimeout> | undefined
  let closed = false

  const open = (): void => {
    ws = new WebSocket(BACKEND_WS_URL)
    ws.binaryType = 'blob'
    ws.onopen = () => onStatus(true)
    ws.onmessage = (e) => {
      if (e.data instanceof Blob) onFrame(e.data) // text messages (uv, error) are not used yet
    }
    ws.onclose = () => {
      onStatus(false)
      if (!closed) retry = setTimeout(open, RETRY_MS)
    }
  }

  open()
  return () => {
    closed = true
    clearTimeout(retry)
    ws?.close()
  }
}
