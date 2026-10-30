---
name: catalog-creator
description: "สร้างหน้าภาพรวม (catalog) ของ HandCleanStation จาก systems/ เป็น HTML หน้าเดียว ให้ทีมเห็นสถานะ, spec, API, metrics และ open items ในที่เดียว ใช้เมื่อผู้ใช้ขอดูภาพรวม / catalog / สถานะโปรเจกต์ หรือหลังแก้ไฟล์ใน systems/. Build the project overview page from systems/."
---

อ่าน `systems/` ทั้งหมด → เขียน `systems/catalog/index.html` หน้าเดียว → (ถ้ามี Artifact tool) publish เป็น Artifact

## 1. อ่าน

อ่านทุกไฟล์ `.md` ใน `systems/` (persona/, spec/, hardware.md, api.md, metrics/, benchmark/README.md), [README.md](../../../README.md), `frontend/package.json`, `backend/pyproject.toml`, `backend/.python-version` และ `backend/Dockerfile`
**ห้ามแต่งข้อมูลเพิ่ม** — ทุกอย่างในหน้าต้องมาจากไฟล์เหล่านี้ เรื่องที่ไฟล์ไม่ได้บอก ให้แสดงว่า "ยังไม่มีข้อมูล"

เสร็จเมื่อ: มีรายการของทุกส่วนต่อไปนี้ พร้อมไฟล์ต้นทาง

## 2. เนื้อหาของหน้า

**หัว** — ชื่อโปรเจกต์, วันที่สร้าง, commit ล่าสุด (`git log -1 --format=%h`), ไฟล์ต้นทาง

มุมขวาบนมี **ปุ่มสลับโหมดสว่าง / มืด** (ค่าเริ่มต้นสว่าง จำค่าที่เลือกไว้ใน localStorage ห่อด้วย try/catch)

แล้วแบ่งเป็น **4 tab** (เปิดตรงด้วย `#overview`, `#frontend`, `#backend`, `#skills`):

1. **ภาพรวม** (`#overview`)
   - **การ์ดเซกะ** (บนสุด) — รูปจาก `systems/persona/seika.webp` embed เป็น data URI (base64 ด้วยสคริปต์ ห้ามพิมพ์เอง) + บุคลิก 5 ข้อจาก `systems/persona/SEIKA.md`
   - **Mindmap** อธิบายระบบ: ราก = HandCleanStation, กิ่ง = Frontend (หน้าจอ), Backend, AI, Docker, Hardware, Safety แต่ละกิ่งมีใบสั้นๆ อธิบาย + แถบขั้นตอนใช้งาน
     - desktop: ต้นไม้จากซ้ายไปขวา เส้นแนวตั้งเริ่มที่กิ่งแรกและจบที่กิ่งสุดท้าย เส้นจากรากต้องไม่ทับตัวหนังสือ
     - มือถือ (≤ 640px): รากอยู่บน กิ่งเรียงลงด้านล่าง หน้าต้องไม่ล้นแนวนอน
   - **Ports** — ตาราง `Repo | Port`: Frontend, Backend, Backend (Docker) และ repo อื่นถ้ามี (จาก README.md, docker-compose.yml, config ของ electron-vite)
   - **อุปกรณ์ที่ใช้** — ตารางจาก `systems/hardware.md`
   - **Docker** — ตาราง Dev (Windows) เทียบ Pi 5 จาก `backend/Dockerfile`, `docker-compose.yml`, `docker-compose.pi.yml`: base image, platform, uv, image, port, restart, GPIO factory, volumes, devices, compose, script
   - **การวัดผล AI** จาก `systems/metrics/ai.md` + `systems/benchmark/`:
     - การประมวลผลต่อเฟรม: grab / decode / binary / infer / total พร้อมเป้า (AI-1, AI-2) และผลล่าสุด
     - ความแม่นยำ: AI-3 – AI-6 พร้อมเป้า วิธีวัด และผลล่าสุด
     - เกณฑ์ตัดสินผลสแกน (ค่าจาก config)
     - ผลล่าสุดจากตารางผล → ผ่าน (เขียว) / ไม่ผ่าน (แดง) / ยังไม่วัด (เทา)
2. **Frontend** (`#frontend`) — ตาราง `Stack, Libs | Version` จาก `frontend/package.json` (แถวกลุ่ม Stack แล้ว Libs)
3. **Backend** (`#backend`) — ตาราง `Stack, Libs | Version` จาก `backend/pyproject.toml`, `.python-version`, `Dockerfile` (ตัวที่ใช้ marker Linux ให้ระบุ `(Linux)`)
4. **Skill** (`#skills`) — จาก `AGENTS.md` และ `.agents/skills/*/SKILL.md`:
   - แถบ "ใช้ skill ไหนตอนไหน": ก่อนเริ่มงาน · ระหว่างทำงาน · ตอนเปิด PR · หลังแก้ systems/
   - การ์ดละ skill: ทำอะไร, ใช้ตอนไหน, เรียกใช้ (Claude `/name` · tool อื่นอ่าน SKILL.md), รูปแบบ branch / commit (ถ้ามี), ผลลัพธ์, ขั้นตอนย่อ
   - skill ใหม่ใน `.agents/skills/` ต้องขึ้นใน tab นี้ด้วย

ทุกตารางระบุไฟล์ต้นทาง · version ต้องตรงกับไฟล์ทุกตัว

## 3. ดีไซน์

- HTML ไฟล์เดียว CSS inline ไม่มี build ไม่พึ่ง CDN ยกเว้น Google Fonts (Noto Sans Thai Looped)
- อ่านง่ายบนจอคอมและมือถือ, **ค่าเริ่มต้นสว่าง** + ปุ่มสลับ: token สว่างบน `:root`, token มืดบน `:root[data-theme="dark"]` (ไม่ตาม `prefers-color-scheme`)
- ใส่ `[hidden] { display: none !important }` และ viewport meta เอง เพราะตอนเปิดเป็นไฟล์ในเครื่องจะไม่มี reset ของ Artifact
- ตรวจจากภาพจริงก่อน publish (desktop + มือถือ 375px, ทุก tab, ทั้งสองโหมด)
- สถานะใช้สี + ข้อความ (ไม่ใช้สีอย่างเดียว)
- ภาษาไทย ศัพท์เทคนิคคงภาษาอังกฤษ

## 4. ส่งออก

- เขียนทับ `systems/catalog/index.html` ทุกครั้ง (ไฟล์นี้อยู่ใน git ให้ทีมเปิดดูในเครื่องได้)
- **ถ้า tool มี Artifact tool (Claude):** publish ไฟล์นี้เป็น Artifact — ครั้งแรกสร้างใหม่ แล้วจด URL ไว้ใน `systems/catalog/ARTIFACT_URL` ครั้งต่อไปอ่าน URL จากไฟล์นี้และอัปเดตที่ URL เดิม (อ่าน artifact ก่อน publish ตามกติกาของ tool)
- **tool อื่น:** บอกผู้ใช้ให้เปิด `systems/catalog/index.html` ในเบราว์เซอร์

เสร็จเมื่อ: ไฟล์ถูกเขียน, ลิงก์ทุกตัวชี้ไปไฟล์ที่มีจริง และบอก URL หรือ path ให้ผู้ใช้แล้ว
