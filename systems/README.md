# systems/

ศูนย์กลางของสิ่งที่ทีมต้องยึด: spec, อุปกรณ์, สัญญา API, เกณฑ์วัดผล, benchmark และสคริปต์ setup/run

| ไฟล์ / โฟลเดอร์ | ใช้ทำอะไร |
|---|---|
| [persona/SEIKA.md](persona/SEIKA.md) | บุคลิก "เซกะ" ของ AI agent ทุกตัวใน repo นี้ + รูป |
| [spec/frontend.md](spec/frontend.md) | หน้าจอ, ฟอนต์, การวาดกรอบ, kiosk |
| [spec/backend.md](spec/backend.md) | Architecture, camera pipeline, scan logic, config, safety, deployment |
| [spec/ai.md](spec/ai.md) | โมเดล, preprocess, เกณฑ์ตรวจ |
| [hardware.md](hardware.md) | รุ่นอุปกรณ์, ผังต่อสาย, ตาราง GPIO |
| [api.md](api.md) | สัญญา frontend ↔ backend (REST + WebSocket) |
| [metrics/](metrics/) | เกณฑ์วัดผลของแต่ละส่วน + ตารางบันทึกผล |
| [benchmark/](benchmark/) | สคริปต์วัดความเร็วของ pipeline บน Pi |
| [scripts/](scripts/) | setup / run ของ frontend, backend, docker (`.ps1` Windows, `.sh` Pi) |
| [catalog/](catalog/) | หน้าภาพรวม HTML สร้างด้วย skill `catalog-creator` |

กติกา:
- แก้พฤติกรรมของระบบ → อัปเดต spec ใน PR เดียวกัน
- แก้อะไรที่กระทบ metric → วัดแล้วเติมแถวในตารางผลของ `metrics/<ส่วน>.md` และแนบใน PR
- แต่ละไฟล์มีหัวข้อ **Open items** สำหรับเรื่องที่ยังไม่ตัดสิน ห้ามเดาเอง ให้ถามเจ้าของโปรเจกต์
