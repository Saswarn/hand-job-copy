---
name: senior-frontend
description: "วางโครงงาน frontend ของ HandCleanStation ก่อนเขียนโค้ด: แบ่งงานลง layer (pages, components, common, hooks, services, utils), flow ของหน้าจอ, การเชื่อม backend, metric FE-* ที่กระทบ แล้วส่งต่อให้ react-best-practices / ui-ux-pro-max. Use before writing or restructuring code in frontend/."
---

# Senior Frontend

วางแผนก่อนลงโค้ดใน `frontend/` (Electron + React + TS + Tailwind) · ผลลัพธ์คือ **Frontend Plan** สั้นๆ แล้วค่อยเขียนโค้ดด้วย [react-best-practices](../react-best-practices/SKILL.md) และออกแบบหน้าจอด้วย [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md)
งานที่แตะสัญญากับ backend (REST / WebSocket) → ใช้ [senior-fullstack](../senior-fullstack/SKILL.md) ก่อน

## 1. อ่าน

- `systems/spec/frontend.md` — หน้าจอ, จอ 1366×768, kiosk, ภาพสด + กรอบ AI
- `systems/api.md` — สัญญากับ backend
- `systems/metrics/frontend.md` — FE-1 … FE-6
- โค้ดที่งานแตะ: เปิดไฟล์ และ grep ทุกจุดที่เรียกใช้

เรื่องที่อยู่ใน **Open items** ห้ามเดา ให้ถามผู้ใช้

## 2. วางลง layer

| ที่ | ใส่อะไร | ห้าม |
|---|---|---|
| `src/main/` | สร้างหน้าต่าง (`KIOSK=1` → `kiosk: true`), ซ่อนเมาส์ | logic ของแอป, แตะกล้อง / GPIO |
| `src/preload/` | expose API ที่ renderer ต้องใช้จริงเท่านั้น | เปิด `ipcRenderer` ทั้งก้อน |
| `renderer/src/pages/` | หนึ่งไฟล์ต่อหนึ่งหน้า: วิดีโอสอน, สแกน, ผลลัพธ์, Settings / Debug | เรียก backend ตรง |
| `renderer/src/components/` | UI ที่ใช้ซ้ำ (ปุ่ม, overlay "กำลังเชื่อมต่อ…", canvas กรอบ AI) | state ของระบบ |
| `renderer/src/hooks/` | state + logic ที่หน้าใช้ (เช่น การเชื่อม WebSocket, สถานะสแกน) | JSX |
| `renderer/src/services/` | คุยกับ backend: WebSocket client, REST (`/config`, `/auth/pin`) | React |
| `renderer/src/utils/` | ฟังก์ชันบริสุทธิ์ เช่น แปลงพิกัด 640×640 letterbox → พิกัดจอ (คิดครอป / ซูม) | side effect |
| `renderer/src/common/` | types และ constants ที่ใช้หลาย layer (รูปแบบข้อความ WebSocket ตาม `api.md`) | logic |

## 3. กฎของระบบ

- Renderer **ไม่แตะกล้อง / GPIO / ไฟล์ config** — ทุกอย่างผ่าน backend `localhost:8000`
- Flow หลัก: วิดีโอ → (แตะ) สแกน → ผลลัพธ์ → วิดีโอ · Settings เข้าได้ทางกดค้างมุมจอ 3 วินาที + PIN
- Backend หลุด → overlay "กำลังเชื่อมต่อ…" ระดับแอป และต่อใหม่เอง (FE-4) · frontend หลุด = backend ดับ UV เอง ห้ามพึ่ง frontend ในการดับไฟ
- ภาพสด 30 fps + กรอบ AI บน `<canvas>`: เฟรม / ผลล่าสุดเก็บใน ref ไม่ใช่ state, หน่วงภาพตาม `display_delay_ms`
- สไตล์ใช้ Tailwind + token ใน `@theme` ของ `assets/main.css` เท่านั้น · ไม่โหลดอะไรจากเน็ต
- Dependency ใหม่: `npm install <pkg>@<x.y.z>` (version ตายตัว) และถามก่อนเพิ่ม

## 4. Frontend Plan

ส่งให้ผู้ใช้ก่อนลงโค้ด:

```markdown
🎯 เป้าหมาย: <ก่อน → หลัง>
📂 ไฟล์ตาม layer: <pages / components / hooks / services / utils / common: ไฟล์ + หน้าที่>
🔁 Flow / state: <state อยู่ที่ไหน ใครเปลี่ยน>
🔌 Backend: <endpoint / ข้อความ WebSocket ที่ใช้ — ต้องมีใน api.md>
📊 Metrics: <FE-* ที่กระทบ + วิธีวัด>
❓ คำถาม: <Open items / เรื่องที่ไม่ชัด>
```

เสร็จเมื่อ: ผู้ใช้ตอบ ❓ ครบ แล้วค่อยเขียนโค้ดตาม react-best-practices
