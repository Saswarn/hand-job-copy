import { useRef } from 'react'
import { useNavigate } from 'react-router'
import { ROUTES } from '../common/routes'

const HOLD_MS = 3000

/** Invisible top-right corner: hold 3 s to open Settings / Debug (no PIN). A short tap does nothing. */
export default function LongPressCorner(): React.JSX.Element {
  const navigate = useNavigate()
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)

  const start = (): void => {
    timer.current = setTimeout(() => navigate(ROUTES.settings), HOLD_MS)
  }
  const cancel = (): void => clearTimeout(timer.current)

  return (
    <div
      aria-hidden="true"
      className="fixed top-0 right-0 z-50 h-24 w-24"
      onPointerDown={start}
      onPointerUp={cancel}
      onPointerLeave={cancel}
      onPointerCancel={cancel}
      onClick={(e) => e.stopPropagation()}
    />
  )
}
