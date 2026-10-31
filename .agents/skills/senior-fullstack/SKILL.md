---
name: senior-fullstack
description: "มองภาพรวมตอนเชื่อม frontend ↔ backend ของ HandCleanStation: ออกแบบ / แก้สัญญา REST และ WebSocket ใน systems/api.md, ลำดับงานสองฝั่ง, กรณีหลุด / พัง ใช้คู่กับ ponytail เพื่อเลือกทางที่ง่ายที่สุด. Use for any change that crosses the frontend-backend boundary or the overall system design."
---

# Senior Fullstack

ใช้เมื่องานข้ามเส้น frontend ↔ backend หรือต้องตัดสินใจระดับระบบ · **ใช้คู่กับ [ponytail](../ponytail/SKILL.md)**: ทุกทางเลือกไล่บันได ponytail ก่อน (ต้องมีไหม → มีในโค้ดแล้วไหม → stdlib / platform → dependency ที่มีอยู่ → เขียนน้อยที่สุด)
หลังได้สัญญาแล้ว แต่ละฝั่งวางต่อด้วย [senior-backend](../senior-backend/SKILL.md) และ [senior-frontend](../senior-frontend/SKILL.md)

## 1. อ่าน

- `systems/api.md` — สัญญาปัจจุบัน (✅ ตกลงแล้ว / TODO)
- `systems/spec/frontend.md`, `systems/spec/backend.md`, `systems/spec/ai.md`
- `systems/metrics/` ส่วนที่เกี่ยว
- โค้ดทั้งสองฝั่งที่งานแตะ

เรื่องที่อยู่ใน **Open items** (เช่น ช่องทางส่งภาพ) ห้ามเดา — เสนอทางเลือกพร้อมข้อดีข้อเสีย แล้วให้ผู้ใช้เลือก

## 2. ภาพระบบ

```
Electron renderer ──HTTP / WS :8000──► FastAPI backend ──► กล้อง (linuxpy) · AI (onnxruntime) · UV (gpiozero)
```

- Backend เป็นเจ้าของ hardware และ state ของการสแกน · frontend เป็นหน้าจออย่างเดียว
- WebSocket `/ws` เส้นเดียว: ภาพสด / ผล AI / สถานะสแกน / สถานะ UV ไปทาง frontend · คำสั่งมาทาง backend
- WebSocket หลุด → backend ดับ UV ทุกช่องทันที · frontend ขึ้น "กำลังเชื่อมต่อ…" และต่อใหม่เอง

## 3. ออกแบบสัญญา

ทุกข้อความ / endpoint ต้องตอบได้:

- **ใครเป็นเจ้าของ state** — ค่าจริงอยู่ฝั่ง backend; frontend แสดงตามที่ได้รับ ไม่เดาเอง
- **รูปแบบ** — field, type, หน่วย (ms, px อ้างอิงภาพขนาดไหน, ค่าครอป) · ผล AI ต้องมี `frame_id`, กรอบ, `class`, `conf`
- **หลุด / ซ้ำ / มาช้า** — reconnect แล้ว state ตรงกันไหม, ข้อความเก่ามาหลังข้อความใหม่ได้ไหม
- **Safety** — คำสั่งที่เปิด UV ต้องมีทางดับเองเสมอ
- **Performance** — ภาพสด ≥ 30 fps (BE-2, FE-1), ดีเลย์กล้อง → จอ ≤ 100 ms (BE-1)

อัปเดต `systems/api.md` **ใน PR เดียวกับโค้ด** (AGENTS.md กฎ 2)

## 4. Fullstack Plan

ส่งให้ผู้ใช้ก่อนลงโค้ด:

```markdown
🎯 เป้าหมาย: <ก่อน → หลัง>
🔌 สัญญา: <endpoint / ข้อความ: ทิศทาง, field, ตัวอย่าง JSON>
🪜 Ponytail: <ทางที่เลือก + ทางที่ข้าม และเหตุผลหนึ่งบรรทัด>
⚠️ หลุด / พัง: <แต่ละฝั่งทำอะไร, UV ดับไหม>
🧩 ลำดับงาน: <backend ก่อน → frontend · ไฟล์หลักแต่ละฝั่ง>
📊 Metrics: <ID ที่กระทบ>
❓ คำถาม: <Open items / ทางเลือกที่ผู้ใช้ต้องเลือก>
```

เสร็จเมื่อ: ผู้ใช้เลือกทางและตอบ ❓ ครบ, `api.md` มีร่างสัญญาใหม่ แล้วส่งต่อแต่ละฝั่ง
