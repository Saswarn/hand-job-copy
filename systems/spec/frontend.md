# Spec: Frontend (Electron kiosk)

สถานะ: Draft · ที่มา: design session 2026-10-29

## Stack

- Electron + React + TypeScript (template electron-vite) อยู่ใน `frontend/`
- สไตล์: **Tailwind CSS v4** (`@tailwindcss/vite`) · design token (สี, ฟอนต์, ขนาด) อยู่ใน `@theme` ของ `src/renderer/src/assets/main.css` ที่เดียว ไม่ hard-code ใน component
- Electron เป็น**หน้าจออย่างเดียว** ไม่รัน AI ไม่แตะกล้อง / GPIO ตรงๆ ทุกอย่างผ่าน backend (`localhost:8000`, ดู [api.md](../api.md))
- โครง renderer: `src/renderer/src/{pages,components,common,hooks,services,utils,assets}`
- Routing: **react-router** `HashRouter` (Electron โหลดจาก `file://` ใช้ hash ได้ทุกที่) · path อยู่ใน `common/routes.ts`
- CSP ใน `src/renderer/index.html` เปิด `connect-src` ให้ `ws://localhost:8000` / `http://localhost:8000`
- Type: `npm run typecheck` — TS `strict` + `noImplicitAny` + `noUncheckedIndexedAccess` (ตั้งใน `tsconfig.web.json` / `tsconfig.node.json`) · ข้อความ text จาก `/ws` ตอนนี้ยังไม่ได้ใช้ ถ้าจะใช้ให้เขียน type ตาม `backend/app/schemas/ws.py` และตรวจด้วย type guard ก่อนใช้
- เทสต์: `npm test` (Vitest + jsdom + Testing Library) ไฟล์ `*.test.ts(x)` ข้างไฟล์ที่ทดสอบ · ครอบ: `backendSocket` (ส่งต่อเฉพาะภาพ, ต่อใหม่ 1 วิ, ปิดแล้วไม่ต่อ), `useLiveFrames` (สถานะ, ทิ้งเฟรมที่ decode เสร็จช้า, ปิด socket), `LongPressCorner` (3 วิ, ปล่อยก่อน, ไม่ส่ง click ต่อ)

## จอและดีไซน์

- จอ ViewSonic TD1630-3: **1366×768**, TN, touch → ออกแบบที่ 1366×768, สี contrast สูง (TN มุมมองแคบ)
- ฟอนต์: **Noto Sans Thai Looped** ทั้งแอป (ไทยแบบมีหัว อ่านสบายตา)
- ตัวใหญ่ ปุ่มใหญ่ อ่านได้ในระยะแขน ดีไซน์เรียบ ไม่ดู "AI"

## หน้าจอ

| หน้า | Route / ไฟล์ | รายละเอียด |
|---|---|---|
| วิดีโอสอนใช้งาน | `#/` · `pages/TutorialPage.tsx` | `.mp4` ไฟล์เดียวในเครื่อง เล่นวน ปิดเสียง สอนวิธีใช้งาน · แตะตรงไหนก็ได้ → หน้า AI detection |
| AI detection | `#/detection` · `pages/AiDetectionPage.tsx` | สั่งเปิด UV ทุกช่อง → ภาพสด + กรอบ AI → นับเวลาถอยหลัง → ขึ้นผล "สะอาด" / "ยังมีคราบ" + จุดที่เจอ ทับบนหน้าเดียวกัน (ไม่มีหน้าผลลัพธ์แยก) → สั่งปิด UV · ไม่มีการแตะจอนานเกิน 60 วินาที → กลับหน้าวิดีโอ |
| Settings / Debug | `#/settings` · `pages/SettingsPage.tsx` | เข้าได้โดยกดค้างที่**มุมขวาบน** 3 วินาที (ไม่มี PIN) จากทุกหน้า · ปุ่ม "กลับ" → หน้าวิดีโอ |

Route อื่นที่ไม่รู้จัก → หน้าวิดีโอ

สถานะตอนนี้ (HAN-15): ทั้ง 3 หน้าเป็นโครง · หน้าวิดีโอยังเป็นข้อความแทนวิดีโอ · หน้า AI detection แสดงภาพสดจาก `/ws` แล้ว แต่ยังไม่มี UV / นับถอยหลัง / ผล (รอ scan ใน api.md) · Settings ยังว่าง

### Components / hooks / services

| ไฟล์ | หน้าที่ |
|---|---|
| `components/LongPressCorner.tsx` | พื้นที่มองไม่เห็น 96×96 px มุมขวาบน วางครั้งเดียวใน `App.tsx` · กดค้าง 3 วิ → Settings · แตะสั้นไม่ทำอะไร (ไม่ส่ง click ต่อให้หน้าข้างใต้) |
| `components/LiveView.tsx` | `<canvas>` ภาพสดเต็มพื้นที่ (`object-contain`) + `ConnectingOverlay` ตอนยังต่อไม่ได้ |
| `components/ConnectingOverlay.tsx` | "กำลังเชื่อมต่อ…" ตัวใหญ่กลางจอ |
| `hooks/useLiveFrames.ts` | `useLiveFrames(canvasRef) → connected` · รับ JPEG → `createImageBitmap` → วาดใน `requestAnimationFrame` เก็บแค่เฟรมล่าสุด ทิ้งเฟรมที่มาช้ากว่า · เฟรมไม่ผ่าน React state |
| `services/backendSocket.ts` | `connectBackend({ onFrame, onStatus })` เปิด `/ws`, หลุดแล้วต่อใหม่ทุก 1 วินาที, คืนฟังก์ชันปิด |
| `common/routes.ts` | path ของทั้ง 3 หน้า |

Settings / Debug มี:
- **Debug camera:** ภาพสด, ปุ่ม "ดูภาพ binary", binary threshold, exposure / gain / white balance, ซูม, เวลาหน่วงภาพ
- **Debug UV:** ปุ่มเปิดปิดแยกทีละช่อง (3 ช่อง)
- **Scan params:** `scan_seconds`, `dirt_conf`, `dirt_min_frames`

ถ้าเชื่อม backend ไม่ได้ → แสดง "กำลังเชื่อมต่อ…" ตัวใหญ่ และต่อใหม่เองอัตโนมัติ

## ภาพสดและกรอบ AI

- รับภาพจาก `/ws` เป็นข้อความ binary (JPEG ล้วน) ที่ backend **crop และวาดกรอบ AI ให้แล้ว** (ดู [api.md](../api.md)) · frontend แค่แสดงผล ไม่แปลงพิกัด ไม่หน่วงภาพ
- แสดงผล: `createImageBitmap(blob)` (decode นอก main thread) แล้ววาดลง `<canvas>` ย่อ / ขยายให้พอดีพื้นที่ · ปิด bitmap เก่าทุกเฟรม (`bitmap.close()`)
- ภาพลื่น ~30 fps ตามกล้อง; กรอบอัปเดตตามผล AI (5–10 ครั้ง/วินาที)

## Kiosk

- Pi: เปิดเองตอนบูต, fullscreen (`KIOSK=1` → `BrowserWindow({ kiosk: true })`), ซ่อนเมาส์
- Dev (Windows): หน้าต่าง 1366×768 ปกติ

## Open items

- [ ] วิธี autostart Electron บน Pi (desktop autostart / systemd user service)
