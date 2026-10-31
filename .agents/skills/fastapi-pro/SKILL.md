---
name: fastapi-pro
description: "แนวเขียนโค้ด FastAPI ของ HandCleanStation: route, WebSocket /ws, lifespan + ดับไฟ UV, Pydantic v2, config.json, งานกล้อง / AI ใน thread, เทสต์ด้วย TestClient + mock GPIO, uvicorn ใน Docker arm64 ใช้ตอนเขียน / รีวิวโค้ดใน backend/ หลังวางโครงด้วย senior-backend แล้ว. FastAPI coding guide scoped to this project."
metadata:
  source: "based on claude-code-templates development/fastapi-pro (2026-02-27), rewritten for HandCleanStation 2026-10-31"
---

# FastAPI Pro (HandCleanStation)

เขียนโค้ดใน `backend/` ตาม plan จาก [senior-backend](../senior-backend/SKILL.md) · ใช้เฉพาะสิ่งที่โปรเจกต์นี้มี: FastAPI, uvicorn, Pydantic v2 (มากับ FastAPI), numpy, onnxruntime, simplejpeg, gpiozero (+ lgpio), linuxpy
**ไม่มีในโปรเจกต์ อย่านำเข้า:** DB / ORM, Redis, auth แบบ JWT / OAuth, GraphQL, Celery / queue, microservices, k8s, OpenTelemetry · ถ้างานต้องใช้จริง ถามผู้ใช้ก่อน

## App และ lifespan

- `app/main.py` สร้าง `FastAPI(lifespan=...)` และ `include_router` จาก `app/api/` เท่านั้น
- `lifespan`: เปิด service (กล้อง, AI, UV) ตอนเริ่ม · ตอนจบ (`finally`) **ดับ UV ทุกช่องก่อน** แล้วค่อยปิดกล้อง / thread
- เก็บ service ไว้ใน `app.state` แล้วดึงผ่าน dependency (`Annotated[UvService, Depends(get_uv)]`) — ไม่ใช้ global ลอยๆ เพื่อให้เทสต์ใส่ mock ได้
- ใช้ `def` ธรรมดาสำหรับ route ที่ไม่มี I/O แบบ async · `async def` เมื่อ await จริง (WebSocket)

## WebSocket `/ws`

- รับ client หลักทีละตัว (kiosk เดียว) — ตามสัญญาใน `systems/api.md`
- ห่อ loop ด้วย `try / except WebSocketDisconnect / finally` → ใน `finally` **ดับ UV ทุกช่อง** (กฎ: frontend หลุด → ไฟดับ)
- ข้อความ JSON สร้างจาก Pydantic model (`model.model_dump_json()`) ไม่ประกอบ dict เอง
- ภาพสด: ส่ง JPEG เดิมจากกล้อง ไม่ decode / re-encode · รูปแบบการส่งยังเป็น Open item ใน `api.md` — ห้ามเลือกเอง
- คนส่งช้าไม่ทำให้กล้องช้า: ส่งเฟรมล่าสุด ข้ามเฟรมที่ค้าง ไม่ต่อคิวยาว

## Thread และ event loop

- อ่านกล้อง (linuxpy) และ infer (onnxruntime) เป็นงาน blocking → รันใน thread ของ service เอง (`threading.Thread(daemon=True)`) ไม่รันใน event loop
- ส่งผลจาก thread ไป WebSocket: เก็บ "ผลล่าสุด" ไว้ในตัวแปรที่มี lock หรือใช้ `loop.call_soon_threadsafe` — ห้ามเรียก `await` ข้าม thread
- งานสั้นที่ blocking ใน route ใช้ `def` route (FastAPI รันใน threadpool ให้) หรือ `run_in_threadpool`
- สร้าง `onnxruntime.InferenceSession` ครั้งเดียวตอนเริ่ม ไม่สร้างต่อเฟรม

## Schemas และ config

- Pydantic v2 ใน `app/schemas/` · ตั้ง `model_config = ConfigDict(extra="forbid")` กับ input จาก frontend (`PUT /config`) แล้วใส่ `Field(ge=..., le=...)` กับค่าที่มีช่วง
- `config.json` ไฟล์เดียว: โหลดเป็น Pydantic model ใน `app/core/`, บันทึกแบบเขียนไฟล์ชั่วคราวแล้ว `os.replace` (ไฟดับกลางทางไฟล์ไม่พัง)
- `GET /config` ห้ามส่ง `pin` กลับ — ใช้ response model แยกที่ไม่มี field นี้
- ค่าที่เปลี่ยนตามเครื่อง (เลขขา GPIO, device กล้อง) อยู่ใน config ไม่ hard-code

## GPIO (ไฟ UV)

- `gpiozero.OutputDevice` / `LED` ต่อช่อง ตามเลขขาใน `uv_gpio` · ห้าม `RPi.GPIO`
- ทุกทางที่จบการสแกน (ครบเวลา, error, ยกเลิก) ดับ UV ใน `finally`
- Dev บน Windows / Docker dev: `GPIOZERO_PIN_FACTORY=mock`

## Error handling

- Error ที่คาดได้ → `HTTPException` พร้อมข้อความสั้น
- `@app.exception_handler(Exception)` ระดับแอป: log แล้ว**ดับ UV** ก่อนตอบ 500
- อย่ากลืน exception ใน thread ของกล้อง / AI เงียบๆ — log และตั้งสถานะให้ frontend รู้

## เทสต์

- `fastapi.testclient.TestClient` (รวม `client.websocket_connect("/ws")`) + `GPIOZERO_PIN_FACTORY=mock`
- เทสต์ที่ต้องมีเมื่อแตะ UV: ปิด WebSocket → ขาวัดของ mock เป็นปิดทุกช่อง · สแกนครบเวลา → ปิดทุกช่อง
- ใช้ `app.dependency_overrides` แทนกล้อง / AI จริง
- เพิ่ม pytest เป็น dev dependency ด้วย `uv add --dev --bounds exact pytest` เมื่อจำเป็น (ถามก่อน)

## รันและ deploy

- Dev: `uv run uvicorn app.main:app --reload --port 8000`
- Docker: uvicorn **worker เดียว** (กล้องและ GPIO เปิดได้ที่เดียว) · image `python:3.11.15-slim-bookworm` arm64 · `restart: always`
- Dependency ใหม่: `uv add --bounds exact <pkg>` (ตัวที่ใช้เฉพาะ Linux ใส่ `; sys_platform == 'linux'`)
- ถ้างานกระทบ BE-* / AI-* → วัดบน Pi แล้วเติมผลใน `systems/metrics/`
