# Spec: Frontend (Electron kiosk)

สถานะ: Draft · ที่มา: design session 2026-10-29

## Stack

- Electron + React + TypeScript (template electron-vite) อยู่ใน `frontend/`
- สไตล์: **Tailwind CSS v4** (`@tailwindcss/vite`) · design token (สี, ฟอนต์, ขนาด) อยู่ใน `@theme` ของ `src/renderer/src/assets/main.css` ที่เดียว ไม่ hard-code ใน component
- Electron เป็น**หน้าจออย่างเดียว** ไม่รัน AI ไม่แตะกล้อง / GPIO ตรงๆ ทุกอย่างผ่าน backend (`localhost:8000`, ดู [api.md](../api.md))
- โครง renderer: `src/renderer/src/{pages,components,common,hooks,services,utils,assets}`

## จอและดีไซน์

- จอ ViewSonic TD1630-3: **1366×768**, TN, touch → ออกแบบที่ 1366×768, สี contrast สูง (TN มุมมองแคบ)
- ฟอนต์: **Noto Sans Thai Looped** ทั้งแอป (ไทยแบบมีหัว อ่านสบายตา)
- ตัวใหญ่ ปุ่มใหญ่ อ่านได้ในระยะแขน ดีไซน์เรียบ ไม่ดู "AI"

## หน้าจอ

| หน้า | รายละเอียด |
|---|---|
| วิดีโอสอนใช้งาน | `.mp4` ไฟล์เดียวในเครื่อง เล่นวน ปิดเสียง สอนวิธีใช้งาน · แตะตรงไหนก็ได้ → หน้า AI detection |
| AI detection | สั่งเปิด UV ทุกช่อง → ภาพสด + กรอบ AI → นับเวลาถอยหลัง → ขึ้นผล "สะอาด" / "ยังมีคราบ" + จุดที่เจอ ทับบนหน้าเดียวกัน (ไม่มีหน้าผลลัพธ์แยก) → สั่งปิด UV · ไม่มีการแตะจอนานเกิน 60 วินาที → กลับหน้าวิดีโอ |
| Settings / Debug | เข้าได้โดยกดค้างที่มุมจอ 3 วินาที (ไม่มี PIN) |

Settings / Debug มี:
- **Debug camera:** ภาพสด, ปุ่ม "ดูภาพ binary", binary threshold, exposure / gain / white balance, ซูม, เวลาหน่วงภาพ
- **Debug UV:** ปุ่มเปิดปิดแยกทีละช่อง (3 ช่อง)
- **Scan params:** `scan_seconds`, `dirt_conf`, `dirt_min_frames`

ถ้าเชื่อม backend ไม่ได้ → แสดง "กำลังเชื่อมต่อ…" ตัวใหญ่ และต่อใหม่เองอัตโนมัติ

## ภาพสดและกรอบ AI

- ภาพสดลื่น 30 fps; ผล AI มาราว 5–10 ครั้ง/วินาที (CPU ของ Pi 5)
- **หน่วงภาพสด ~200ms** (`display_delay_ms`, ปรับได้ในหน้า Debug) ให้กรอบตรงกับเฟรมที่ AI ประมวลผลจริง ผลทับด้วย `<canvas>`
- เฟรมระหว่างผล AI ใช้กรอบของผลล่าสุด
- แปลงพิกัดกรอบจาก 640×640 (letterbox) กลับเป็นพิกัดบนจอ โดยคิดค่าครอป / ซูมด้วย
- ซูม: ถ้ากล้องครอปเองไม่ได้ ภาพบนจอครอปด้วย CSS ใช้ค่าครอปเดียวกับที่ backend ใช้กับภาพเข้า AI

## Kiosk

- Pi: เปิดเองตอนบูต, fullscreen (`KIOSK=1` → `BrowserWindow({ kiosk: true })`), ซ่อนเมาส์
- Dev (Windows): หน้าต่าง 1366×768 ปกติ

## Open items

- [ ] ช่องทางรับภาพจาก backend: WebSocket + `frame_id` หรือ MJPEG ผ่าน HTTP (ดู [api.md](../api.md))
- [ ] วิธี autostart Electron บน Pi (desktop autostart / systemd user service)
