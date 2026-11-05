# Spec: Frontend (Electron kiosk)

สถานะ: Draft · ที่มา: design session 2026-10-29

## Stack

- Electron + React + TypeScript (template electron-vite) อยู่ใน `frontend/`
- สไตล์: **Tailwind CSS v4** (`@tailwindcss/vite`) · design token (สี, ฟอนต์, ขนาด) อยู่ใน `@theme` ของ `src/renderer/src/assets/main.css` ที่เดียว ไม่ hard-code ใน component
- Electron เป็น**หน้าจออย่างเดียว** ไม่รัน AI ไม่แตะกล้อง / GPIO ตรงๆ ทุกอย่างผ่าน backend (`localhost:8000`, ดู [api.md](../api.md))
- โครง renderer: `src/renderer/src/{pages,components,common,hooks,services,utils,assets}`
- Routing: **react-router** `HashRouter` (Electron โหลดจาก `file://` ใช้ hash ได้ทุกที่) · path อยู่ใน `common/routes.ts`
- CSP ใน `src/renderer/index.html` เปิด `connect-src` ให้ `ws://localhost:8000` / `http://localhost:8000`
- Type: `npm run typecheck` — TS `strict` + `noImplicitAny` + `noUncheckedIndexedAccess` (ตั้งใน `tsconfig.web.json` / `tsconfig.node.json`) · สัญญากับ backend ทั้งหมดอยู่ใน `common/api.ts` (type ของ REST / `/ws` + `parseServerMessage` ตรวจข้อความก่อนใช้)
- เทสต์: `npm test` (Vitest + jsdom + Testing Library) ไฟล์ `*.test.ts(x)` ข้างไฟล์ที่ทดสอบ · ครอบ: `api` (ข้อความถูก / ผิด), `backendSocket` (ภาพ / ข้อความ, ส่งเฉพาะตอนต่ออยู่, ต่อใหม่ 1 วิ, ปิดแล้วไม่ต่อ), `BackendProvider` (state, ส่งภาพให้ผู้ฟัง, ฟังก์ชันคงที่, ปิดตอน unmount), `useLiveFrames` (ทิ้งเฟรมที่ decode เสร็จช้า), `LongPressCorner` (3 วิ, ปล่อยก่อน, ไม่ส่ง click ต่อ)

## จอและดีไซน์

- จอ ViewSonic TD1630-3: **1366×768**, TN, touch → ออกแบบที่ 1366×768, สี contrast สูง (TN มุมมองแคบ)
- ฟอนต์: **Noto Sans Thai Looped** ทั้งแอป (ไทยแบบมีหัว อ่านสบายตา) · ไฟล์ในเครื่องจาก `@fontsource/noto-sans-thai-looped` (400, 700) import ใน `main.tsx` ใช้ได้ไม่มีเน็ต
- Token ใน `@theme` (`assets/main.css`): สี `surface` (ดำ), `ink` (ขาว), `muted`, `uv`, `clean` (เขียว), `dirt` (แดง) · ขนาดตัวอักษร `text-body` 36 px, `text-title` 48 px, `text-display` 72 px (นับถอยหลัง / ผล) · ข้อความหลัก ≥ 32 px (FE-5)
- ตัวใหญ่ ปุ่มใหญ่ อ่านได้ในระยะแขน ดีไซน์เรียบ ไม่ดู "AI"

## หน้าจอ

| หน้า | Route / ไฟล์ | รายละเอียด |
|---|---|---|
| วิดีโอสอนใช้งาน | `#/` · `pages/TutorialPage.tsx` | `.mp4` ไฟล์เดียวในเครื่อง เล่นวน ปิดเสียง สอนวิธีใช้งาน · แตะตรงไหนก็ได้ → หน้า AI detection |
| AI detection | `#/detection` · `pages/AiDetectionPage.tsx` | ส่ง `scan_start` (backend เปิด / ปิด UV เอง) → ภาพสด + กรอบ AI → นับถอยหลังจาก `scan.remaining_s` → ขึ้นผล "สะอาด" / "ยังมีคราบ" จาก `scan.result` ทับบนหน้าเดียวกัน (ไม่มีหน้าผลลัพธ์แยก) · ไม่มีการแตะจอนานเกิน 5 วินาที → กลับหน้าวิดีโอ |
| Settings / Debug | `#/settings` · `pages/SettingsPage.tsx` | เข้าได้โดยกดค้างที่**มุมขวาบน** 3 วินาที (ไม่มี PIN) จากทุกหน้า · ปุ่ม "กลับ" → หน้าวิดีโอ |

Route อื่นที่ไม่รู้จัก → หน้าวิดีโอ

สถานะตอนนี้: หน้าวิดีโอเล่นไฟล์ตัวอย่างแล้ว · หน้า AI detection แสดงภาพสดและกลับหน้าวิดีโอเมื่อไม่ได้แตะ 5 วินาที ยังไม่มีนับถอยหลัง / ผล · Settings มี 3 ช่อง (กล้อง / ไฟ UV / การสแกน) แสดงสถานะ UV อย่างเดียว

### Components / hooks / services

| ไฟล์ | หน้าที่ |
|---|---|
| `components/LongPressCorner.tsx` | พื้นที่มองไม่เห็น 96×96 px มุมขวาบน วางครั้งเดียวใน `App.tsx` · กดค้าง 3 วิ → Settings · แตะสั้นไม่ทำอะไร (ไม่ส่ง click ต่อให้หน้าข้างใต้) |
| `components/BackendProvider.tsx` | เปิด `/ws` **ครั้งเดียวทั้งแอป** (ครอบใน `App.tsx`) · ข้อความ text → state, ภาพ → ส่งตรงให้ผู้ฟัง ไม่ผ่าน state |
| `hooks/useIdleReturn.ts` | หน้าตรวจเริ่มนับใหม่เมื่อเกิด `pointerdown` · ครบเวลาแล้วกลับหน้าวิดีโอ · ล้าง timer และ listener เมื่อออกจากหน้า |
| `hooks/useBackend.ts` | `useBackend() → { connected, uv, scan, error, send, subscribeFrames }` ใช้ได้ทุกหน้า · `send(msg)` คืน `false` ถ้ายังต่อไม่ได้ · `send` / `subscribeFrames` เป็นฟังก์ชันตัวเดิมตลอด |
| `components/ConnectingOverlay.tsx` | "กำลังเชื่อมต่อ…" ทับ**ทุกหน้า**ตอน `connected = false` (อยู่ใต้ `LongPressCorner` จึงยังเข้า Settings ได้) |
| `components/LiveView.tsx` | `<canvas>` ภาพสดเต็มพื้นที่ (`object-contain`) |
| `hooks/useLiveFrames.ts` | `useLiveFrames(canvasRef)` · รับ JPEG จาก `subscribeFrames` → `createImageBitmap` → วาดใน `requestAnimationFrame` เก็บแค่เฟรมล่าสุด ทิ้งเฟรมที่มาช้ากว่า |
| `services/backendSocket.ts` | `connectBackend({ onFrame, onMessage, onStatus }) → { send, close }` · ต่อใหม่ทุก 1 วินาที · ข้อความที่ไม่รู้จัก → `console.warn` แล้วทิ้ง |
| `common/api.ts` | สัญญากับ backend: URL, `ClientMessage`, `ServerMessage`, `AppConfig`, `parseServerMessage` |
| `common/routes.ts` | path ของทั้ง 3 หน้า |

**ไฟ UV กับ socket เดียว:** backend ดับ UV เมื่อ socket หลุด แต่ socket ทั้งแอปไม่ปิดตอนเปลี่ยนหน้า → หน้าที่เปิด UV เอง (Settings / Debug) **ต้องส่ง `uv_set` ปิดทุกช่องตอนออกจากหน้า** · การสแกนให้ backend ดับเองเมื่อครบเวลา

Settings / Debug มี:
- **Debug camera:** ภาพสด, ปุ่ม "ดูภาพ binary", binary threshold, exposure / gain / white balance, ซูม, crop
- **Debug UV:** ปุ่มเปิดปิดแยกทีละช่อง (3 ช่อง)
- **Scan params:** `scan_seconds`, `dirt_conf`, `dirt_min_frames`

ถ้าเชื่อม backend ไม่ได้ → แสดง "กำลังเชื่อมต่อ…" ตัวใหญ่ และต่อใหม่เองอัตโนมัติ

## ภาพสดและกรอบ AI

- รับภาพจาก `/ws` เป็นข้อความ binary (JPEG ล้วน) ที่ backend **crop และวาดกรอบ AI ให้แล้ว** (ดู [api.md](../api.md)) · frontend แค่แสดงผล ไม่แปลงพิกัด ไม่หน่วงภาพ
- แสดงผล: `createImageBitmap(blob)` (decode นอก main thread) แล้ววาดลง `<canvas>` ย่อ / ขยายให้พอดีพื้นที่ · ปิด bitmap เก่าทุกเฟรม (`bitmap.close()`)
- ภาพลื่น ~30 fps ตามกล้อง; กรอบอัปเดตตามผล AI (5–10 ครั้ง/วินาที)

## Kiosk

- Pi: เปิดเองตอนบูต, fullscreen (`KIOSK=1` → `BrowserWindow({ kiosk: true })`), ซ่อนเมาส์ (`insertCSS` `cursor: none` ใน `src/main/index.ts`)
- Dev (Windows): หน้าต่าง 1366×768 ปกติ

## Open items

- [ ] วิธี autostart Electron บน Pi (desktop autostart / systemd user service)
