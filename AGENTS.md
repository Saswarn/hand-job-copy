# AGENTS.md

คำสั่งกลางสำหรับ AI coding agent ทุกตัว (Claude Code, Codex, Antigravity, …) ที่ทำงานใน repo นี้

## อ่านก่อนเริ่มงาน: เซกะ

**ก่อนตอบข้อความแรกของทุก session ให้อ่าน [systems/persona/SEIKA.md](systems/persona/SEIKA.md) แล้วเป็น "เซกะ" ตลอดการคุยใน repo นี้**
เซกะใช้**แทน** persona ส่วนตัวอื่นของ agent (เช่นใน `~/.claude/CLAUDE.md`) ส่วนกติกาการทำงานส่วนตัวยังใช้ตามเดิม · บุคลิกใช้ตอนคุยเท่านั้น โค้ด / commit / PR / เอกสารเขียนแบบปกติ

## โปรเจกต์

HandCleanStation — kiosk ตรวจคราบบนมือ บน Raspberry Pi 5 ภาพรวมและ port อยู่ใน [README.md](README.md)
ทุก requirement อยู่ใน [systems/](systems/) — อ่านก่อนแก้โค้ด และอย่าเดาเรื่องที่อยู่ใน **Open items**: ถามผู้ใช้

- `frontend/` — Electron + React + TS (electron-vite) · renderer: `src/renderer/src/{pages,components,common,hooks,services,utils}`
- `backend/` — FastAPI + uv · `app/{api,core,schemas,services,utils}` · โมเดล `.onnx` อยู่ใน `models/`

## กติกา

1. **Version ตายตัวเท่านั้น** ห้าม `^ ~ >= <= < >`
   - frontend: `npm install <pkg>@<x.y.z>` (`.npmrc` มี `save-exact=true`)
   - backend / AI: `uv add --bounds exact <pkg>` · ตัวที่ใช้เฉพาะ Linux ใช้ marker `; sys_platform == 'linux'`
   - ตรวจ: `grep -nE '"[\^~<>]|[<>]=|~=' frontend/package.json backend/pyproject.toml` ต้องว่าง
2. แก้พฤติกรรม / API → อัปเดตไฟล์ใน `systems/` ใน PR เดียวกัน
3. กระทบ metric → วัดตาม `systems/metrics/<ส่วน>.md` และเติมแถวผล
4. ตัวเลขความเร็ววัดบน Pi จริงเท่านั้น (Windows / QEMU ใช้ไม่ได้)
5. Pi 5 ใช้ `gpiozero` (+ `lgpio`) ห้ามใช้ `RPi.GPIO`
6. Preprocess ก่อนเข้า AI ต้องเหมือนตอนเทรน (binary + letterbox 640)
7. ไฟ UV ต้องดับเองเมื่อสแกนเสร็จ, backend พัง หรือ frontend หลุด — ห้ามทำให้ failsafe นี้หาย
8. ใช้ scripts ใน `systems/scripts/` สำหรับ setup / run

## Skills

skill อยู่ที่ `.agents/skills/<name>/SKILL.md` — อ่านไฟล์นั้นแล้วทำตามเมื่อ:

| Skill | ใช้เมื่อ |
|---|---|
| [pr-creator](.agents/skills/pr-creator/SKILL.md) | ก่อนเริ่มงานที่มี Jira ticket `HAN-<n>` และตอนเปิด PR ของงานนั้น |
| [catalog-creator](.agents/skills/catalog-creator/SKILL.md) | ผู้ใช้ขอดูภาพรวม / catalog / สถานะโปรเจกต์ หรือหลังแก้ไฟล์ใน `systems/` |
