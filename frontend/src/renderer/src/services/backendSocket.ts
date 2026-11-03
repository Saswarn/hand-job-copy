// WebSocket to the backend. Contract: systems/api.md
import {
  BACKEND_WS_URL,
  type ClientMessage,
  parseServerMessage,
  type ServerMessage
} from '../common/api'

const RETRY_MS = 1000

type Handlers = {
  onFrame: (jpeg: Blob) => void
  onMessage: (msg: ServerMessage) => void
  onStatus: (connected: boolean) => void
}

export type BackendConnection = {
  /** Sends a message; returns false (message dropped) while disconnected. */
  send: (msg: ClientMessage) => boolean
  /** Closes for good (the backend then turns every UV channel off). */
  close: () => void
}

/** Keeps one WebSocket to the backend open and reconnects every second when it drops. */
export function connectBackend({ onFrame, onMessage, onStatus }: Handlers): BackendConnection {
  let ws: WebSocket | null = null
  let retry: ReturnType<typeof setTimeout> | undefined
  let closed = false

  const open = (): void => {
    ws = new WebSocket(BACKEND_WS_URL)
    ws.binaryType = 'blob'
    ws.onopen = () => onStatus(true)
    ws.onmessage = (e: MessageEvent<unknown>) => {
      if (e.data instanceof Blob) return onFrame(e.data)
      const msg = typeof e.data === 'string' ? parseServerMessage(e.data) : null
      if (msg) onMessage(msg)
      else console.warn('unknown message from backend', e.data)
    }
    ws.onclose = () => {
      onStatus(false)
      if (!closed) retry = setTimeout(open, RETRY_MS)
    }
  }

  open()
  return {
    send: (msg) => {
      if (ws?.readyState !== WebSocket.OPEN) return false
      ws.send(JSON.stringify(msg))
      return true
    },
    close: () => {
      closed = true
      clearTimeout(retry)
      ws?.close()
    }
  }
}
