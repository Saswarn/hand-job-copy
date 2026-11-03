import { useBackend } from '../hooks/useBackend'

/** Covers every page while the backend is unreachable (it reconnects by itself). Below LongPressCorner. */
export default function ConnectingOverlay(): React.JSX.Element | null {
  const { connected } = useBackend()
  if (connected) return null
  return (
    <div
      className="fixed inset-0 z-40 flex items-center justify-center bg-surface/80"
      role="status"
    >
      <p className="text-title font-bold">กำลังเชื่อมต่อ…</p>
    </div>
  )
}
