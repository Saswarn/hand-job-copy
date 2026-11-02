---
name: react-best-practices
description: "กฎเขียน React ให้เร็วและไม่ re-render เกิน สำหรับ renderer ของ Electron ใน frontend/ (hooks, state, WebSocket, canvas 30 fps, lazy-load) ใช้ตอนเขียน / รีวิว / refactor component, hook, service ฝั่ง frontend หลังวางโครงด้วย senior-frontend แล้ว. React performance rules for the Electron renderer."
license: MIT
metadata:
  source: "claude-code-templates web-development/react-best-practices v1.0.0 (Vercel Engineering), trimmed to client-side React 2026-10-31"
---

# React Best Practices

กฎ React ฝั่ง client จาก Vercel Engineering ตัดส่วน Next.js / RSC / SSR / API routes ออกแล้ว · แต่ละกฎมีตัวอย่างผิด / ถูกใน `references/rules/<id>.md` เปิดเฉพาะกฎที่เกี่ยว

## HandCleanStation overrides

- Renderer เป็น **SPA ใน Electron** (electron-vite, React 19, TS) — ไม่มี SSR, hydration, server component, `next/*`
- ข้อมูลหลักมาทาง **WebSocket เดียว** (`ws://localhost:8000/ws`, ดู `systems/api.md`) ไม่ใช่ fetch หลายตัว — กลุ่ม `async-*` ใช้กับ REST ไม่กี่ตัว (`/config`)
- **หน้าสแกนต้อง 30 fps** (FE-1): ภาพสดและกรอบ AI วาดบน `<canvas>` ใน `requestAnimationFrame` เก็บเฟรม / ผลล่าสุดใน `useRef` **ไม่ใช่ state** — ห้ามให้ทุกข้อความ WebSocket ทำให้ component re-render
- ไม่เพิ่ม library ใหม่เพื่อทำตามกฎ (เช่น SWR) ถ้าโค้ดไม่กี่บรรทัดทำได้ · ถ้าต้องเพิ่มจริง ล็อก version ตามกฎ AGENTS.md
- กฎที่สำคัญที่สุดกับโปรเจกต์นี้: `rerender-*`, `advanced-*`, `client-event-listeners`, `rendering-conditional-render`, `js-*` ใน loop วาดกรอบ, `bundle-dynamic-imports` (lazy-load หน้า Debug ให้ FE-6 ≤ 5 s)

## กฎตามลำดับผลกระทบ

| # | กลุ่ม | prefix | ผล |
|---|---|---|---|
| 1 | Eliminating Waterfalls | `async-` | CRITICAL |
| 2 | Bundle Size | `bundle-` | CRITICAL |
| 3 | Client-Side Data Fetching | `client-` | MEDIUM-HIGH |
| 4 | Re-render Optimization | `rerender-` | MEDIUM |
| 5 | Rendering Performance | `rendering-` | MEDIUM |
| 6 | JavaScript Performance | `js-` | LOW-MEDIUM |
| 7 | Advanced Patterns | `advanced-` | LOW |

### 1. Eliminating Waterfalls
- `async-defer-await` — ย้าย await เข้าไปใน branch ที่ใช้จริง
- `async-dependencies` — parallel ตาม dependency
- `async-parallel` — `Promise.all()` สำหรับงานที่ไม่ขึ้นต่อกัน
- `async-suspense-boundaries` — วาง Suspense ให้ layout ขึ้นก่อน

### 2. Bundle Size
- `bundle-barrel-imports` — import ตรงจากไฟล์ ไม่ผ่าน barrel
- `bundle-conditional` — โหลด module ใหญ่เฉพาะเมื่อใช้
- `bundle-dynamic-imports` — `React.lazy` สำหรับหน้า / component หนัก
- `bundle-preload` — preload ตามสิ่งที่ผู้ใช้กำลังจะทำ

### 3. Client-Side Data Fetching
- `client-event-listeners` — รวม global listener (ใช้กับ WebSocket / keydown / touch)
- `client-swr-dedup` — ใช้เฉพาะถ้าโปรเจกต์มี SWR แล้ว

### 4. Re-render Optimization
- `rerender-defer-reads` — อ่าน state ที่จุดใช้งาน
- `rerender-memo` — แยก component ที่แพงแล้ว memo
- `rerender-dependencies` — dependency ของ effect ให้แคบ
- `rerender-derived-state` — subscribe ค่าที่ derive แล้ว
- `rerender-lazy-state-init` — `useState(() => ...)`
- `rerender-transitions` — `startTransition` สำหรับงานไม่เร่งด่วน

### 5. Rendering Performance
- `rendering-animate-svg-wrapper` — animate ตัวห่อ ไม่ใช่ SVG
- `rendering-content-visibility` — `content-visibility` กับ list ยาว
- `rendering-hoist-jsx` — ย้าย JSX คงที่ออกนอก component
- `rendering-svg-precision` — ลดทศนิยมใน SVG
- `rendering-activity` — `<Activity>` สำหรับซ่อน / แสดง
- `rendering-conditional-render` — ใช้ ternary ชัดๆ ไม่ใช้ `&&` กับตัวเลข

### 6. JavaScript Performance (hot path เช่น loop วาดกรอบ)
- `js-batch-dom-css`, `js-index-maps`, `js-cache-property-access`, `js-cache-function-results`, `js-cache-storage`, `js-combine-iterations`, `js-length-check-first`, `js-early-exit`, `js-hoist-regexp`, `js-min-max-loop`, `js-set-map-lookups`, `js-tosorted-immutable`

### 7. Advanced Patterns
- `advanced-event-handler-refs` — เก็บ handler ใน ref
- `advanced-use-latest` — `useLatest` ให้ callback คงที่ (เหมาะกับ handler ของ WebSocket)

## วิธีใช้

1. วัดก่อน: React DevTools Profiler / Performance panel — ตัวเลขความเร็วจริงวัดบน Pi เท่านั้น (AGENTS.md กฎ 4)
2. แก้ตามลำดับผลกระทบในตาราง
3. วัดซ้ำ แล้วเติมผลใน `systems/metrics/frontend.md` ถ้ากระทบ FE-*
4. อย่า optimize ล่วงหน้า — memo / ref เฉพาะจุดที่วัดแล้วช้า หรือ hot path ที่รู้อยู่แล้ว (หน้าสแกน)

## Resources

- [React Documentation](https://react.dev)
