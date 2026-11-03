import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { BACKEND_WS_URL } from '../common/api'
import { connectBackend } from './backendSocket'

/** Stand-in for the browser WebSocket: tests fire the events by hand. */
class FakeSocket {
  static readonly OPEN = 1
  static all: FakeSocket[] = []
  binaryType = ''
  readyState = 0
  onopen: (() => void) | null = null
  onmessage: ((e: { data: unknown }) => void) | null = null
  onclose: (() => void) | null = null
  send = vi.fn()
  close = vi.fn(() => this.onclose?.())

  constructor(readonly url: string) {
    FakeSocket.all.push(this)
  }

  open(): void {
    this.readyState = FakeSocket.OPEN
    this.onopen?.()
  }
}

function latest(): FakeSocket {
  const ws = FakeSocket.all.at(-1)
  if (!ws) throw new Error('no socket opened')
  return ws
}

const handlers = (): Parameters<typeof connectBackend>[0] => ({
  onFrame: vi.fn(),
  onMessage: vi.fn(),
  onStatus: vi.fn()
})

describe('connectBackend', () => {
  beforeEach(() => {
    FakeSocket.all = []
    vi.useFakeTimers()
    vi.stubGlobal('WebSocket', FakeSocket)
    vi.spyOn(console, 'warn').mockImplementation(() => {})
  })
  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('reports status, passes frames and parsed messages on', () => {
    const h = handlers()
    connectBackend(h)
    const ws = latest()
    expect(ws.url).toBe(BACKEND_WS_URL)
    expect(ws.binaryType).toBe('blob')

    ws.open()
    expect(h.onStatus).toHaveBeenLastCalledWith(true)

    const jpeg = new Blob([new Uint8Array([0xff, 0xd8])])
    ws.onmessage?.({ data: jpeg })
    ws.onmessage?.({ data: '{"type":"uv","channels":[false,true,false]}' })
    ws.onmessage?.({ data: '{"type":"nope"}' })
    expect(h.onFrame).toHaveBeenCalledExactlyOnceWith(jpeg)
    expect(h.onMessage).toHaveBeenCalledExactlyOnceWith({
      type: 'uv',
      channels: [false, true, false]
    })
  })

  it('sends JSON only while open', () => {
    const conn = connectBackend(handlers())
    expect(conn.send({ type: 'scan_start' })).toBe(false)
    latest().open()
    expect(conn.send({ type: 'uv_set', channel: 1, on: true })).toBe(true)
    expect(latest().send).toHaveBeenCalledWith('{"type":"uv_set","channel":1,"on":true}')
  })

  it('reconnects 1 s after the socket drops', () => {
    const h = handlers()
    connectBackend(h)
    latest().onclose?.()
    expect(h.onStatus).toHaveBeenLastCalledWith(false)

    vi.advanceTimersByTime(999)
    expect(FakeSocket.all).toHaveLength(1)
    vi.advanceTimersByTime(1)
    expect(FakeSocket.all).toHaveLength(2)
  })

  it('stops reconnecting once closed', () => {
    const conn = connectBackend(handlers())
    const ws = latest()
    conn.close()
    expect(ws.close).toHaveBeenCalled()
    vi.advanceTimersByTime(5000)
    expect(FakeSocket.all).toHaveLength(1)
  })
})
