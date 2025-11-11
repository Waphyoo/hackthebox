# การโจมตีแบบ Spraying, Stuffing และ Default Credentials

## 1. Password Spraying

### คำอธิบาย
Password Spraying เป็นการโจมตีแบบ brute-force ที่ผู้โจมตี**ใช้รหัสผ่านเดียวกันทดสอบกับหลายๆ บัญชีผู้ใช้** เทคนิคนี้มีประสิทธิภาพสูงในสภาพแวดล้อมที่ผู้ใช้ได้รับรหัสผ่านเริ่มต้นหรือรหัสผ่านมาตรฐาน

### ตัวอย่างการใช้งาน

**สถานการณ์:** ถ้าทราบว่าผู้ดูแลระบบของบริษัทมักใช้รหัสผ่าน `ChangeMe123!` เมื่อสร้างบัญชีใหม่ เราสามารถ spray รหัสผ่านนี้ไปยังบัญชีผู้ใช้ทั้งหมด เพื่อหาบัญชีที่ยังไม่ได้เปลี่ยนรหัสผ่าน

### เครื่องมือที่ใช้

**ตามประเภทของระบบ:**
- **Web Applications** → Burp Suite
- **Active Directory** → NetExec หรือ Kerbrute

### ตัวอย่างคำสั่ง

```bash
netexec smb 10.100.38.0/24 -u <usernames.list> -p 'ChangeMe123!'
```

**อธิบาย:**
- Spray รหัสผ่าน `ChangeMe123!` ไปยังทุก IP ใน subnet 10.100.38.0/24
- ใช้รายชื่อผู้ใช้จากไฟล์ `usernames.list`
- ทดสอบผ่าน SMB protocol

---

## 2. Credential Stuffing

### คำอธิบาย
Credential Stuffing เป็นการโจมตีแบบ brute-force ที่ผู้โจมตี**ใช้ credentials ที่ถูกขะโมยมาจากบริการหนึ่ง เพื่อพยายามเข้าถึงบริการอื่นๆ**

### เหตุผลที่ได้ผล
ผู้ใช้หลายคน**ใช้ username และ password เดียวกันในหลายแพลตฟอร์ม** เช่น:
- อีเมล
- โซเชียลมีเดีย
- ระบบองค์กร

### ตัวอย่างการใช้งาน

**สถานการณ์:** เราได้รายการ `username:password` จากการรั่วไหลข้อมูล (database leak) และต้องการทดสอบกับบริการ SSH

```bash
hydra -C user_pass.list ssh://10.100.38.23
```

**อธิบาย:**
- `-C` = ใช้ไฟล์ที่มีรูปแบบ `username:password` (colon-separated)
- `user_pass.list` = ไฟล์ที่เก็บ credentials ที่รั่วไหลมา
- ทดสอบกับ SSH service ที่ IP 10.100.38.23

---

## 3. Default Credentials

### คำอธิบาย
ระบบหลายประเภทมาพร้อมกับ **credentials เริ่มต้น** เช่น:
- Router
- Firewall
- ฐานข้อมูล

### ปัญหาความปลอดภัย
แม้ว่า best practice จะแนะนำให้เปลี่ยน credentials เหล่านี้ แต่บางครั้ง**ผู้ดูแลระบบลืมเปลี่ยน** ทำให้เกิดช่องโหว่ความปลอดภัยร้ายแรง

---

## เครื่องมือตรวจสอบ Default Credentials

### Default Credentials Cheat Sheet

**การติดตั้ง:**
```bash
pip3 install defaultcreds-cheat-sheet
```

**การใช้งาน:**
```bash
creds search linksys
```

**ผลลัพธ์:**
```
+---------------+---------------+------------+
| Product       |    username   |  password  |
+---------------+---------------+------------+
| linksys       |    <blank>    |  <blank>   |
| linksys       |    <blank>    |   admin    |
| linksys       |    <blank>    | epicrouter |
| linksys       | Administrator |   admin    |
| linksys       |     admin     |  <blank>   |
| linksys       |     admin     |   admin    |
| linksys       |    comcast    |    1234    |
| linksys       |      root     |  orion99   |
| linksys       |      user     |  tivonpw   |
| linksys (ssh) |     admin     |   admin    |
| linksys (ssh) |     admin     |  password  |
| linksys (ssh) |    linksys    |  <blank>   |
| linksys (ssh) |      root     |   admin    |
+---------------+---------------+------------+
```

---

## แหล่งข้อมูล Default Credentials

### 1. **รายการสาธารณะ**
- Default Credentials Cheat Sheet
- รายการ default credentials ของ router ต่างๆ

### 2. **เอกสารผลิตภัณฑ์**
- คู่มือการติดตั้ง
- เอกสาร setup ที่ระบุ default password

### 3. **พฤติกรรมของระบบ**
- บางระบบบังคับให้ตั้งรหัสผ่านตอนติดตั้ง
- บางระบบใช้รหัสผ่านเริ่มต้น (มักจะอ่อนแอ)

---

## วิธีการโจมตีด้วย Default Credentials

### ขั้นตอน:

1. **ระบุ Applications ที่ใช้ในเครือข่าย**
2. **ค้นหา default credentials ออนไลน์**
3. **สร้างรายการในรูปแบบ `username:password`**
4. **ใช้ Hydra ทดสอบ:**

```bash
hydra -C default_creds.list ssh://target-ip
```

---
https://www.softwaretestinghelp.com/default-router-username-and-password-list/

## ตัวอย่าง Default Credentials ของ Router

| Router Brand | Default IP | Default Username | Default Password |
|-------------|------------|------------------|------------------|
| **3Com** | 192.168.1.1 | admin | Admin |
| **Belkin** | 192.168.2.1 | admin | admin |
| **BenQ** | 192.168.1.1 | admin | Admin |
| **D-Link** | 192.168.0.1 | admin | Admin |
| **Digicom** | 192.168.1.254 | admin | Michelangelo |
| **Linksys** | 192.168.1.1 | admin | Admin |
| **Netgear** | 192.168.0.1 | admin | password |

---

## กรณีพิเศษ: Router ในสภาพแวดล้อมทดสอบ

### ความเสี่ยง
แม้ router credentials มักจะถูกเปลี่ยน (เพราะเป็นอุปกรณ์สำคัญต่อความปลอดภัยเครือข่าย) แต่ก็ยังมีช่องโหว่:

**Router ในสภาพแวดล้อมทดสอบภายใน (Internal Testing):**
- อาจถูกทิ้งไว้ด้วย default settings
- สามารถถูก exploit เพื่อเข้าถึงระบบเพิ่มเติม

---

