import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { connectBackend } from '../services/backendSocket'
import { useLiveFrames } from './useLiveFrames'

vi.mock('../services/backendSocket', () => ({ connectBackend: vi.fn() }))

type Handlers = Parameters<typeof connectBackend>[0]

/** createImageBitmap stub whose decodes finish only when the test says so. */
function controllableDecodes(): Array<(width: number) => ImageBitmap> {
  const resolvers: Array<(width: number) => ImageBitmap> = []
  vi.stubGlobal(
    'createImageBitmap',
    () =>
      new Promise<ImageBitmap>((resolve) => {
        resolvers.push((width) => {
          const bitmap = { width, height: 10, close: vi.fn() } as unknown as ImageBitmap
          resolve(bitmap)
          return bitmap
        })
      })
  )
  return resolvers
}

describe('useLiveFrames', () => {
  const drawImage = vi.fn()
  const closeSocket = vi.fn()
  let handlers: Handlers | undefined

  beforeEach(() => {
    handlers = undefined
    vi.mocked(connectBackend).mockImplementation((h) => {
      handlers = h
      return closeSocket
    })
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue({
      drawImage
    } as unknown as CanvasRenderingContext2D)
    vi.stubGlobal('requestAnimationFrame', (cb: FrameRequestCallback) => {
      cb(0)
      return 1
    })
  })
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
    drawImage.mockClear()
    closeSocket.mockClear()
  })

  function setup(): {
    result: { current: boolean }
    canvas: HTMLCanvasElement
    unmount: () => void
  } {
    const canvas = document.createElement('canvas')
    const { result, unmount } = renderHook(() => useLiveFrames({ current: canvas }))
    return { result, canvas, unmount }
  }

  function connected(): Handlers {
    if (!handlers) throw new Error('connectBackend not called')
    return handlers
  }

  it('follows the socket status', () => {
    const { result } = setup()
    expect(result.current).toBe(false)
    act(() => connected().onStatus(true))
    expect(result.current).toBe(true)
  })

  it('draws the newest frame and drops one that finishes decoding late', async () => {
    const decodes = controllableDecodes()
    const { canvas } = setup()
    connected().onFrame(new Blob())
    connected().onFrame(new Blob())

    const newer = await act(async () => decodes[1]?.(20))
    const older = await act(async () => decodes[0]?.(10))

    expect(drawImage).toHaveBeenCalledTimes(1)
    expect(drawImage).toHaveBeenCalledWith(newer, 0, 0)
    expect(canvas.width).toBe(20) // canvas follows the frame size
    expect(older?.close).toHaveBeenCalled()
    expect(newer?.close).toHaveBeenCalled() // closed right after drawing
  })

  it('closes the socket on unmount', () => {
    const { unmount } = setup()
    unmount()
    expect(closeSocket).toHaveBeenCalled()
  })
})
