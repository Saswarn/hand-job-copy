# Metrics: Hardware

## เกณฑ์ (ร่าง)

| ID | เกณฑ์ | เป้า |
|---|---|---|
| HW-1 | สั่งเปิด / ปิดไฟ UV แต่ละช่องจากหน้า Debug | ทำงานถูกช่อง 20/20 ครั้ง |
| HW-2 | สแกนเสร็จ → ไฟ UV ดับ | ≤ 500 ms |
| HW-3 | backend พัง (kill) → ไฟ UV ดับ | ≤ 1 s |
| HW-4 | frontend หลุด (ปิด Electron / ถอด WebSocket) → ไฟ UV ดับ | ≤ 2 s |
| HW-5 | กล้องให้ภาพที่ความละเอียดที่ตั้ง | ได้ fps ตามที่ตั้งจากกล้อง (เช่น 30) |
| HW-6 | อุณหภูมิ CPU ของ Pi ตอนสแกนวน 30 นาที | ≤ 80 °C, ไม่ throttle |

## วิธีวัด

- **HW-1:** กดทีละช่อง ดูไฟจริง + `gpioinfo`
- **HW-2 – HW-4:** อัดวิดีโอ slow-motion ให้เห็นทั้งไฟและหน้าจอ/terminal นับเฟรม
- **HW-5:** `v4l2-ctl -d /dev/video0 --list-formats-ext` + benchmark ขั้นดึงภาพ
- **HW-6:** `vcgencmd measure_temp` และ `vcgencmd get_throttled`

## ผลการวัด

| วันที่ | version | ID | ค่าที่วัดได้ | ผ่าน/ไม่ผ่าน | ผู้วัด |
|---|---|---|---|---|---|
| | | | | | |
