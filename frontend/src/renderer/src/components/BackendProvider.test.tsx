import { act, cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { type Backend, useBackend } from '../hooks/useBackend'
import { connectBackend } from '../services/backendSocket'
import BackendProvider from './BackendProvider'

vi.mock('../services/backendSocket', () => ({ connectBackend: vi.fn() }))

type Handlers = Parameters<typeof connectBackend>[0]

describe('BackendProvider', () => {
  const send = vi.fn(() => true)
  const close = vi.fn()
  let handlers: Handlers | undefined
  let backend: Backend | undefined

  function Probe(): null {
    backend = useBackend()
    return null
  }

  function setup(): { h: Handlers; unmount: () => void } {
    const { unmount } = render(
      <BackendProvider>
        <Probe />
      </BackendProvider>
    )
    if (!handlers) throw new Error('connectBackend not called')
    return { h: handlers, unmount }
  }

  beforeEach(() => {
    handlers = undefined
    backend = undefined
    vi.mocked(connectBackend).mockImplementation((h) => {
      handlers = h
      return { send, close }
    })
  })
  afterEach(() => {
    cleanup()
    vi.clearAllMocks()
  })

  it('opens one connection and turns messages into state', () => {
    const { h } = setup()
    expect(connectBackend).toHaveBeenCalledTimes(1)
    expect(backend?.connected).toBe(false)

    act(() => {
      h.onStatus(true)
      h.onMessage({ type: 'uv', channels: [true, false, false] })
      h.onMessage({ type: 'scan', state: 'scanning', remaining_s: 4, result: null })
      h.onMessage({ type: 'error', message: 'bad' })
    })
    expect(backend?.connected).toBe(true)
    expect(backend?.uv).toEqual([true, false, false])
    expect(backend?.scan?.remaining_s).toBe(4)
    expect(backend?.error).toBe('bad')
  })

  it('fans frames out to subscribers until they unsubscribe', () => {
    const { h } = setup()
    const listener = vi.fn()
    const unsubscribe = backend?.subscribeFrames(listener)
    const jpeg = new Blob()
    h.onFrame(jpeg)
    unsubscribe?.()
    h.onFrame(jpeg)
    expect(listener).toHaveBeenCalledExactlyOnceWith(jpeg)
  })

  it('keeps send and subscribeFrames stable across state changes', () => {
    const { h } = setup()
    const before = backend
    act(() => h.onStatus(true))
    expect(backend?.send).toBe(before?.send)
    expect(backend?.subscribeFrames).toBe(before?.subscribeFrames)
    expect(backend?.send({ type: 'scan_start' })).toBe(true)
    expect(send).toHaveBeenCalledWith({ type: 'scan_start' })
  })

  it('closes the connection on unmount', () => {
    setup().unmount()
    expect(close).toHaveBeenCalled()
  })
})
