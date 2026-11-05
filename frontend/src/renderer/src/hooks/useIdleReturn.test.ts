import { act, cleanup, fireEvent, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ROUTES } from '../common/routes'
import { useIdleReturn } from './useIdleReturn'

const { navigate } = vi.hoisted(() => ({ navigate: vi.fn() }))
vi.mock('react-router', () => ({ useNavigate: () => navigate }))

describe('useIdleReturn', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    navigate.mockClear()
  })

  afterEach(() => {
    cleanup()
    vi.useRealTimers()
  })

  it('returns to the tutorial once after 5 seconds', () => {
    renderHook(() => useIdleReturn(5_000))

    act(() => vi.advanceTimersByTime(5_000))
    expect(navigate).toHaveBeenCalledExactlyOnceWith(ROUTES.tutorial)

    act(() => vi.advanceTimersByTime(5_000))
    expect(navigate).toHaveBeenCalledTimes(1)
  })

  it('restarts the timeout when the screen is touched', () => {
    renderHook(() => useIdleReturn(5_000))

    act(() => vi.advanceTimersByTime(4_000))
    fireEvent.pointerDown(window)
    act(() => vi.advanceTimersByTime(1000))
    expect(navigate).not.toHaveBeenCalled()

    act(() => vi.advanceTimersByTime(4_000))
    expect(navigate).toHaveBeenCalledExactlyOnceWith(ROUTES.tutorial)
  })

  it('cleans up the timer and listener on unmount', () => {
    const { unmount } = renderHook(() => useIdleReturn(5_000))

    unmount()
    fireEvent.pointerDown(window)
    act(() => vi.advanceTimersByTime(5_000))
    expect(navigate).not.toHaveBeenCalled()
  })
})
