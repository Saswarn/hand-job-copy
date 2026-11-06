# Hardware

## อุปกรณ์

| ชิ้น | รุ่น | หมายเหตุ |
|---|---|---|
| Computer | Raspberry Pi 5, 16GB RAM | Raspberry Pi OS Bookworm 64-bit |
| จอ | ViewSonic TD1630-3, 15.6" TN, 1366×768, touch | |
| กล้อง | Arducam IMX585 USB3 (STARVIS 2, 8.3MP) | USB3 → พอร์ตสีฟ้าของ Pi, ส่ง MJPEG |
| เลนส์ | Arducam C-mount 8mm | fixed focal → ซูมได้แบบดิจิทัลเท่านั้น |
| ไฟ UV | **TBD** | 3 ช่อง, ช่องละ 1 รีเลย์ |
| รีเลย์ | **TBD** | |

## ผังต่อสาย

```
Pi 5 GPIO ──► รีเลย์ ch1 ──► ไฟ UV 1
          ──► รีเลย์ ch2 ──► ไฟ UV 2
          ──► รีเลย์ ch3 ──► ไฟ UV 3
Pi 5 USB3 ──► กล้อง IMX585
Pi 5 HDMI + USB ──► จอ (ภาพ + touch)
แหล่งจ่ายไฟ UV ──► (TBD ตามแรงดันของหลอด)
```

## ตาราง GPIO

ค่าจริงอยู่ใน `backend/config/config.json` → `uv_gpio` (แก้ที่ config ได้โดยไม่ต้องแก้โค้ด)

| ช่อง | GPIO (BCM) | ขา header | รีเลย์ | ไฟ |
|---|---|---|---|---|
| UV 1 | 17 | 11 | ch1 | TBD |
| UV 2 | 27 | 13 | ch2 | TBD |
| UV 3 | 22 | 15 | ch3 | TBD |

## Open items

- [ ] **สเปกไฟ UV:** ความยาวคลื่น (nm), แรงดัน (V), กำลังไฟ (W) — ⚠️ ถ้าเป็น UV-C ต้องมี interlock ห้ามเปิดตอนมืออยู่ในเครื่อง
- [ ] รุ่นรีเลย์ / MOSFET และ active-high หรือ active-low
- [ ] แหล่งจ่ายไฟของ UV และของ Pi (Pi 5 ต้องใช้ 5V 5A)
