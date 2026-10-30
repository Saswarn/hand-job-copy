# Spec: AI

สถานะ: Draft · ที่มา: design session 2026-10-29

## โมเดล

- YOLO11n, ไฟล์ `.onnx` วางที่ `backend/models/` (ไม่เก็บใน git)
- Runtime: `onnxruntime` บน CPU ของ Pi 5 (ยังไม่ใช้ Hailo)
- Input: 640×640, ภาพ **binary** — โมเดลเทรนด้วยภาพ binary
- Classes: `hand`, `dirt` แบบตีกรอบ (detect)
- เป้าความเร็ว: ~5–10 fps บน Pi 5 CPU (ถ้าไม่พอ → พิจารณา Raspberry Pi AI HAT+ / Hailo)

## Preprocess

ต้อง**เหมือนตอนเทรนทุกขั้น** ไม่งั้นความแม่นตก:

1. crop / zoom ตาม config
2. binary threshold (`binary_threshold`, ปรับได้ในหน้า Debug; มีปุ่ม "ดูภาพ binary")
3. letterbox เป็น 640×640

## เกณฑ์ตัดสิน

ดู [backend.md § Scan logic](backend.md#scan-logic)

## ไฟ UV กับ AI

ไฟ UV-A เป็นแสงส่องช่วยให้กล้องเห็นคราบ (คราบบางชนิดเรืองแสงเองใต้ UV-A) — ภาพตอนใช้งานต้องถ่ายใต้แสงแบบเดียวกับตอนเทรน

## Open items

- [ ] ชุดทดสอบ (test set) สำหรับวัด precision / recall ของ `dirt` — ใครเก็บ, กี่ภาพ
- [ ] ค่า threshold ของ binary ตอนเทรน (ใช้เป็น default)
- [ ] โมเดลเทรนใต้ไฟ UV ความยาวคลื่นไหน (รอสเปกไฟ UV)
