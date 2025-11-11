# John The Ripper - เครื่องมือถอดรหัสผ่าน

## ข้อมูลทั่วไป

**John the Ripper (JtR)** เป็นเครื่องมือ Penetration Testing ที่มีชื่อเสียงสำหรับถอดรหัสผ่านด้วยเทคนิคต่างๆ รวมถึง Brute-force และ Dictionary Attack

### ประวัติและคุณสมบัติ
- เป็นซอฟต์แวร์โอเพนซอร์ส
- พัฒนาสำหรับระบบ UNIX
- เปิดตัวครั้งแรกในปี **1996**
- เป็นเครื่องมือหลักของอุตสาหกรรมความปลอดภัย

### John the Ripper "Jumbo" Version (แนะนำ)
**คุณสมบัติพิเศษ:**
- ปรับปรุงประสิทธิภาพ
- รองรับ Wordlist หลายภาษา
- รองรับสถาปัตยกรรม 64-bit
- ถอดรหัสได้แม่นยำและเร็วกว่า
- มีเครื่องมือแปลงไฟล์และ Hash หลายรูปแบบ
- อัปเดตเป็นประจำตามเทรนด์ความปลอดภัยปัจจุบัน

---

## โหมดการถอดรหัส (Cracking Modes)

### 1. Single Crack Mode

**คำนิยาม:**
โหมดที่ใช้กฎ (Rule-based) เหมาะสำหรับถอดรหัส Linux credentials โดยสร้างรหัสผ่านผู้ใช้จากข้อมูลต่างๆ

**ข้อมูลที่ใช้สร้างรหัสผ่านคาดเดา:**
- ชื่อผู้ใช้ (Username)
- ชื่อไดเรกทอรีหลัก (Home directory)
- ค่า GECOS (ชื่อเต็ม, เลขห้อง, เบอร์โทรศัพท์)

**การทำงาน:**
สตริงเหล่านี้จะถูกประมวลผลด้วยกฎที่ใช้การแปลงสตริงทั่วไปในรหัสผ่าน

**ตัวอย่าง:**
ผู้ใช้ชื่อ Bob Smith อาจใช้รหัสผ่านเช่น `Smith1`

### ตัวอย่างการใช้งาน Single Crack Mode

**ไฟล์ passwd:**
```
r0lf:$6$ues25dIanlctrWxg$nZHVz2z4kCy1760Ee28M1xtHdGoy0C2cYzZ8l2sVa1kIa8K9gAcdBP.GI6ng/qA4oaMrgElZ1Cb9OeXO4Fvy3/:0:0:Rolf Sebastian:/home/r0lf:/bin/bash
```

**ข้อมูลที่สามารถสกัดได้:**
- Username: `r0lf`
- ชื่อจริง: `Rolf Sebastian`
- Home directory: `/home/r0lf`

**คำสั่งโจมตี:**
```bash
john --single passwd
```

**ผลลัพธ์:**
```
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
[...SNIP...]        (r0lf)     
1g 0:00:00:00 DONE 1/3 (2025-04-10 07:47) 12.50g/s 5400p/s 5400c/s 5400C/s NAITSABESFL0R..rSebastiannaitsabeSr
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

✅ **ถอดรหัสสำเร็จ!**

---

### 2. Wordlist Mode

**คำนิยาม:**
ใช้ถอดรหัสผ่านด้วย Dictionary Attack โดยลองรหัสผ่านทั้งหมดจาก Wordlist กับ Hash ที่เป็นเป้าหมาย

**รูปแบบคำสั่งพื้นฐาน:**
```bash
john --wordlist=<wordlist_file> <hash_file>
```

**ข้อกำหนด Wordlist:**
- ต้องเป็นไฟล์ plain text
- หนึ่งคำต่อหนึ่งบรรทัด
- สามารถระบุหลายไฟล์โดยคั่นด้วยจุลภาค (,)

**การใช้ Rules:**
```bash
john --wordlist=<wordlist_file> --rules <hash_file>
```

**Rules ทำอะไรได้บ้าง:**
- เพิ่มตัวเลขต่อท้าย
- เปลี่ยนตัวอักษรเป็นตัวพิมพ์ใหญ่
- เพิ่มอักขระพิเศษ

**ตัวอย่าง:**
- รหัสผ่านต้นฉบับ: `password`
- หลัง Rules: `Password1`, `P@ssword`, `PASSWORD123`

---

### 3. Incremental Mode

**คำนิยาม:**
โหมดการถอดรหัสแบบ Brute-force ที่ทรงพลัง สร้างรหัสผ่านผู้สมัครจากโมเดลทางสถิติ (Markov chains)

**คุณสมบัติเด่น:**
- ทดสอบทุกการจัดเรียงอักขระที่เป็นไปได้
- จัดลำดับความสำคัญตามข้อมูลการเทรนนิ่ง
- **ไม่ต้องใช้ Wordlist** (สร้างรหัสผ่านเอง)
- ใช้โมเดลทางสถิติ ไม่ใช่การสุ่มแบบ Brute-force ล้วนๆ
- มีประสิทธิภาพสูงกว่า Brute-force ทั่วไป

**ข้อเสีย:**
- ครอบคลุมมากที่สุด แต่ใช้เวลานานที่สุด
- กินทรัพยากรระบบสูง โดยเฉพาะรหัสผ่านยาวและซับซ้อน

**รูปแบบคำสั่งพื้นฐาน:**
```bash
john --incremental <hash_file>
```

### การตั้งค่า Incremental Mode

**ดูการตั้งค่าใน john.conf:**
```bash
grep '# Incremental modes' -A 100 /etc/john/john.conf
```

**ตัวอย่างการตั้งค่าที่มีอยู่:**

```
# Incremental modes

# สำหรับใช้ครั้งเดียว (สร้าง custom.chr เอง)
[Incremental:Custom]
File = $JOHN/custom.chr
MinLen = 0

# CharCount ทฤษฎี = 211, ที่มีจริง = 196
[Incremental:UTF8]
File = $JOHN/utf8.chr
MinLen = 0
CharCount = 196

# นี่คือ CP1252, super-set ของ ISO-8859-1
# CharCount ทฤษฎี = 219, ที่มีจริง = 203
[Incremental:Latin1]
File = $JOHN/latin1.chr
MinLen = 0
CharCount = 203

# ASCII มาตรฐาน
[Incremental:ASCII]
File = $JOHN/ascii.chr
MinLen = 0
MaxLen = 13
CharCount = 95

...SNIP...
```

**พารามิเตอร์สำคัญ:**
- **File:** ไฟล์ character set ที่ใช้
- **MinLen:** ความยาวรหัสผ่านขั้นต่ำ
- **MaxLen:** ความยาวรหัสผ่านสูงสุด
- **CharCount:** จำนวนตัวอักษรที่ใช้

**การปรับแต่ง:**
สามารถกำหนด character set และความยาวรหัสผ่านเองเพื่อเพิ่มประสิทธิภาพ

---

## การระบุรูปแบบ Hash (Identifying Hash Formats)

### ปัญหาที่พบ
บางครั้ง Hash อาจอยู่ในรูปแบบที่ไม่รู้จัก แม้แต่ JtR ก็ไม่สามารถระบุได้อย่างแน่นอน

**ตัวอย่าง Hash:**
```
193069ceb0461e1d40d216e32c79c704
```

### เครื่องมือช่วยระบุ Hash

#### 1. เอกสารตัวอย่าง Hash
- เอกสารของ JtR
- รายการจาก PentestMonkey
- แสดงตัวอย่าง Hash และรูปแบบ JtR ที่สอดคล้อง

#### 2. hashID Tool

**คำสั่ง:**
```bash
hashid -j 193069ceb0461e1d40d216e32c79c704
```

**Flag `-j`:** แสดงรูปแบบ JtR ด้วย

**ผลลัพธ์:**
```
Analyzing '193069ceb0461e1d40d216e32c79c704'
[+] MD2 [JtR Format: md2]
[+] MD5 [JtR Format: raw-md5]
[+] MD4 [JtR Format: raw-md4]
[+] Double MD5 
[+] LM [JtR Format: lm]
[+] RIPEMD-128 [JtR Format: ripemd-128]
[+] Haval-128 [JtR Format: haval-128-4]
[+] Tiger-128 
[+] Skein-256(128) 
[+] Skein-512(128) 
[+] Lotus Notes/Domino 5 [JtR Format: lotus5]
[+] Skype 
[+] Snefru-128 [JtR Format: snefru-128]
[+] NTLM [JtR Format: nt]
[+] Domain Cached Credentials [JtR Format: mscach]
[+] Domain Cached Credentials 2 [JtR Format: mscach2]
[+] DNSSEC(NSEC3) 
[+] RAdmin v2.x [JtR Format: radmin]
```

**สังเกต:**
- ยังไม่ชัดเจนว่าเป็น Hash รูปแบบไหน
- ต้องพิจารณาจาก **บริบท** ที่พบ Hash
- ในตัวอย่างนี้ รูปแบบที่ถูกคือ **RIPEMD-128**

---

## รูปแบบ Hash ที่ JtR รองรับ

JtR รองรับ Hash หลายร้อยรูปแบบ สามารถระบุด้วย `--format`

### ตารางรูปแบบ Hash ยอดนิยม

| Hash Format | คำสั่งตัวอย่าง | คำอธิบาย |
|-------------|----------------|----------|
| **afs** | `john --format=afs <hash_file>` | AFS (Andrew File System) password hashes |
| **bfegg** | `john --format=bfegg <hash_file>` | bfegg hashes ใช้ใน Eggdrop IRC bots |
| **bf** | `john --format=bf <hash_file>` | Blowfish-based crypt(3) hashes |
| **bsdi** | `john --format=bsdi <hash_file>` | BSDi crypt(3) hashes |
| **crypt(3)** | `john --format=crypt <hash_file>` | Traditional Unix crypt(3) hashes |
| **des** | `john --format=des <hash_file>` | Traditional DES-based crypt(3) hashes |
| **dmd5** | `john --format=dmd5 <hash_file>` | DMD5 (Dragonfly BSD MD5) password hashes |
| **dominosec** | `john --format=dominosec <hash_file>` | IBM Lotus Domino 6/7 password hashes |
| **episerver** | `john --format=episerver <hash_file>` | EPiServer SID password hashes |
| **hdaa** | `john --format=hdaa <hash_file>` | hdaa password hashes ใน Openwall GNU/Linux |
| **hmac-md5** | `john --format=hmac-md5 <hash_file>` | hmac-md5 password hashes |
| **hmailserver** | `john --format=hmailserver <hash_file>` | hmailserver password hashes |
| **ipb2** | `john --format=ipb2 <hash_file>` | Invision Power Board 2 password hashes |
| **krb4** | `john --format=krb4 <hash_file>` | Kerberos 4 password hashes |
| **krb5** | `john --format=krb5 <hash_file>` | Kerberos 5 password hashes |
| **LM** | `john --format=LM <hash_file>` | LM (Lan Manager) password hashes |
| **lotus5** | `john --format=lotus5 <hash_file>` | Lotus Notes/Domino 5 password hashes |
| **mscash** | `john --format=mscash <hash_file>` | MS Cache password hashes |
| **mscash2** | `john --format=mscash2 <hash_file>` | MS Cache v2 password hashes |
| **mschapv2** | `john --format=mschapv2 <hash_file>` | MS CHAP v2 password hashes |
| **mskrb5** | `john --format=mskrb5 <hash_file>` | MS Kerberos 5 password hashes |
| **mssql05** | `john --format=mssql05 <hash_file>` | MS SQL 2005 password hashes |
| **mssql** | `john --format=mssql <hash_file>` | MS SQL password hashes |
| **mysql-fast** | `john --format=mysql-fast <hash_file>` | MySQL fast password hashes |
| **mysql** | `john --format=mysql <hash_file>` | MySQL password hashes |
| **mysql-sha1** | `john --format=mysql-sha1 <hash_file>` | MySQL SHA1 password hashes |
| **NETLM** | `john --format=netlm <hash_file>` | NETLM (NT LAN Manager) password hashes |
| **NETLMv2** | `john --format=netlmv2 <hash_file>` | NETLMv2 password hashes |
| **NETNTLM** | `john --format=netntlm <hash_file>` | NETNTLM password hashes |
| **NETNTLMv2** | `john --format=netntlmv2 <hash_file>` | NETNTLMv2 password hashes |
| **NEThalfLM** | `john --format=nethalflm <hash_file>` | NEThalfLM password hashes |
| **md5ns** | `john --format=md5ns <hash_file>` | md5ns (MD5 namespace) password hashes |
| **nsldap** | `john --format=nsldap <hash_file>` | nsldap (OpenLDAP SHA) password hashes |
| **ssha** | `john --format=ssha <hash_file>` | ssha (Salted SHA) password hashes |
| **NT** | `john --format=nt <hash_file>` | NT (Windows NT) password hashes |
| **openssha** | `john --format=openssha <hash_file>` | OPENSSH private key password hashes |
| **oracle11** | `john --format=oracle11 <hash_file>` | Oracle 11 password hashes |
| **oracle** | `john --format=oracle <hash_file>` | Oracle password hashes |
| **pdf** | `john --format=pdf <hash_file>` | PDF password hashes |
| **phpass-md5** | `john --format=phpass-md5 <hash_file>` | PHPass-MD5 password hashes |
| **phps** | `john --format=phps <hash_file>` | PHPS password hashes |
| **pix-md5** | `john --format=pix-md5 <hash_file>` | Cisco PIX MD5 password hashes |
| **po** | `john --format=po <hash_file>` | Po (Sybase SQL Anywhere) password hashes |
| **rar** | `john --format=rar <hash_file>` | RAR (WinRAR) password hashes |
| **raw-md4** | `john --format=raw-md4 <hash_file>` | Raw MD4 password hashes |
| **raw-md5** | `john --format=raw-md5 <hash_file>` | Raw MD5 password hashes |
| **raw-md5-unicode** | `john --format=raw-md5-unicode <hash_file>` | Raw MD5 Unicode password hashes |
| **raw-sha1** | `john --format=raw-sha1 <hash_file>` | Raw SHA1 password hashes |
| **raw-sha224** | `john --format=raw-sha224 <hash_file>` | Raw SHA224 password hashes |
| **raw-sha256** | `john --format=raw-sha256 <hash_file>` | Raw SHA256 password hashes |
| **raw-sha384** | `john --format=raw-sha384 <hash_file>` | Raw SHA384 password hashes |
| **raw-sha512** | `john --format=raw-sha512 <hash_file>` | Raw SHA512 password hashes |
| **salted-sha** | `john --format=salted-sha <hash_file>` | Salted SHA password hashes |
| **sapb** | `john --format=sapb <hash_file>` | SAP CODVN B (BCODE) password hashes |
| **sapg** | `john --format=sapg <hash_file>` | SAP CODVN G (PASSCODE) password hashes |
| **sha1-gen** | `john --format=sha1-gen <hash_file>` | Generic SHA1 password hashes |
| **skey** | `john --format=skey <hash_file>` | S/Key (One-time password) hashes |
| **ssh** | `john --format=ssh <hash_file>` | SSH (Secure Shell) password hashes |
| **sybasease** | `john --format=sybasease <hash_file>` | Sybase ASE password hashes |
| **xsha** | `john --format=xsha <hash_file>` | xsha (Extended SHA) password hashes |
| **zip** | `john --format=zip <hash_file>` | ZIP (WinZip) password hashes |

---

## การถอดรหัสไฟล์ (Cracking Files)

JtR สามารถถอดรหัสไฟล์ที่มีการป้องกันด้วยรหัสผ่านหรือเข้ารหัส

### เครื่องมือ "2john"

**รูปแบบคำสั่งทั่วไป:**
```bash
<tool> <file_to_crack> > file.hash
```

### ตารางเครื่องมือ 2john ที่มาพร้อม JtR

| เครื่องมือ | คำอธิบาย |
|-----------|----------|
| **pdf2john** | แปลงเอกสาร PDF สำหรับ John |
| **ssh2john** | แปลง SSH private keys สำหรับ John |
| **mscash2john** | แปลง MS Cash hashes สำหรับ John |
| **keychain2john** | แปลงไฟล์ OS X keychain สำหรับ John |
| **rar2john** | แปลงไฟล์ RAR archives สำหรับ John |
| **pfx2john** | แปลงไฟล์ PKCS#12 สำหรับ John |
| **truecrypt_volume2john** | แปลง TrueCrypt volumes สำหรับ John |
| **keepass2john** | แปลงฐานข้อมูล KeePass สำหรับ John |
| **vncpcap2john** | แปลงไฟล์ VNC PCAP สำหรับ John |
| **putty2john** | แปลง PuTTY private keys สำหรับ John |
| **zip2john** | แปลงไฟล์ ZIP archives สำหรับ John |
| **hccap2john** | แปลง WPA/WPA2 handshake captures สำหรับ John |
| **office2john** | แปลงเอกสาร MS Office สำหรับ John |
| **wpa2john** | แปลง WPA/WPA2 handshakes สำหรับ John |

### รายการเครื่องมือเพิ่มเติมใน Pwnbox

**คำสั่งค้นหา:**
```bash
locate *2john*
```

**ผลลัพธ์:**
```
/usr/bin/bitlocker2john
/usr/bin/dmg2john
/usr/bin/gpg2john
/usr/bin/hccap2john
/usr/bin/keepass2john
/usr/bin/putty2john
/usr/bin/racf2john
/usr/bin/rar2john
/usr/bin/uaf2john
/usr/bin/vncpcap2john
/usr/bin/wlanhcx2john
/usr/bin/wpapcap2john
/usr/bin/zip2john
/usr/share/john/1password2john.py
/usr/share/john/7z2john.pl
/usr/share/john/DPAPImk2john.py
/usr/share/john/adxcsouf2john.py
/usr/share/john/aem2john.py
/usr/share/john/aix2john.pl
/usr/share/john/aix2john.py
/usr/share/john/andotp2john.py
/usr/share/john/androidbackup2john.py
...SNIP...
```

