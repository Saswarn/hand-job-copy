# เทมเพลต PR body

PR body เขียนเป็น**ภาษาไทย** · ชื่อไฟล์, path, ชื่อฟังก์ชัน, คำสั่ง, ชื่อ branch, commit hash และข้อความ error คงเป็นภาษาอังกฤษตามจริง

กรอกทุกหัวข้อ หัวข้อที่ไม่เกี่ยวให้ใส่ `—` พร้อมเหตุผล เพื่อให้ผู้อ่าน (คนหรือ AI) รู้ว่าตรวจแล้ว ไม่ได้ลืม เขียนสั้นๆ ให้ตารางและ checkbox เป็นตัวจัดโครงสร้าง

## Flags

ใส่ทุก flag ที่เกี่ยวในแถว `Flags` ของหัว PR อีโมจิละหนึ่ง ความหมายเดียวกันทุกที่:

| Flag | ความหมาย |
|---|---|
| 🟢 / 🟡 / 🔴 | ความเสี่ยง: ย้อนกลับได้ ผลกระทบแคบ / ต้องระวัง / ย้อนกลับไม่ได้หรือผลกระทบกว้าง |
| 💥 | Breaking change: REST, ข้อความ WebSocket หรือ config key ที่อีกฝั่งพึ่งพา |
| 🔦 | แตะ logic ของไฟ UV หรือ safety / failsafe |
| 🍓 | แตะฮาร์ดแวร์: กล้อง, GPIO, device ใน Docker |
| 🧠 | แตะโมเดล AI หรือ preprocess |
| 📊 | กระทบ metric (ต้องแนบผลวัด) |
| 🧪 | เพิ่มหรือแก้เทสต์ |
| 🎨 | UI เปลี่ยนที่มองเห็นได้ (ต้องมีภาพหน้าจอในหลักฐาน) |
| 🔄 | `change-job`: เปลี่ยนพฤติกรรมที่ merge ไปแล้ว |
| 📐 | Requirement เปลี่ยน: อัปเดต `systems/` ใน PR นี้แล้ว |

## เทมเพลต

```markdown
| 🎫 Ticket | [HAN-<n>](https://phuminforwork.atlassian.net/browse/HAN-<n>) |
|---|---|
| 🔀 Action | `new-job` / `change-job` ของ #<PR> |
| 🌿 Branch | `<type>/HAN-<n>-<slug>` → `develop` |
| 🔌 Systems | frontend · backend · ai · docker · hardware |
| 🚩 Flags | 🟢 🧪 … |

## 🎯 ทำไม
<ปัญหาที่แก้หรือความสามารถที่เพิ่ม หนึ่งถึงสองบรรทัด ใช้ภาษาเดียวกับ ticket>
<เฉพาะ change-job: ตาราง | ก่อน (#<PR>) | หลัง | ของพฤติกรรมที่เปลี่ยน>

## 🧩 เปลี่ยนอะไร
<มุมมองที่เล็กที่สุดที่อ่านแล้วเข้าใจ: diff-sketch, call tree, component tree หรือ file tree>

| Layer | ไฟล์ |
|---|---|
| page / component / hook / api / service / schema / infra / … | `path/to/file` |

## ⚠️ ผลลัพธ์และผลข้างเคียง
- **API / WebSocket:** <รูปแบบที่เปลี่ยน หรือ ไม่มี> (อัปเดต `systems/api.md` แล้ว?)
- **Config / ไฟล์:** <config.json key, ไฟล์โมเดล, ไฟล์อื่นที่อ่าน/เขียน>
- **ฮาร์ดแวร์ / UV:** <พฤติกรรมของไฟ UV, กล้อง, GPIO ที่เปลี่ยน หรือ ไม่มี>
- **ผู้เรียกอื่น:** <ใครอีกที่เรียกโค้ดที่เปลี่ยน และทำไมยังทำงานได้>

## 📐 Requirement
- **ตรวจกับ:** `systems/<file>` §<section>
- **ผล:** ✅ ตรงกับ spec / 📐 requirement เปลี่ยน (ยืนยันโดย <user> วันที่ <date>)
- **แก้เอกสาร:** commit `<hash>` — <กฎเดิม> → <กฎใหม่>  _(หรือ —)_

## 📊 Metrics
| ID | เป้า | ก่อน | หลัง | วัดบน | ผ่าน/ไม่ผ่าน |
|---|---|---|---|---|---|
| <FE-1> | <≥ 30 fps> | <…> | <…> | Pi 5 / Windows | ✅ / ❌ |
_(หรือ — ไม่กระทบ metric เพราะ …)_

## 🧪 หลักฐาน
- **ก่อน:** <ภาพหน้าจอ / เทสต์ที่ fail / output>
- **หลัง:** <ภาพหน้าจอ / เทสต์ที่ผ่าน / output>
- คำสั่งที่รัน: `npm run typecheck` ✅ · `npm run lint` ✅ · `npm test` ✅ · `uv run pyright` ✅ · `uv run pytest` ✅ · `curl localhost:8000/health` ✅ · …

## 🚪 ความเสี่ยงตอน merge
**ประตู:** ย้อนกลับไม่ได้ / ย้อนกลับได้ — <เพราะอะไร>
**วงผลกระทบ:** <คำเดียว> — <อะไรที่อาจพัง>

## ✅ Checklist
- [ ] แก้เฉพาะส่วนที่อยู่ใน Work Card
- [ ] เทียบ diff กับ `systems/` อีกรอบแล้ว (api.md / spec อัปเดตถ้าจำเป็น)
- [ ] dependency ใหม่ pin เลขตายตัว: `grep -nE '"[\^~<>]|[<>]=|~=' frontend/package.json backend/pyproject.toml` ว่าง
- [ ] type safe + unit test ของ logic ใหม่ ผ่านทั้ง typecheck / pyright และ `npm test` / `uv run pytest` (AGENTS.md ข้อ 9–10)
- [ ] 🔦 failsafe ไฟ UV ยังครบ (หรือ ไม่ได้แตะ)
- [ ] 📊 แนบผลวัดและเติมแถวใน `systems/metrics/` แล้ว (หรือ ไม่กระทบ)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
