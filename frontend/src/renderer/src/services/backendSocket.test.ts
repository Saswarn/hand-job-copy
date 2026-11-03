import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { BACKEND_WS_URL, connectBackend } from './backendSocket'

/** Stand-in for the browser WebSocket: tests fire the events by hand. */
class FakeSocket {
  static all: FakeSocket[] = []
  binaryType = ''
  onopen: (() => void) | null = null
  onmessage: ((e: { data: unknown }) => void) | null = null
  onclose: (() => void) | null = null
  close = vi.fn(() => this.onclose?.())

  constructor(readonly url: string) {
    FakeSocket.all.push(this)
  }
}

function latest(): FakeSocket {
  const ws = FakeSocket.all.at(-1)
  if (!ws) throw new Error('no socket opened')
  return ws
}

describe('connectBackend', () => {
  beforeEach(() => {
    FakeSocket.all = []
    vi.useFakeTimers()
    vi.stubGlobal('WebSocket', FakeSocket)
  })
  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  it('reports status and passes only binary frames on', () => {
    const onFrame = vi.fn()
    const onStatus = vi.fn()
    connectBackend({ onFrame, onStatus })
    const ws = latest()
    expect(ws.url).toBe(BACKEND_WS_URL)
    expect(ws.binaryType).toBe('blob')

    ws.onopen?.()
    expect(onStatus).toHaveBeenLastCalledWith(true)

    const jpeg = new Blob([new Uint8Array([0xff, 0xd8])])
    ws.onmessage?.({ data: jpeg })
    ws.onmessage?.({ data: '{"type":"uv","channels":[false,false,false]}' })
    expect(onFrame).toHaveBeenCalledTimes(1)
    expect(onFrame).toHaveBeenCalledWith(jpeg)
  })

  it('reconnects 1 s after the socket drops', () => {
    const onStatus = vi.fn()
    connectBackend({ onFrame: vi.fn(), onStatus })
    latest().onclose?.()
    expect(onStatus).toHaveBeenLastCalledWith(false)

    vi.advanceTimersByTime(999)
    expect(FakeSocket.all).toHaveLength(1)
    vi.advanceTimersByTime(1)
    expect(FakeSocket.all).toHaveLength(2)
  })

  it('stops reconnecting once closed', () => {
    const close = connectBackend({ onFrame: vi.fn(), onStatus: vi.fn() })
    const ws = latest()
    close()
    expect(ws.close).toHaveBeenCalled()
    vi.advanceTimersByTime(5000)
    expect(FakeSocket.all).toHaveLength(1)
  })
})
