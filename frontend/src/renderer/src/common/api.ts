// Backend contract, mirrored by hand from backend/app/schemas/ws.py and backend/app/core/config.py.
// Source of truth: systems/api.md. Change both sides (and api.md) in the same PR.

export const BACKEND_HTTP_URL = 'http://localhost:8000'
export const BACKEND_WS_URL = 'ws://localhost:8000/ws'

/** UV channel index 0-2, in the order of uv_gpio. */
export type UvChannel = 0 | 1 | 2

// frontend -> backend (text)
export type ClientMessage =
  | { type: 'uv_set'; channel: UvChannel; on: boolean }
  | { type: 'scan_start' }
  | { type: 'binary_view'; on: boolean }

// backend -> frontend (text)
export type UvState = { type: 'uv'; channels: boolean[] }
export type ScanState = {
  type: 'scan'
  state: 'idle' | 'scanning' | 'done'
  remaining_s: number | null
  result: 'clean' | 'dirt' | null
}
export type ErrorMessage = { type: 'error'; message: string }
export type ServerMessage = UvState | ScanState | ErrorMessage

const isObject = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null

/** Parses one text message from /ws. Returns null for anything that is not a known, well-formed message. */
export function parseServerMessage(text: string): ServerMessage | null {
  let data: unknown
  try {
    data = JSON.parse(text)
  } catch {
    return null
  }
  if (!isObject(data)) return null
  switch (data.type) {
    case 'uv':
      return Array.isArray(data.channels) && data.channels.every((c) => typeof c === 'boolean')
        ? { type: 'uv', channels: data.channels }
        : null
    case 'scan':
      return (data.state === 'idle' || data.state === 'scanning' || data.state === 'done') &&
        (data.remaining_s === null || typeof data.remaining_s === 'number') &&
        (data.result === null || data.result === 'clean' || data.result === 'dirt')
        ? { type: 'scan', state: data.state, remaining_s: data.remaining_s, result: data.result }
        : null
    case 'error':
      return typeof data.message === 'string' ? { type: 'error', message: data.message } : null
    default:
      return null
  }
}

// GET /config -> AppConfig · PUT /config <- AppConfig (204, or 422 on bad values; 501 until saving lands)
export type AppConfig = {
  uv_gpio: [number, number, number]
  camera: {
    device: string
    capture: { width: number; height: number; fps: number }
    exposure: number
    gain: number
    white_balance: number
    zoom: number
    crop: [number, number, number, number] // [x1, y1, x2, y2], 0-1 of the camera frame
  }
  binary_threshold: number
  stream: { min_width: number; quality: number }
  scan_seconds: number
  dirt_conf: number
  dirt_min_frames: number
}
