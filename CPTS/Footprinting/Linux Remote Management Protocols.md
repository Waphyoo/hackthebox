# สรุปสั้นๆ เรื่อง SSH และการจัดการระยะไกลของ Linux

## SSH คืออะไร?
**Secure Shell (SSH)** เป็นโปรโตคอลที่ให้คอมพิวเตอร์สองเครื่องเชื่อมต่อกันอย่างปลอดภัยผ่านเครือข่าย โดยใช้พอร์ต TCP 22 และมีการเข้ารหัสข้อมูลเพื่อป้องกันการดักฟัง

## SSH มี 2 เวอร์ชัน
- **SSH-1**: เวอร์ชันเก่า มีช่องโหว่ต่อการโจมตี MITM
- **SSH-2**: เวอร์ชันใหม่ ปลอดภัยกว่า เร็วกว่า เสถียรกว่า

## วิธีการยืนยันตัวตนหลักๆ
1. **รหัสผ่าน (Password)** - ง่ายแต่ต้องพิมพ์ทุกครั้ง
2. **คีย์สาธารณะ (Public Key)** - ปลอดภัยกว่า ใช้คู่คีย์สาธารณะ-ส่วนตัว ป้อน passphrase ครั้งเดียวต่อเซสชัน

## การตั้งค่าที่เป็นอันตราย ⚠️
- `PasswordAuthentication yes` - เสี่ยงต่อการ brute-force
- `PermitEmptyPasswords yes` - อนุญาตรหัสผ่านว่าง
- `PermitRootLogin yes` - อนุญาตให้ login เป็น root
- `Protocol 1` - ใช้การเข้ารหัสแบบเก่า
- `X11Forwarding yes` - เคยมีช่องโหว่

## ข้อควรระวัง
การตั้งค่า SSH ที่ไม่ถูกต้องอาจทำให้แฮกเกอร์เจาะเข้าระบบได้ง่าย โดยเฉพาะการใช้รหัสผ่านที่ง่ายหรือมีรูปแบบ (เช่น เติมตัวเลขท้ายรหัสผ่าน) ซึ่งสามารถเดาได้

# การสำรวจบริการ SSH (Footprinting)

## เครื่องมือสำรวจ: ssh-audit

**ssh-audit** เป็นเครื่องมือที่ใช้ตรวจสอบและวิเคราะห์เซิร์ฟเวอร์ SSH โดยจะแสดงข้อมูล:
- การกำหนดค่าฝั่งไคลเอนต์และเซิร์ฟเวอร์
- อัลกอริทึมการเข้ารหัสที่ใช้งานอยู่
- ช่องโหว่ด้านความปลอดภัยที่อาจมี

### ตัวอย่างผลการสแกน

เมื่อรันคำสั่ง:
```bash
./ssh-audit.py 10.129.14.132
```

**ข้อมูลที่ได้:**

**1. ข้อมูลทั่วไป (General)**
- Banner: `SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3`
- เวอร์ชัน OpenSSH และระบบปฏิบัติการ
- วิธีการบีบอัดข้อมูล

**2. อัลกอริทึมแลกเปลี่ยนคีย์ (Key Exchange)**
- ✅ `curve25519-sha256` - ปลอดภัย
- ❌ `ecdh-sha2-nistp256/384/521` - ใช้ elliptic curves ที่อ่อนแอ
- ℹ️ `diffie-hellman-group` ต่างๆ - ข้อมูลเพิ่มเติม

**3. อัลกอริทึม Host-Key**
- ✅ `rsa-sha2-512/256` - ปลอดภัย
- ❌ `ssh-rsa` - ใช้ hashing ที่อ่อนแอ
- ❌ `ecdsa-sha2-nistp256` - มีจุดอ่อนหลายจุด
- ✅ `ssh-ed25519` - แนะนำ

## การดูข้อมูลการเชื่อมต่อแบบละเอียด

ใช้คำสั่ง SSH พร้อม flag `-v` (verbose):

```bash
ssh -v cry0l1t3@10.129.14.132
```

**จะแสดง:**
- ขั้นตอนการเชื่อมต่อทั้งหมด
- วิธีการยืนยันตัวตนที่เซิร์ฟเวอร์รองรับ
- ตัวอย่าง: `publickey,password,keyboard-interactive`

## การระบุวิธียืนยันตัวตนสำหรับ Brute-Force

สามารถบังคับใช้วิธีการยืนยันตัวตนเฉพาะด้วย:

```bash
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password
```

คำสั่งนี้จะบังคับให้ใช้การยืนยันตัวตนด้วยรหัสผ่านเท่านั้น ซึ่งเป็นประโยชน์สำหรับการทดสอบ brute-force

## การอ่าน SSH Banner

**รูปแบบ Banner:**
- `SSH-1.99-OpenSSH_3.9p1` 
  - รองรับทั้ง SSH-1 และ SSH-2
  - เซิร์ฟเวอร์ OpenSSH เวอร์ชัน 3.9p1

- `SSH-2.0-OpenSSH_8.2p1`
  - รองรับเฉพาะ SSH-2
  - เซิร์ฟเวอร์ OpenSSH เวอร์ชัน 8.2p1

## ประโยชน์ของการ Footprinting

1. **ระบุช่องโหว่** - เช่น CVE-2020-14145 ที่ทำให้เกิดการโจมตี Man-In-The-Middle
2. **วางแผนการโจมตี** - เลือกวิธีโจมตีที่เหมาะสมตามการกำหนดค่า
3. **ทดสอบความปลอดภัย** - ตรวจสอบอัลกอริทึมที่อ่อนแอ

## คำแนะนำ

ควรทดลองติดตั้ง OpenSSH server บนเครื่อง VM ของตัวเองเพื่อทดลองกับการตั้งค่าต่างๆ และทำความเข้าใจกับตัวเลือกต่างๆ ก่อนทำการทดสอบจริง

# PreferredAuthentications=password - คืออะไร?

## คำอธิบาย

`PreferredAuthentications=password` เป็น **ตัวเลือก (option)** ของคำสั่ง SSH ที่ใช้เพื่อ**บังคับระบุวิธีการยืนยันตัวตน**ที่ต้องการใช้

## การใช้งาน

```bash
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password
```

**โครงสร้าง:**
- `-o` = ตัวเลือก (option)
- `PreferredAuthentications=password` = กำหนดให้ใช้การยืนยันตัวตนด้วยรหัสผ่าน

## ทำไมต้องใช้?

**ปกติ SSH จะลองวิธียืนยันตัวตนตามลำดับ:**
1. Public key (คีย์สาธารณะ) - ลองก่อน
2. Password (รหัสผ่าน) - ลองทีหลัง
3. Keyboard-interactive - ลองสุดท้าย

**แต่เมื่อระบุ `PreferredAuthentications=password`:**
- SSH จะ**ข้ามขั้นตอนอื่น** และใช้**รหัสผ่านทันที**
- ไม่พยายามใช้ public key ก่อน

## กรณีการใช้งาน

### 1. **การทดสอบ Brute-Force**
```bash
# เหมาะสำหรับการเดารหัสผ่าน
ssh -o PreferredAuthentications=password user@target
```

### 2. **เมื่อมี Key แต่ต้องการใช้รหัสผ่าน**
```bash
# บังคับใช้รหัสผ่านแม้ว่าจะมี SSH key ในเครื่อง
ssh -o PreferredAuthentications=password admin@server
```

### 3. **การทดสอบความปลอดภัย**
- ทดสอบว่าเซิร์ฟเวอร์อนุญาตให้ login ด้วยรหัสผ่านหรือไม่
- ตรวจสอบนโยบายการยืนยันตัวตน

## ตัวเลือกอื่นๆ ที่ใช้ได้

```bash
# ใช้เฉพาะ public key
-o PreferredAuthentications=publickey

# ใช้เฉพาะ keyboard-interactive
-o PreferredAuthentications=keyboard-interactive

# ใช้หลายวิธี (ลำดับความสำคัญ)
-o PreferredAuthentications=publickey,password
```

## สรุป

`PreferredAuthentications=password` ช่วยให้เรา**ควบคุมวิธีการยืนยันตัวตน**ได้อย่างชัดเจน มีประโยชน์มากในการทดสอบความปลอดภัย การ penetration testing และการแก้ไขปัญหาการเชื่อมต่อ SSH

# อธิบาย R-Services ให้เข้าใจง่าย 🔍

## R-Services คืออะไร? (แบบง่ายๆ)

ลองจินตนาการว่า **R-Services เป็นเหมือนประตูหลังบ้านที่ไม่มีกุญแจ** ในยุคก่อน (สมัยที่ยังไม่มี SSH)

**เปรียบเทียบ:**
- **SSH** = ประตูที่มีกุญแจดี มีระบบรักษาความปลอดภัย (เข้ารหัส)
- **R-Services** = ประตูเก่าๆ ที่ใช้ระบบ "คนที่บ้านรู้จักเข้าได้เลย" **ไม่เข้ารหัส**

---

## ทำไมเรียกว่า "R"-Services?

**"R" = Remote** (ระยะไกล)

เป็นชุดคำสั่งที่ขึ้นต้นด้วย `r` เช่น:
- **r**login = remote login (เข้าสู่ระบบระยะไกล)
- **r**sh = remote shell (เปิดเชลล์ระยะไกล)
- **r**cp = remote copy (คัดลอกไฟล์ระยะไกล)

---

## มันทำงานยังไง? (แบบง่าย)

### ระบบ "คนรู้จัก" (Trusted Hosts)

คิดว่าคุณมีสมุดโน้ตที่เขียนชื่อเพื่อนสนิท:

**ไฟล์ `/etc/hosts.equiv` หรือ `.rhosts`:**
```
เพื่อนชื่อ Bob จาก IP 192.168.1.100 → ไว้ใจได้ เข้าบ้านได้เลย
เพื่อนชื่อ Alice จาก IP 192.168.1.50 → ไว้ใจได้ เข้าบ้านได้เลย
```

**เมื่อ Bob พยายามเชื่อมต่อ:**
1. Bob: "สวัsdี ผม Bob จาก 192.168.1.100"
2. เซิร์ฟเวอร์: *เช็คในสมุดโน้ต* "โอ้ Bob! เข้ามาได้เลยไม่ต้องใส่รหัสผ่าน"
3. Bob เข้าระบบได้ทันที ✅

---

## ปัญหาคืออะไร? ⚠️

### 1. **ไม่เข้ารหัส** 
```
Bob → "username: bob, password: 12345" → เซิร์ฟเวอร์
     ↑ คนกลางทาง (hacker) อ่านได้หมด!
```

เหมือนส่งจดหมายไม่ใส่ซอง คนระหว่างทางอ่านได้หมด

### 2. **ระบบไว้วางใจผิดพลาดได้ง่าย**

ถ้าเขียนในไฟล์แบบนี้:
```
+    +
```

แปลว่า: **"ทุกคน (+) จากทุกที่ (+) เข้าได้หมด"** 😱

---

## ตัวอย่างคำสั่งแต่ละตัว

### 1. **rlogin** - เข้าสู่ระบบ
```bash
rlogin 10.0.17.2 -l htb-student
```
**เหมือน:** SSH แต่ไม่ปลอดภัย

**ผลลัพธ์:**
```
[htb-student@localhost ~]$  ← เข้าระบบได้เลย!
```

---

### 2. **rsh** - รันคำสั่ง
```bash
rsh 10.0.17.2 ls -la
```
**เหมือน:** SSH แล้วพิมพ์คำสั่ง แต่ไม่ปลอดภัย

---

### 3. **rcp** - คัดลอกไฟล์
```bash
rcp file.txt 10.0.17.2:/home/user/
```
**เหมือน:** scp แต่ไม่ปลอดภัย

---

### 4. **rwho** - ดูใครออนไลน์
```bash
rwho

root         web01:pts/0    Dec 2 21:34
htb-student  workstn01:tty1 Dec 2 19:57
```
**เหมือน:** ดูว่าใครกำลังใช้งานคอมพิวเตอร์ไหนอยู่

---

## ทำไมแฮกเกอร์ชอบ? 🎯

### สถานการณ์การโจมตี:

**1. แฮกเกอร์สแกนเจอพอร์ต 512, 513, 514 เปิดอยู่**
```bash
nmap -p 512-514 target.com
```

**2. เช็คไฟล์ .rhosts ถ้าเจอแบบนี้:**
```
+    +    ← อนุญาตทุกคน!
```

**3. แฮกเกอร์ใช้ rlogin**
```bash
rlogin target.com
```
**ผลลัพธ์:** เข้าได้เลย ไม่ต้องรหัสผ่าน! 🚨

**4. รวบรวมข้อมูล**
```bash
rwho      ← ดูใครออนไลน์
rusers    ← ดูรายละเอียดผู้ใช้
```

---

## เปรียบเทียบ SSH vs R-Services

| คุณสมบัติ | SSH ✅ | R-Services ❌ |
|-----------|--------|---------------|
| **เข้ารหัส** | มี | ไม่มี |
| **รหัสผ่าน** | ต้องใส่เสมอ | ถ้า "trusted" ไม่ต้องใส่ |
| **ความปลอดภัย** | สูง | ต่ำมาก |
| **ยุคสมัย** | ใช้ตอนนี้ | เก่ามาก (1980s) |
| **พอร์ต** | 22 | 512, 513, 514 |

---

## พอร์ตที่ต้องจำ 📝

```
512 = rexec  (รันคำสั่ง)
513 = rlogin (เข้าสู่ระบบ)
514 = rsh    (remote shell)
```

**วิธีจำ:** **5-1-2**, **5-1-3**, **5-1-4** เรียงกันไป

---

## ทำไมยังต้องเรียนรู้ถ้ามันเก่า?

1. **ระบบเก่ายังใช้อยู่** - โรงงาน, ธนาคาร, รัฐบาล บางแห่งยังใช้ระบบเก่า
2. **Penetration Testing** - ถ้าเจอในการทดสอบ ต้องรู้วิธีโจมตี
3. **ความรู้พื้นฐาน** - เข้าใจประวัติศาสตร์ช่วยให้เข้าใจ SSH มากขึ้น

---

## สรุปสั้นๆ 🎯

**R-Services = วิธีเชื่อมต่อคอมพิวเตอร์ระยะไกลแบบเก่า**

**ข้อเสีย:**
- 🔓 ไม่เข้ารหัส (ดักฟังได้)
- 🚪 ใช้ระบบ "trusted hosts" (ตั้งค่าผิดพลาดได้ง่าย)
- 🕰️ เก่ามาก แต่ยังพบในระบบบางที่

**ทำไมต้องรู้จัก:**
- เพื่อโจมตีในการทดสอบความปลอดภัย
- เพื่อรู้ว่าต้องปิดถ้าเจอในระบบของเรา

**สิ่งที่ต้องจำ:**
- ใช้พอร์ต 512-514
- เช็คไฟล์ `.rhosts` และ `/etc/hosts.equiv`
- **อย่าใช้ในระบบจริง ใช้ SSH แทน!**

---

### มีอะไรที่ยังสงสัยไหมครับ? 😊

# อธิบายไฟล์ `.rhosts` และ `/etc/hosts.equiv` แบบละเอียด

## ไฟล์เหล่านี้คืออะไร? 📝

เป็นไฟล์ที่เก็บ**รายชื่อคนที่เชื่อถือได้** สำหรับ R-Services

**เปรียบเทียบ:**
- เหมือน**รายชื่อแขกVIP** ที่ไม่ต้องเช็คบัตรก็เข้างานปาร์ตี้ได้เลย
- เหมือน**รายชื่อเพื่อนสนิท** ที่มาบ้านไม่ต้องกดกริ่ง เข้ามาได้เลย

---

## ความแตกต่างระหว่าง 2 ไฟล์

| ไฟล์ | ขอบเขต | ตำแหน่ง | ใครใช้ |
|------|---------|---------|--------|
| **`/etc/hosts.equiv`** | **Global** (ทั้งระบบ) | `/etc/hosts.equiv` | ผู้ใช้ทุกคนในระบบ |
| **`.rhosts`** | **Per-user** (แต่ละคน) | `/home/username/.rhosts` | เฉพาะผู้ใช้คนนั้น |

---

## 1. `/etc/hosts.equiv` - ไฟล์ส่วนกลาง 🌐

### ตำแหน่ง:
```
/etc/hosts.equiv
```

### ใช้ทำอะไร?
**ตั้งค่าสำหรับผู้ใช้ทุกคนในระบบ**

### ตัวอย่างเนื้อหา:

```bash
# รูปแบบ: <hostname หรือ IP> <username>

pwnbox cry0l1t3
192.168.1.100 alice
web-server bob
```

### อ่านยังไง? 📖

**บรรทัดที่ 1:** `pwnbox cry0l1t3`
- ผู้ใช้ชื่อ **cry0l1t3** จากเครื่องชื่อ **pwnbox** 
- สามารถเข้าสู่ระบบนี้ได้โดย**ไม่ต้องใส่รหัสผ่าน**

**บรรทัดที่ 2:** `192.168.1.100 alice`
- ผู้ใช้ชื่อ **alice** จาก IP **192.168.1.100**
- เข้าได้เลยไม่ต้องรหัสผ่าน

**บรรทัดที่ 3:** `web-server bob`
- ผู้ใช้ชื่อ **bob** จากเครื่องชื่อ **web-server**
- เข้าได้เลยไม่ต้องรหัสผ่าน

---

## 2. `.rhosts` - ไฟล์ส่วนตัว 👤

### ตำแหน่ง:
```
/home/username/.rhosts
หรือ
~/.rhosts
```

### ใช้ทำอะไร?
**ตั้งค่าเฉพาะสำหรับผู้ใช้คนนั้นๆ เท่านั้น**

### ตัวอย่างเนื้อหา:

```bash
htb-student     10.0.17.5
+               10.0.17.10
+               +
```

### อ่านยังไง? 📖

**บรรทัดที่ 1:** `htb-student     10.0.17.5`
- ผู้ใช้ชื่อ **htb-student** จาก IP **10.0.17.5**
- สามารถ login เข้าบัญชีของเจ้าของไฟล์นี้ได้โดยไม่ต้องรหัสผ่าน

**บรรทัดที่ 2:** `+               10.0.17.10`
- **ผู้ใช้ทุกคน** (`+`) จาก IP **10.0.17.10**
- ใครก็ได้จาก IP นี้เข้าได้หมด! ⚠️

**บรรทัดที่ 3:** `+               +`
- **ผู้ใช้ทุกคน** (`+`) จาก**ทุกที่** (`+`)
- **อันตรายมาก! ใครก็เข้าได้หมด!** 🚨🚨🚨

---

## ตัวพิเศษ: เครื่องหมาย `+` (Wildcard)

`+` = **อะไรก็ได้** (wildcard)

### ตัวอย่างการใช้:

```bash
+    alice           # ผู้ใช้ alice จากเครื่องไหนก็ได้
bob  +               # ผู้ใช้ bob เข้าบัญชีใดก็ได้ในระบบนี้
+    +               # ทุกคนจากทุกที่ เข้าได้หมด (อันตรายสุด!)
```

---

## ตัวอย่างสถานการณ์จริง 🎬

### สถานการณ์ที่ 1: ตั้งค่าถูกต้อง ✅

**ไฟล์ `/home/john/.rhosts`:**
```bash
alice  192.168.1.50
```

**ความหมาย:**
- เฉพาะผู้ใช้ **alice** จาก IP **192.168.1.50** เท่านั้น
- ที่สามารถ login เป็น **john** โดยไม่ต้องรหัสผ่าน

**การใช้งาน:**
```bash
# alice ที่เครื่อง 192.168.1.50 พิมพ์:
rlogin server -l john

# เข้าได้เลย! ไม่ต้องใส่รหัสผ่าน
[john@server ~]$
```

---

### สถานการณ์ที่ 2: ตั้งค่าผิดพลาด ❌

**ไฟล์ `/home/admin/.rhosts`:**
```bash
+  +
```

**ความหมาย:**
- **ทุกคนจากทุกที่** สามารถ login เป็น **admin** ได้
- **ไม่ต้องรหัสผ่าน!**

**แฮกเกอร์ทำได้:**
```bash
# แฮกเกอร์จากที่ไหนก็ได้พิมพ์:
rlogin server -l admin

# เข้าได้ทันที!
[admin@server ~]$ whoami
admin
[admin@server ~]$ sudo su
[root@server ~]#  ← ได้เป็น root!
```

---

## ความสำคัญของแต่ละไฟล์ 🎯

### `/etc/hosts.equiv` - อิทธิพลกว้าง
```bash
# ถ้าเขียนแบบนี้:
hacker-pc  +

# หมายความว่า:
ผู้ใช้ทุกคนจากเครื่อง hacker-pc
สามารถเข้าเป็นผู้ใช้ทุกคนในระบบนี้ได้!
```

### `.rhosts` - เฉพาะบุคคล
```bash
# ถ้าไฟล์ /home/bob/.rhosts เขียน:
alice  192.168.1.50

# หมายความว่า:
เฉพาะ alice จาก 192.168.1.50
เข้าเป็น bob ได้เท่านั้น
ไม่กระทบผู้ใช้คนอื่น
```

---

## การตรวจสอบไฟล์เหล่านี้ 🔍

### 1. เช็คว่ามีไฟล์หรือไม่:
```bash
# เช็ค global
ls -la /etc/hosts.equiv

# เช็ค per-user
ls -la ~/.rhosts
ls -la /home/*/.rhosts
```

### 2. อ่านเนื้อหา:
```bash
cat /etc/hosts.equiv
cat ~/.rhosts
```

### 3. หาไฟล์ที่เป็นอันตราย:
```bash
# หา .rhosts ทั้งหมดในระบบ
find / -name .rhosts 2>/dev/null

# หาไฟล์ที่มี + +
grep -r "+ +" /home/*/.rhosts /etc/hosts.equiv 2>/dev/null
```

---

## ตัวอย่างการโจมตี (Penetration Testing) 🎯

### ขั้นตอนที่ 1: สแกนหา R-Services
```bash
nmap -p 512-514 target.com
```

### ขั้นตอนที่ 2: ลอง rlogin
```bash
rlogin target.com -l root
```

### ขั้นตอนที่ 3: ถ้าเข้าไม่ได้ ลองเดาจากข้อมูล
```bash
# ลองใช้ชื่อผู้ใช้ทั่วไป
rlogin target.com -l admin
rlogin target.com -l user
rlogin target.com -l backup
```

### ขั้นตอนที่ 4: ถ้าเข้าได้ ค้นหาไฟล์ config
```bash
cat /etc/hosts.equiv
cat ~/.rhosts
find /home -name .rhosts -exec cat {} \;
```

---

# SSH (Secure Shell) - คู่มือฉบับสมบูรณ์ 🔐

## SSH คืออะไร?

**SSH (Secure Shell)** = โปรโตคอลสำหรับเชื่อมต่อและจัดการคอมพิวเตอร์ระยะไกลอย่าง**ปลอดภัย**

**คุณสมบัติหลัก:**
- 🔒 **เข้ารหัสข้อมูลทั้งหมด** (encrypted)
- 🔑 **ยืนยันตัวตนได้หลายวิธี** (multiple authentication)
- 🚀 **รวดเร็วและเสถียร**
- 🌐 **ใช้ได้ทุก OS** (Linux, macOS, Windows)
- 🔐 **ปลอดภัยจาก Man-in-the-Middle**

---

## ข้อมูลพื้นฐาน 📊

| รายการ | รายละเอียด |
|--------|------------|
| **พอร์ตเริ่มต้น** | TCP 22 |
| **เวอร์ชัน** | SSH-1 (เก่า, ไม่ปลอดภัย), SSH-2 (ใช้ปัจจุบัน) |
| **ซอฟต์แวร์ยอดนิยม** | OpenSSH |
| **ระบบปฏิบัติการ** | Linux, macOS, Windows |

---

## SSH-1 vs SSH-2 ⚖️

| คุณสมบัติ | SSH-1 ❌ | SSH-2 ✅ |
|-----------|----------|----------|
| **ความปลอดภัย** | อ่อนแอ | แข็งแกร่ง |
| **MITM Attack** | มีช่องโหว่ | ปลอดภัย |
| **ความเร็ว** | ช้า | เร็ว |
| **เสถียรภาพ** | น้อย | สูง |
| **แนะนำ** | ❌ ไม่แนะนำ | ✅ ใช้ตัวนี้ |

---

## วิธีการยืนยันตัวตน (Authentication Methods) 🔑

OpenSSH รองรับ **6 วิธี:**

### 1. **Password Authentication** 🔑
```bash
ssh user@server
Password: ******
```
**ข้อดี:** ง่าย ไม่ต้องตั้งค่า  
**ข้อเสีย:** เสี่ยงต่อ brute-force, ต้องพิมพ์ทุกครั้ง

---

### 2. **Public Key Authentication** 🔐 (แนะนำสุด!)

**ทำงานยังไง?**

#### ขั้นตอนการตั้งค่า:

**1. สร้างคู่กุญแจ (Key Pair)**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"

# หรือใช้ RSA (ถ้า ed25519 ไม่รองรับ)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**ผลลัพธ์:**
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519): [Enter]
Enter passphrase (empty for no passphrase): ******  # ใส่รหัสป้องกันกุญแจ
Enter same passphrase again: ******
```

**ได้ 2 ไฟล์:**
- `~/.ssh/id_ed25519` = **Private Key** (กุญแจส่วนตัว) 🔴 **ห้ามแชร์!**
- `~/.ssh/id_ed25519.pub` = **Public Key** (กุญแจสาธารณะ) ✅ แชร์ได้

**2. คัดลอก Public Key ไปเซิร์ฟเวอร์**
```bash
ssh-copy-id user@server

# หรือทำแบบ manual
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**3. เชื่อมต่อโดยไม่ต้องพิมพ์รหัสผ่าน**
```bash
ssh user@server
Enter passphrase for key '/home/user/.ssh/id_ed25519': ******  # พิมพ์ครั้งเดียวต่อ session
```

#### กลไกการทำงาน:

```
1. Client: "ผมมี Public Key นะ"
2. Server: "โอเค ผมส่งโจทย์เข้ารหัสให้ (ใช้ Public Key เข้ารหัส)"
3. Client: "ผมถอดรหัสได้ด้วย Private Key นี่คำตอบ"
4. Server: "ถูกต้อง! เข้ามาได้"
```

**ข้อดี:**
- ✅ ปลอดภัยมาก
- ✅ ไม่ต้องพิมพ์รหัสผ่านทุกครั้ง (ใส่ passphrase ครั้งเดียวต่อ session)
- ✅ ป้องกัน brute-force ได้

**ข้อเสีย:**
- ⚠️ ต้องตั้งค่าก่อน
- ⚠️ ถ้า Private Key หาย ต้องสร้างใหม่

---

### 3. **Host-based Authentication** 🏠
ใช้ไฟล์ `/etc/ssh/shosts.equiv` (คล้าย R-Services แต่ปลอดภัยกว่า)

---

### 4. **Keyboard Interactive** ⌨️
แสดงคำถามท้าทาย (Challenge) เช่น OTP, Security Questions

---

### 5. **Challenge-Response** 🎯
ระบบท้าทาย-ตอบ เช่น Google Authenticator

---

### 6. **GSSAPI Authentication** 🎫
ใช้กับ Kerberos สำหรับองค์กรขนาดใหญ่

---

## คำสั่ง SSH พื้นฐาน 💻

### 1. เชื่อมต่อพื้นฐาน
```bash
ssh user@hostname
ssh user@192.168.1.100
ssh -p 2222 user@server  # ถ้าใช้พอร์ตอื่น
```

### 2. เชื่อมต่อแบบ Verbose (ดูรายละเอียด)
```bash
ssh -v user@server        # verbose
ssh -vv user@server       # มากขึ้น
ssh -vvv user@server      # มากที่สุด (debug)
```

### 3. ระบุวิธียืนยันตัวตน
```bash
# ใช้รหัสผ่านเท่านั้น
ssh -o PreferredAuthentications=password user@server

# ใช้ Public Key เท่านั้น
ssh -o PreferredAuthentications=publickey user@server

# ระบุไฟล์ Private Key
ssh -i ~/.ssh/my_key user@server
```

### 4. รันคำสั่งแล้วออก
```bash
ssh user@server "ls -la /home"
ssh user@server "df -h"
ssh user@server "uptime"
```

### 5. คัดลอกไฟล์ (SCP)
```bash
# คัดลอกไปเซิร์ฟเวอร์
scp file.txt user@server:/path/to/destination/

# คัดลอกจากเซิร์ฟเวอร์
scp user@server:/path/to/file.txt ./

# คัดลอกโฟลเดอร์ (recursive)
scp -r folder/ user@server:/path/
```

### 6. SFTP (Secure File Transfer Protocol)
```bash
sftp user@server

# คำสั่งใน SFTP:
sftp> ls              # ดูไฟล์บนเซิร์ฟเวอร์
sftp> lls             # ดูไฟล์ในเครื่องตัวเอง
sftp> get file.txt    # ดาวน์โหลด
sftp> put file.txt    # อัพโหลด
sftp> exit            # ออก
```

### 7. Port Forwarding (Tunneling)
```bash
# Local Port Forwarding
ssh -L 8080:localhost:80 user@server
# เข้า localhost:8080 จะไปที่ server:80

# Remote Port Forwarding
ssh -R 8080:localhost:80 user@server
# คนอื่นเข้า server:8080 จะมาที่เครื่องเรา:80

# Dynamic Port Forwarding (SOCKS Proxy)
ssh -D 1080 user@server
# ตั้งเบราว์เซอร์ใช้ SOCKS proxy localhost:1080
```

---

## ไฟล์การตั้งค่า SSH 📁

### ฝั่ง Client: `~/.ssh/config`

**ตัวอย่าง:**
```bash
# เซิร์ฟเวอร์ที่ใช้บ่อย
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/myserver_key

# เซิร์ฟเวอร์ทำงาน
Host work
    HostName work.example.com
    User employee123
    IdentityFile ~/.ssh/work_key
    
# ตั้งค่าทั่วไป
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**ใช้งาน:**
```bash
# แทนที่จะพิมพ์ยาวๆ:
ssh -p 2222 -i ~/.ssh/myserver_key admin@192.168.1.100

# เพียงแค่:
ssh myserver
```

---

### ฝั่ง Server: `/etc/ssh/sshd_config`

**ดูการตั้งค่าปัจจุบัน:**
```bash
cat /etc/ssh/sshd_config | grep -v "#" | sed -r '/^\s*$/d'
```

**ตัวอย่างการตั้งค่า:**
```bash
# พอร์ต
Port 22

# โปรโตคอล (ใช้แค่ SSH-2)
Protocol 2

# การยืนยันตัวตน
PermitRootLogin no                    # ห้าม login เป็น root
PasswordAuthentication yes            # อนุญาตรหัสผ่าน
PubkeyAuthentication yes              # อนุญาต Public Key
PermitEmptyPasswords no               # ห้ามรหัสผ่านว่าง

# ความปลอดภัย
X11Forwarding no                      # ปิด X11 (ไม่ต้องใช้ GUI)
AllowTcpForwarding no                 # ปิด TCP Forwarding
MaxAuthTries 3                        # ลองผิด 3 ครั้ง
LoginGraceTime 60                     # เวลา login 60 วินาที

# จำกัดผู้ใช้
AllowUsers alice bob                  # อนุญาตเฉพาะ alice, bob
DenyUsers hacker                      # ห้าม hacker
```

**รีสตาร์ทหลังแก้ไข:**
```bash
sudo systemctl restart sshd
# หรือ
sudo service ssh restart
```

---

## การตั้งค่าที่เป็นอันตราย ⚠️

| การตั้งค่า | ทำไมอันตราย | แก้ไข |
|------------|-------------|-------|
| `PasswordAuthentication yes` | เสี่ยง brute-force | ปิด ใช้ Public Key แทน |
| `PermitEmptyPasswords yes` | login ได้โดยไม่ต้องรหัส! | ตั้งเป็น `no` |
| `PermitRootLogin yes` | แฮกเกอร์ได้ root เลย | ตั้งเป็น `no` หรือ `prohibit-password` |
| `Protocol 1` | ใช้เวอร์ชันเก่าไม่ปลอดภัย | ตั้งเป็น `2` |
| `X11Forwarding yes` | เคยมีช่องโหว่ | ปิดถ้าไม่ใช้ GUI |
| `AllowTcpForwarding yes` | อาจถูกใช้เป็น tunnel | พิจารณาปิด |

---

## การเพิ่มความปลอดภัย 🛡️

### 1. เปลี่ยนพอร์ต
```bash
# แก้ไข /etc/ssh/sshd_config
Port 2222  # แทนที่ 22

# เชื่อมต่อ
ssh -p 2222 user@server
```

### 2. ใช้ Fail2Ban
```bash
# ติดตั้ง
sudo apt install fail2ban

# ตั้งค่า
sudo nano /etc/fail2ban/jail.local
```

**เนื้อหา:**
```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

### 3. ปิด Root Login
```bash
# แก้ไข /etc/ssh/sshd_config
PermitRootLogin no
```

### 4. ใช้เฉพาะ Public Key
```bash
# แก้ไข /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
```

### 5. ใช้ Two-Factor Authentication (2FA)
```bash
# ติดตั้ง Google Authenticator
sudo apt install libpam-google-authenticator

# ตั้งค่า
google-authenticator
```

### 6. จำกัด IP ที่เข้าได้
```bash
# ใช้ UFW Firewall
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw deny 22
```

---

## การตรวจสอบและ Footprinting 🔍

### 1. สแกนด้วย Nmap
```bash
nmap -p 22 -sV target.com

# ผลลัพธ์:
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu-4ubuntu0.3
```

### 2. ใช้ ssh-audit
```bash
git clone https://github.com/jtesta/ssh-audit.git
cd ssh-audit
./ssh-audit.py target.com
```

**ข้อมูลที่ได้:**
- เวอร์ชัน OpenSSH
- อัลกอริทึมการเข้ารหัส
- ช่องโหว่ที่ทราบ
- วิธียืนยันตัวตนที่รองรับ

### 3. เชื่อมต่อแบบ Verbose
```bash
ssh -vvv user@server

# ดูข้อมูล:
debug1: Authentications that can continue: publickey,password,keyboard-interactive
```

### 4. ทดสอบ Authentication Methods
```bash
# ลองใช้รหัสผ่าน
ssh -o PreferredAuthentications=password user@server

# ลองใช้ Public Key
ssh -o PreferredAuthentications=publickey user@server
```

---

## ตัวอย่างการใช้งานจริง 🎯

### สถานการณ์ 1: ตั้งค่า SSH Server ครั้งแรก

```bash
# 1. ติดตั้ง OpenSSH
sudo apt update
sudo apt install openssh-server

# 2. ตรวจสอบสถานะ
sudo systemctl status ssh

# 3. เปิดใช้งานอัตโนมัติ
sudo systemctl enable ssh

# 4. อนุญาต Firewall
sudo ufw allow ssh
# หรือ
sudo ufw allow 22/tcp
```

---

### สถานการณ์ 2: ตั้งค่า Public Key Authentication

**ฝั่ง Client:**
```bash
# 1. สร้าง Key
ssh-keygen -t ed25519

# 2. คัดลอกไป Server
ssh-copy-id user@server

# 3. ทดสอบ
ssh user@server
```

**ฝั่ง Server:**
```bash
# 1. ตรวจสอบ Public Key
cat ~/.ssh/authorized_keys

# 2. ตั้งค่าสิทธิ์ (สำคัญ!)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# 3. ปิด Password Auth (optional)
sudo nano /etc/ssh/sshd_config
# เปลี่ยนเป็น: PasswordAuthentication no

# 4. รีสตาร์ท
sudo systemctl restart sshd
```

---

### สถานการณ์ 3: SSH Tunnel สำหรับ Web Application

```bash
# เซิร์ฟเวอร์มี web service บนพอร์ต 8080 (ไม่เปิดออกภายนอก)
# ใช้ SSH Tunnel เพื่อเข้าถึง

ssh -L 9000:localhost:8080 user@server

# ตอนนี้เปิดเบราว์เซอร์:
http://localhost:9000  # จะเข้าถึง server:8080
```

---

## ปัญหาที่พบบ่อยและวิธีแก้ 🔧

### 1. Permission denied (publickey)
```bash
# สาเหตุ: สิทธิ์ไฟล์ผิด
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
```

### 2. Connection refused
```bash
# ตรวจสอบ SSH service ทำงานหรือไม่
sudo systemctl status sshd

# ตรวจสอบ Firewall
sudo ufw status
```

### 3. Too many authentication failures
```bash
# ลดจำนวน Key ที่ลอง
ssh -o IdentitiesOnly=yes -i ~/.ssh/specific_key user@server
```

### 4. Host key verification failed
```bash
# ลบ old key
ssh-keygen -R server_hostname

# หรือ
rm ~/.ssh/known_hosts
```

---

## เปรียบเทียบ SSH vs R-Services 🆚

| คุณสมบัติ | SSH ✅ | R-Services ❌ |
|-----------|--------|---------------|
| **เข้ารหัส** | ✅ เต็มรูปแบบ | ❌ ไม่เข้ารหัส |
| **ความปลอดภัย** | ✅ สูงมาก | ❌ ต่ำมาก |
| **MITM Protection** | ✅ มี | ❌ ไม่มี |
| **Authentication** | ✅ หลายวิธี | ❌ Trusted hosts only |
| **พอร์ต** | 22 | 512, 513, 514 |
| **ใช้ในปัจจุบัน** | ✅ แนะนำ | ❌ เลิกใช้แล้ว |

---

## สรุป TL;DR 📌

**SSH คือ:**
- 🔐 โปรโตคอลปลอดภัยสำหรับจัดการระบบระยะไกล
- 🔒 เข้ารหัสข้อมูลทั้งหมด
- 🔑 ใช้ Public Key Authentication (แนะนำสุด)
- 🚀 รวดเร็ว เสถียร ปลอดภัย

**คำสั่งสำคัญ:**
```bash
ssh user@server                 # เชื่อมต่อ
ssh-keygen                      # สร้าง key
ssh-copy-id user@server         # คัดลอก public key
scp file.txt user@server:/path  # คัดลอกไฟล์
```

**ความปลอดภัย:**
- ✅ ใช้ Public Key แทนรหัสผ่าน
- ✅ ปิด Root Login
- ✅ เปลี่ยนพอร์ตจาก 22
- ✅ ใช้ Fail2Ban
- ✅ ใช้ 2FA

---

