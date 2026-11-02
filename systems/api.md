# API: frontend ↔ backend

Base: `http://localhost:8000` · WebSocket: `ws://localhost:8000/ws`

สถานะ: **โครง** — ✅ = ตกลงแล้ว / มีแล้ว · TODO = ทีมออกแบบและเขียนต่อ (อัปเดตไฟล์นี้ใน PR เดียวกับโค้ด)

## REST

| Method | Path | สถานะ | รายละเอียด |
|---|---|---|---|
| GET | `/health` | ✅ มีแล้ว | `{"status": "ok"}` |
| GET | `/config` | TODO | อ่าน config |
| PUT | `/config` | TODO | แก้ค่าจากหน้า Debug แล้วบันทึกลง `config.json` |

## WebSocket `/ws`

### backend → frontend

| ข้อความ | สถานะ | รายละเอียด |
|---|---|---|
| ภาพสด | TODO | ดู Open items เรื่องช่องทางส่งภาพ |
| ผล AI | ✅ ต้องมี: `frame_id`, กรอบ, `class` (`hand` / `dirt`), `conf` | รูปแบบ JSON: TODO |
| สถานะการสแกน | TODO | เริ่ม / เวลาที่เหลือ / ผล "สะอาด" หรือ "ยังมีคราบ" |
| สถานะไฟ UV | TODO | แต่ละช่องเปิดหรือปิด |

### frontend → backend

| ข้อความ | สถานะ | รายละเอียด |
|---|---|---|
| เริ่มสแกน | TODO | backend เปิด UV + เริ่มนับเวลา |
| เปิด / ปิดไฟ UV รายช่อง | TODO | ใช้ในหน้า Debug |
| ขอดูภาพ binary | TODO | ใช้ในหน้า Debug |

## กติกาที่ตกลงแล้ว

- ✅ frontend หลุดการเชื่อมต่อ WebSocket → backend ดับไฟ UV ทุกช่องทันที
- ✅ พิกัดกรอบต้องแปลงกลับเป็นพิกัดบนจอได้ (ระบุว่าอ้างอิงภาพขนาดไหน และค่าครอปที่ใช้)

## Open items

- [ ] **ช่องทางส่งภาพ:** (a) WebSocket binary = `frame_id` 4 byte + JPEG เดิมจากกล้อง — จับคู่กับผล AI ได้ตรงเฟรม · (b) MJPEG ผ่าน HTTP (`<img>`) — ง่ายกว่า แต่ใส่ `frame_id` ต่อเฟรมไม่ได้
