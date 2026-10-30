# Metrics: Docker

## เกณฑ์ (ร่าง)

| ID | เกณฑ์ | เป้า |
|---|---|---|
| DK-1 | build image arm64 จาก clean | ผ่าน ไม่มี error (ทั้งบน Windows/QEMU และบน Pi) |
| DK-2 | dependency ทุกตัว pin เลขตายตัว | ไม่มี `^ ~ >= <= < >` ใน `package.json` / `pyproject.toml` |
| DK-3 | เปิดเครื่อง Pi → `/health` ตอบ | ≤ 60 s |
| DK-4 | backend พัง → container เปิดใหม่เอง | ≤ 10 s |
| DK-5 | ขนาด image | ≤ 800 MB |
| DK-6 | container เห็นกล้องและ GPIO บน Pi | `/dev/video0`, `/dev/gpiochip0` ใช้ได้ |

## วิธีวัด

- **DK-1:** `systems/scripts/setup-docker.ps1` (Windows) / `.sh` (Pi) ด้วย `--no-cache`
- **DK-2:** `grep -nE '"[\^~<>]|[<>]=|~=' frontend/package.json backend/pyproject.toml` ต้องไม่มีผลลัพธ์
- **DK-3:** reboot แล้วจับเวลาจนกว่า `curl localhost:8000/health` ตอบ
- **DK-4:** `docker kill` process ข้างใน (หรือ `docker compose exec backend kill 1`) แล้วจับเวลา
- **DK-5:** `docker images hand-clean-station-backend`
- **DK-6:** `docker compose exec backend ls -l /dev/video0 /dev/gpiochip0`

## ผลการวัด

| วันที่ | version | ID | ค่าที่วัดได้ | ผ่าน/ไม่ผ่าน | ผู้วัด |
|---|---|---|---|---|---|
| 2026-10-30 | ก่อน commit แรก | DK-1 | build arm64 (Windows + QEMU) ผ่าน, image 183 MB — ยังไม่ได้ build บน Pi | ผ่าน (เฉพาะ Windows) | เซกะ (AI) |
| 2026-10-30 | ก่อน commit แรก | DK-2 | grep ไม่เจอ `^ ~ >= <= < >` ใน package.json / pyproject.toml | ผ่าน | เซกะ (AI) |
