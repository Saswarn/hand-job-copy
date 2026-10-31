---
name: ticket-flow
description: "ใช้ก่อนเริ่มงาน HandCleanStation ที่มี ticket และตอนเปิด PR ของงานนั้น: รับ Jira ticket HAN, ทำ Work Card ตรวจกับโค้ดและ systems/, branch, commit, PR body (ภาษาไทย). Run before starting ticketed HandCleanStation work and when opening its PR."
---

หนึ่ง ticket → หนึ่ง Work Card → ชื่อ branch เดียว → หนึ่ง PR · Work Card คือ**ด่านกั้น**: ห้ามสร้าง branch ห้ามแก้ไฟล์ จนกว่าผู้ใช้จะพิมพ์ `เริ่ม` / `go`

## 1. Ticket

ขอ Jira ticket (`HAN-<n>`) ก่อน ไม่มี ticket ห้ามเริ่มงาน ดึงด้วย Atlassian MCP `getJiraIssue` (cloudId `7e6fbae7-38cd-429d-b1c2-d1d59035732f`, project `HAN` = HandCleanStation): summary, description, acceptance criteria, issue ที่ link ไว้ · ถ้า tool นี้ไม่มี Atlassian MCP ให้ขอผู้ใช้ copy เนื้อหา ticket มาให้

เสร็จเมื่อ: สรุปเป้าหมายของ ticket ได้ในหนึ่งบรรทัด

## 2. ร่าง Work Card

ก่อนถามอะไร ให้ทำการบ้านก่อน: อ่านโค้ดที่ ticket แตะ (เปิดไฟล์, grep ทุกจุดที่เรียกใช้) และส่วนที่เกี่ยวข้องใน [systems/](#systems) แล้วกรอกทุกช่องเอง พร้อมติดเครื่องหมายทุกช่อง:

- ✅ **ข้อเท็จจริง**: ยืนยันได้จากโค้ด, ticket หรือ systems/ (อ้าง `file:line` หรือ § ของเอกสาร)
- ❓ **ยังไม่ชัด**: ยืนยันไม่ได้
- ⚠️ **ขัดกัน**: ticket, โค้ด และ systems/ ไม่ตรงกัน ยกข้อความทั้งสองฝั่งมา

```markdown
🎫 HAN-<n> — <summary ของ ticket>
🌿 Base: develop                     → <type>/HAN-<n>-<slug>
🔀 Action: new-job | change-job ของ #<PR>
🧩 Changes: <layer: page · component · hook · service · utils (frontend) · api · service · schema · core (backend) · infra (docker / scripts)> + ไฟล์
🎯 Solve: <ปัญหาที่แก้หรือความสามารถที่เพิ่ม: ก่อน → หลัง>
🔌 Systems: <frontend · backend · ai · docker · hardware (กล้อง / GPIO / UV)>
⚠️ Output: <API / ข้อความ WebSocket · config.json key · ไฟล์โมเดล · พฤติกรรมไฟ UV · ผู้เรียกอื่น>
📐 Spec: <ไฟล์และ § ใน systems/ ที่ต้องเป็นไปตาม>
📊 Metrics: <ID ใน systems/metrics/ ที่กระทบ เช่น FE-1, AI-1 หรือ —>
🚩 Flags: <จาก TEMPLATE.md>
```

- `new-job` = งานใหม่ · `change-job` = เปลี่ยนพฤติกรรมที่ merge ไปแล้ว: ต้องระบุ PR/commit ที่ถูกเปลี่ยน และแตก branch ใหม่จาก `develop`
- Base คือ `develop` (repo มี `develop` + `main`)

ตรวจทุกช่องกับ**กับดัก**เหล่านี้ (มันเปลี่ยนได้ ยืนยันในโค้ดเสมอ):

- **Version ตายตัว:** dependency ใหม่ห้ามมี `^ ~ >= <= < >` (frontend `npm install <pkg>@<x.y.z>`, backend `uv add --bounds exact`)
- **Preprocess ต้องเหมือนตอนเทรน:** crop → binary → letterbox 640 — แก้ขั้นไหนต้องเช็กกับโมเดล
- **Pi 5 ใช้ `gpiozero` + `lgpio`** ห้าม `RPi.GPIO` · dev บน Windows ใช้ `GPIOZERO_PIN_FACTORY=mock`
- **ไฟ UV failsafe:** ต้องดับเมื่อสแกนเสร็จ, backend พัง, frontend หลุด — งานที่แตะ UV ต้องยืนยันว่ายังครบ
- **ความเร็ววัดบน Pi จริงเท่านั้น** ผลจาก Windows / QEMU ใช้เป็นหลักฐานความเร็วไม่ได้
- **Backend เป็นเจ้าของกล้องและ GPIO คนเดียว** frontend ห้ามแตะตรง
- ไฟล์โมเดล `backend/models/*.onnx` ไม่อยู่ใน git

เสร็จเมื่อ: ทุกช่องมีเครื่องหมาย และทุก ✅ มีที่อ้างอิง

## 3. ยืนยัน

แสดง card แล้วถามเฉพาะช่อง ❓ และ ⚠️ ช่องละหนึ่งคำถาม · ⚠️ ที่เกี่ยวกับ spec ให้ไปตาม [Requirement ขัดกัน](#requirement-ขัดกัน)

- คำตอบที่**ไม่แน่ใจ** (`อาจจะ`, `น่าจะ`, `มั้ง`, `คิดว่า`, `maybe`, `probably`, `I think`) ช่องนั้นยังเป็น ❓ ให้ถามใหม่ให้แคบลง
- คำตอบที่ขัดกับโค้ด เปลี่ยนช่องเป็น ⚠️ และบอกในข้อความถัดไปพร้อม `file:line`
- ผู้ใช้แก้ช่องที่เป็น ✅: อ่านโค้ดใหม่ แล้วติดเครื่องหมายใหม่

เสร็จเมื่อ: ทุกช่องเป็น ✅ และผู้ใช้พิมพ์ `เริ่ม` / `go`

## 4. ลงมือ

- Branch `<type>/HAN-<n>-<slug>`; `type` ∈ `feat fix refactor chore docs`
- Commit: `[HAN-<n>] <type>(<scope>): <english description>` เช่น `[HAN-12] feat(uv): turn off all channels on websocket disconnect` · commit ย่อยเป็น checkpoint เล็กๆ (ข้อความ commit ยังเป็นภาษาอังกฤษ)
- `scope` ∈ `frontend backend ai uv camera docker systems` หรือชื่อหน้า / service
- แก้เฉพาะส่วนที่อยู่ใน card ถ้าต้องแตะที่อื่น → หยุดแล้วถามก่อน อัปเดต card ก่อนเสมอ

## 5. ตรวจกับ systems/ อีกรอบ

- เอา diff ที่เสร็จแล้วเทียบกับ [systems/](#systems): grep หาทุก endpoint, ข้อความ WebSocket, config key, หน้า และกฎที่ diff แตะ รวมถึงที่ card ตกหล่น แต่ละอย่างต้องตรงกับหัวข้อใดหัวข้อหนึ่ง (จดไว้ใส่ PR) หรือไปตาม [Requirement ขัดกัน](#requirement-ขัดกัน)
- แตะ API → `systems/api.md` ต้องอัปเดตใน PR นี้
- กระทบ metric → วัดตาม `systems/metrics/<ส่วน>.md` เติมแถวผล แล้วแนบในหลักฐานของ PR
- รัน `grep -nE '"[\^~<>]|[<>]=|~=' frontend/package.json backend/pyproject.toml` ต้องว่าง

เสร็จเมื่อ: ทุกพฤติกรรมที่แตะตรงกับหัวข้อใน systems/ หรือ systems/ ถูกอัปเดตใน PR นี้แล้วโดยผู้ใช้ยืนยัน

## 6. PR

- **PR body เขียนเป็นภาษาไทย** ตาม [`TEMPLATE.md`](TEMPLATE.md) · ชื่อไฟล์, path, ชื่อฟังก์ชัน, คำสั่ง, ชื่อ branch และ commit hash คงเป็นภาษาอังกฤษตามจริง
- Title = รูปแบบเดียวกับ commit (`[HAN-<n>] <type>(<scope>): <english description>`)
- push เข้า branch ที่มีอยู่แล้ว: เช็ก `gh pr view <N> --json state` ก่อน ถ้า merge แล้วให้เปิด PR ใหม่และแจ้งผู้ใช้
- เป้าหมายคือ base ของ card (`develop`)

เสร็จเมื่อ: รายงาน URL ของ PR แล้ว

---

## systems/

ทุก requirement อยู่ใน `systems/` ของ repo นี้ อ่านจาก working tree ได้เลย

- `systems/spec/` = frontend.md · backend.md · ai.md
- `systems/hardware.md` = อุปกรณ์ + ผังต่อสาย + GPIO
- `systems/api.md` = สัญญา frontend ↔ backend
- `systems/metrics/` = เกณฑ์วัดผลแต่ละส่วน + ตารางผล
- หัวข้อ **Open items** = ยังไม่ตัดสิน ห้ามเดา ให้ถามผู้ใช้

## Requirement ขัดกัน

แสดงข้อความ spec (ไฟล์ + §) คู่กับ ticket หรือโค้ด แล้วถามว่า: requirement เปลี่ยนแล้วหรือยัง? ปิดได้ด้วยคำตอบ ใช่ หรือ ไม่ใช่ เท่านั้น ถ้าตอบแบบไม่แน่ใจให้ถามใหม่

- **ไม่ใช่** → โค้ด (หรือ card) ผิด: แก้ให้ตรงกับ spec
- **ใช่** → อัปเดตไฟล์ใน `systems/` ใน PR เดียวกัน (commit แยก `[HAN-<n>] docs(systems): <what changed>`) จดกฎ เก่า → ใหม่ ลงหัวข้อ `📐 Requirement` ของ PR แล้วเพิ่ม 📐 ใน flags
