# API: frontend ↔ backend

Base: `http://localhost:8000` · WebSocket: `ws://localhost:8000/ws`

สถานะ: ✅ = มีในโค้ดแล้ว · 📝 = ตกลงรูปแบบแล้ว ยังไม่ทำในโค้ด · TODO = ยังไม่ออกแบบ (อัปเดตไฟล์นี้ใน PR เดียวกับโค้ด)

## REST

| Method | Path | สถานะ | รายละเอียด |
|---|---|---|---|
| GET | `/health` | ✅ | `{"status": "ok"}` |
| GET | `/config` | TODO (HAN-10) | อ่าน config |
| PUT | `/config` | TODO (HAN-10) | แก้ค่าจากหน้า Debug แล้วบันทึกลง `config.json` |

## WebSocket `/ws`

- **ข้อความ binary** (backend → frontend) = ภาพสด 1 เฟรม เป็น JPEG ล้วน
- **ข้อความ text** = JSON มี field `type` บอกชนิด · schema อยู่ใน `backend/app/schemas/ws.py`
- ช่องไฟ UV (`channel`, `channels[i]`) เป็น index เริ่มที่ 0 ตามลำดับใน `uv_gpio` (0 = UV 1)

### ภาพสด (binary)

| สถานะ | รายละเอียด |
|---|---|
| ✅ | backend crop ตาม `camera.crop` และวาดกรอบ AI ทับลงบนภาพแล้ว frontend แค่แสดงผล ไม่ต้องแปลงพิกัด ไม่ต้องหน่วงภาพ |
| ✅ | ส่งเฉพาะเฟรมล่าสุด ถ้า client รับไม่ทันจะข้ามเฟรม ไม่ต่อคิว |
| ✅ | กรอบสี: `hand` เขียว, `dirt` แดง · ตอนนี้ยังไม่มีกรอบ: `Detector` ใน `backend/app/services/detector.py` คืนค่าว่างจนกว่าจะต่อโมเดล |

ขนาดภาพ: กว้างอย่างน้อย `stream.min_width` แต่ไม่ถึง 2 เท่า (หรือเท่าภาพที่ crop ได้ ถ้ากล้องเล็กกว่า) · frontend ควรย่อ / ขยายให้พอดีจอเอง

### backend → frontend (text)

| `type` | สถานะ | รูปแบบ | ส่งเมื่อ |
|---|---|---|---|
| `uv` | ✅ | `{"type": "uv", "channels": [false, false, false]}` | ทันทีที่ต่อ และหลังสั่ง `uv_set` ทุกครั้ง |
| `error` | ✅ | `{"type": "error", "message": "..."}` | ข้อความจาก frontend ผิดรูปแบบ หรือคำสั่งที่ยังไม่ทำ |
| `scan` | 📝 (HAN-13) | `{"type": "scan", "state": "idle" \| "scanning" \| "done", "remaining_s": 3.2 \| null, "result": "clean" \| "dirt" \| null}` | เริ่มสแกน, ทุกวินาทีระหว่างสแกน, ตอนจบ |

### frontend → backend (text)

| `type` | สถานะ | รูปแบบ | ผล |
|---|---|---|---|
| `uv_set` | ✅ | `{"type": "uv_set", "channel": 0, "on": true}` | เปิด / ปิดไฟ UV ช่องเดียว (หน้า Debug) แล้วตอบ `uv` |
| `scan_start` | 📝 | `{"type": "scan_start"}` | backend เปิด UV ทุกช่อง + นับ `scan_seconds` แล้วดับเอง · ตอนนี้ตอบ `error` |
| `binary_view` | 📝 | `{"type": "binary_view", "on": true}` | สลับภาพสดเป็นภาพ binary ที่ป้อนเข้า AI (หน้า Debug) · ตอนนี้ตอบ `error` |

## กติกาที่ตกลงแล้ว

- ✅ WebSocket ตัวไหนก็ตามหลุด → backend ดับไฟ UV ทุกช่องทันที
- ✅ backend เริ่มทำงาน / ปิด → ไฟ UV ทุกช่องดับ
- ✅ กรอบ AI วาดบนภาพที่ backend แล้ว (ไม่ส่งพิกัดให้ frontend)
