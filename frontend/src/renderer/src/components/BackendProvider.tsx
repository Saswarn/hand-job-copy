import { type ReactNode, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { ClientMessage, ScanState, ServerMessage } from '../common/api'
import { type Backend, BackendContext, type FrameListener } from '../hooks/useBackend'
import { type BackendConnection, connectBackend } from '../services/backendSocket'

/**
 * One WebSocket for the whole app (mounted once in App.tsx). Text messages become React state;
 * frames go straight to subscribers. Unmounting closes it, and the backend turns UV off.
 */
export default function BackendProvider({ children }: { children: ReactNode }): React.JSX.Element {
  const [connected, setConnected] = useState(false)
  const [uv, setUv] = useState<boolean[] | null>(null)
  const [scan, setScan] = useState<ScanState | null>(null)
  const [error, setError] = useState<string | null>(null)
  const connection = useRef<BackendConnection | null>(null)
  const frameListeners = useRef(new Set<FrameListener>())

  useEffect(() => {
    const onMessage = (msg: ServerMessage): void => {
      if (msg.type === 'uv') setUv(msg.channels)
      else if (msg.type === 'scan') setScan(msg)
      else setError(msg.message)
    }
    const conn = connectBackend({
      onFrame: (jpeg) => frameListeners.current.forEach((listen) => listen(jpeg)),
      onMessage,
      onStatus: setConnected
    })
    connection.current = conn
    return () => {
      conn.close()
      connection.current = null
    }
  }, [])

  // Stable identities, so effects that use them do not re-run on every state change.
  const send = useCallback((msg: ClientMessage) => connection.current?.send(msg) ?? false, [])
  const subscribeFrames = useCallback((listener: FrameListener) => {
    frameListeners.current.add(listener)
    return () => {
      frameListeners.current.delete(listener)
    }
  }, [])

  const value = useMemo<Backend>(
    () => ({ connected, uv, scan, error, send, subscribeFrames }),
    [connected, uv, scan, error, send, subscribeFrames]
  )

  return <BackendContext.Provider value={value}>{children}</BackendContext.Provider>
}
