# Spec: Backend (Python service)

สถานะ: Draft · ที่มา: design session 2026-10-29

## Stack

- Python 3.11.15, FastAPI + uvicorn, จัดการด้วย **uv** อยู่ใน `backend/`
- โครง: `app/{api,core,schemas,services,utils}`, ไฟล์โมเดลอยู่ใน `models/`
- Backend เป็นเจ้าของกล้องและ GPIO **คนเดียว**
- Pi 5 ใช้ `RPi.GPIO` ไม่ได้ → ใช้ `gpiozero` (+ `lgpio`); dev บน Windows ใช้ `GPIOZERO_PIN_FACTORY=mock`

## Architecture

```
┌──────────── backend (Docker, restart: always) ─────────────┐
│ linuxpy (v4l2) ── raw MJPEG ──┬──► ring buffer ──► ส่งภาพไปหน้าจอ   │
│                               └──► เฉพาะเฟรม AI (5–10 fps)         │
│                                    simplejpeg scaled decode → crop │
│                                    → binary → letterbox 640        │
│                                    → onnxruntime → detections      │
│ gpiozero ◄── คำสั่ง UV                                             │
└────────────────────────────────────────────────────────────┘
            ▲ HTTP / WebSocket :8000
┌──────── frontend (Electron) ────────┐
└─────────────────────────────────────┘
```

## Camera pipeline

1. ดึง JPEG เฟรมดิบจากกล้อง (Arducam IMX585 USB3, MJPEG) ด้วย `linuxpy` — ไม่ผ่าน OpenCV ในขั้นนี้
2. **ภาพแสดงผล:** ส่ง JPEG เดิมจากกล้องไปหน้าจอ ไม่ decode / re-encode
3. **ภาพเข้า AI:** decode เฉพาะเฟรมที่จะ infer ด้วย `simplejpeg` (libjpeg-turbo) แบบย่อขนาดตอน decode (1/2, 1/4)
4. ล็อกค่ากล้องเอง: exposure, gain, white balance (ห้าม auto ใต้ UV)
5. **ซูม** (ตั้งครั้งเดียวตอนติดตั้ง): ถ้ากล้องรองรับ `zoom_absolute` → ให้กล้องครอปเอง ไม่งั้นครอปใน Python สำหรับภาพเข้า AI

เหตุผลที่ไม่ decode ทุกเฟรม: Pi 5 ไม่มี hardware JPEG decoder; decode 4K ทุกเฟรมที่ 30 fps + re-encode จะทำให้ CPU เต็ม

## Scan logic

- สแกนนาน `scan_seconds` (default 5)
- เจอ `dirt` ที่ confidence ≥ `dirt_conf` (default 0.5) ติดต่อกัน ≥ `dirt_min_frames` เฟรม (default 3) → "ยังมีคราบ" ไม่งั้น → "สะอาด"
- ไม่บันทึกผล / รูป / ประวัติ

## Config

ไฟล์เดียว [`backend/config.json`](../../backend/config.json) backend อ่าน / เขียน (หน้า Debug แก้ผ่าน API แล้ว backend บันทึก)

| key | ความหมาย |
|---|---|
| `pin` | PIN เข้าหน้า Settings |
| `uv_gpio` | เลขขา GPIO ของไฟ UV แต่ละช่อง (แก้ตามสายจริงได้โดยไม่ต้องแก้โค้ด) |
| `camera.*` | device, ความละเอียดที่ดึง, exposure, gain, white balance, zoom, crop |
| `binary_threshold` | threshold ของภาพ binary ก่อนเข้า AI |
| `display_delay_ms` | เวลาหน่วงภาพสดให้ตรงกับกรอบ |
| `scan_seconds`, `dirt_conf`, `dirt_min_frames` | เกณฑ์การสแกน |

## Safety (ไฟ UV)

ไฟ UV ดับเองทุกครั้งเมื่อ:
- สแกนเสร็จ
- backend ปิดหรือพัง
- frontend หลุดการเชื่อมต่อ

## Deployment

- Docker image arm64 ตรงกับ Raspberry Pi OS Bookworm: `python:3.11.15-slim-bookworm` + uv `0.11.8`
- Dev (Windows): `docker-compose.yml` (QEMU, mock GPIO, ไม่มีกล้อง)
- Pi: `docker-compose.yml` + `docker-compose.pi.yml` (ส่ง `/dev/video0`, `/dev/gpiochip0` เข้า container, `restart: always`)

## Open items

- [ ] **Deployment บน Pi:** spec เดิมกำหนด systemd; ตอนนี้ setup เป็น Docker `restart: always` — ยืนยันว่าใช้ Docker
- [ ] **ผล `v4l2-ctl -d /dev/video0 --list-ctrls`** บน Pi จริง (มี `zoom_absolute` ไหม, ชื่อ control ของ exposure / gain / WB)
- [ ] **ความละเอียดที่ดึงจากกล้อง** (4K / 1080p / 720p) — ตัดสินหลัง benchmark
- [ ] **เพดานเวลาเปิดไฟ UV** (เสนอ 60 วินาที แม้เปิดจากหน้า Debug) — ยังไม่ยืนยัน
- [ ] ชื่อ device GPIO บน Pi 5 (`/dev/gpiochip0` หรือ `gpiochip4` ขึ้นกับ kernel)
