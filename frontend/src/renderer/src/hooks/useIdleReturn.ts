import { useEffect } from 'react'
import { useNavigate } from 'react-router'
import { ROUTES } from '../common/routes'

export function useIdleReturn(ms: number): void {
  const navigate = useNavigate()

  useEffect(() => {
    let timer: number
    const resetTimer = (): void => {
      window.clearTimeout(timer)
      timer = window.setTimeout(() => void navigate(ROUTES.tutorial), ms)
    }

    resetTimer()
    window.addEventListener('pointerdown', resetTimer, true)

    return () => {
      window.removeEventListener('pointerdown', resetTimer, true)
      window.clearTimeout(timer)
    }
  }, [ms, navigate])
}
