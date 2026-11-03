import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ROUTES } from '../common/routes'
import LongPressCorner from './LongPressCorner'

function renderAt(path: string, onPageClick = vi.fn()): HTMLElement {
  const { container } = render(
    <MemoryRouter initialEntries={[path]}>
      <div onClick={onPageClick}>
        <Routes>
          <Route path={ROUTES.detection} element={<p>detection</p>} />
          <Route path={ROUTES.settings} element={<p>settings</p>} />
        </Routes>
        <LongPressCorner />
      </div>
    </MemoryRouter>
  )
  const corner = container.querySelector('[aria-hidden="true"]')
  if (!(corner instanceof HTMLElement)) throw new Error('corner not rendered')
  return corner
}

describe('LongPressCorner', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => {
    cleanup()
    vi.useRealTimers()
  })

  it('opens Settings after a 3 s hold', () => {
    const corner = renderAt(ROUTES.detection)
    fireEvent.pointerDown(corner)
    act(() => vi.advanceTimersByTime(2999))
    expect(screen.getByText('detection')).toBeTruthy()
    act(() => vi.advanceTimersByTime(1))
    expect(screen.getByText('settings')).toBeTruthy()
  })

  it('does nothing when released early', () => {
    const corner = renderAt(ROUTES.detection)
    fireEvent.pointerDown(corner)
    act(() => vi.advanceTimersByTime(1000))
    fireEvent.pointerUp(corner)
    act(() => vi.advanceTimersByTime(5000))
    expect(screen.getByText('detection')).toBeTruthy()
  })

  it('does not pass taps to the page underneath', () => {
    const onPageClick = vi.fn()
    fireEvent.click(renderAt(ROUTES.detection, onPageClick))
    expect(onPageClick).not.toHaveBeenCalled()
  })
})
