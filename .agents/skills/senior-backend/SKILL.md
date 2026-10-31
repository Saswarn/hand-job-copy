---
name: senior-backend
description: "วางโครงงาน backend ของ HandCleanStation ก่อนเขียนโค้ด: แบ่งงานลง layer (api, core, schemas, services, utils), thread ของกล้อง / AI, ความปลอดภัยไฟ UV, config, metric BE-* / AI-* แล้วส่งต่อให้ fastapi-pro. Use before writing or restructuring code in backend/."
---

# Senior Backend

วางแผนก่อนลงโค้ดใน `backend/` (FastAPI + uv, Python 3.11) · ผลลัพธ์คือ **Backend Plan** สั้นๆ แล้วค่อยเขียนโค้ดด้วย [fastapi-pro](../fastapi-pro/SKILL.md)
งานที่แตะสัญญากับ frontend (REST / WebSocket) → ใช้ [senior-fullstack](../senior-fullstack/SKILL.md) ก่อน

## 1. อ่าน

- `systems/spec/backend.md` — camera pipeline, scan logic, config, safety, deployment
- `systems/spec/ai.md` — โมเดล, preprocess
- `systems/api.md` — สัญญากับ frontend
- `systems/hardware.md` — GPIO, กล้อง
- `systems/metrics/backend.md`, `systems/metrics/ai.md`
- โค้ดที่งานแตะ: เปิดไฟล์ และ grep ทุกจุดที่เรียกใช้

เรื่องที่อยู่ใน **Open items** ห้ามเดา ให้ถามผู้ใช้

## 2. วางลง layer

| ที่ | ใส่อะไร | ห้าม |
|---|---|---|
| `app/main.py` | สร้าง app, `lifespan`, รวม router | logic |
| `app/api/` | route REST และ `/ws` — รับ / ส่ง แล้วเรียก service | งานหนัก, แตะ hardware ตรง |
| `app/schemas/` | Pydantic model ของ request / response / ข้อความ WebSocket / config ตาม `api.md` | logic |
| `app/core/` | โหลด / บันทึก `config.json`, ค่าคงที่, logging | hardware |
| `app/services/` | camera (linuxpy, ring buffer), ai (onnxruntime), uv (gpiozero), scan (นับเวลา + ตัดสินผล) | import FastAPI |
| `app/utils/` | ฟังก์ชันบริสุทธิ์: crop, binary, letterbox 640, แปลงพิกัดกรอบ | state, I/O |

## 3. กฎของระบบ

- Backend เป็น**เจ้าของกล้องและ GPIO คนเดียว** · Pi 5 ใช้ `gpiozero` + `lgpio` ห้าม `RPi.GPIO` · dev ใช้ `GPIOZERO_PIN_FACTORY=mock`
- **ไฟ UV ต้องดับเอง** เมื่อสแกนเสร็จ, backend ปิด / พัง, WebSocket ของ frontend หลุด — ทุก plan ที่แตะ UV ต้องบอกว่าทั้ง 3 ทางยังครบ
- ภาพแสดงผล: ส่ง JPEG เดิมจากกล้อง ไม่ decode / re-encode · decode เฉพาะเฟรมที่ infer (simplejpeg scaled)
- **Preprocess ต้องเหมือนตอนเทรน**: crop → binary → letterbox 640 — แก้ขั้นไหนต้องเช็กกับโมเดล
- งานกล้อง / AI เป็น CPU / blocking → อยู่ใน thread ของตัวเอง ไม่บล็อก event loop ของ WebSocket
- ไม่บันทึกผล / รูป / ประวัติ · config มีไฟล์เดียว `backend/config.json`
- Dependency ใหม่: `uv add --bounds exact <pkg>` (ตัวที่ใช้เฉพาะ Linux ใส่ `; sys_platform == 'linux'`) และถามก่อนเพิ่ม
- ตัวเลขความเร็ววัดบน Pi จริงเท่านั้น

## 4. Backend Plan

ส่งให้ผู้ใช้ก่อนลงโค้ด:

```markdown
🎯 เป้าหมาย: <ก่อน → หลัง>
📂 ไฟล์ตาม layer: <api / schemas / core / services / utils: ไฟล์ + หน้าที่>
🧵 Thread / async: <อะไรรันที่ไหน ส่งข้อมูลข้าม thread ยังไง>
💡 UV failsafe: <3 ทางยังครบไหม — หรือ "ไม่แตะ">
⚙️ Config: <key ที่เพิ่ม / เปลี่ยนใน config.json>
🔌 API: <endpoint / ข้อความ WebSocket — ต้องมีใน api.md>
📊 Metrics: <BE-* / AI-* ที่กระทบ + วิธีวัด>
❓ คำถาม: <Open items / เรื่องที่ไม่ชัด>
```

เสร็จเมื่อ: ผู้ใช้ตอบ ❓ ครบ แล้วค่อยเขียนโค้ดตาม fastapi-pro
