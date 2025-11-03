# Windows Remote Management Protocols

## ภาพรวม
Windows servers สามารถจัดการได้ทั้งแบบภายในเครื่อง (locally) โดยใช้ Server Manager หรือจัดการระยะไหล (remotely) ได้ โดยตั้งแต่ Windows Server 2016 เป็นต้นมา ระบบจะเปิดใช้งานการจัดการระยะไหลโดยอัตโนมัติ

ฟีเจอร์การจัดการระยะไหลนี้ประกอบด้วย:
- บริการที่รองรับโปรโตคอล WS-Management
- การวินิจฉัยและควบคุมฮาร์ดแวร์ผ่าน baseboard management controllers
- COM API และ script objects สำหรับเขียนโปรแกรมสื่อสารระยะไหลผ่าน WS-Management

## ส่วนประกอบหลักสำหรับการจัดการระยะไหล

มี 3 ส่วนหลักที่ใช้จัดการ Windows และ Windows servers ระยะไหล:

### 1. **Remote Desktop Protocol (RDP)**
RDP เป็นโปรโตคอลที่ Microsoft พัฒนาขึ้นสำหรับการเข้าถึงเครื่อง Windows ระยะไหล โปรโตคอลนี้ทำให้สามารถส่งคำสั่งแสดงผลและควบคุมผ่าน GUI ที่เข้ารหัสผ่านเครือข่าย IP

**คุณสมบัติสำคัญ:**
- ทำงานที่ application layer ในโมเดล TCP/IP
- ใช้พอร์ต TCP 3389 เป็นหลัก (หรือใช้ UDP พอร์ต 3389 ก็ได้)
- รองรับการเข้ารหัส TLS/SSL ตั้งแต่ Windows Vista เป็นต้นมา

**ข้อกำหนดในการเชื่อมต่อ:**
- ไฟร์วอลล์ทั้งของเครือข่ายและเซิร์ฟเวอร์ต้องอนุญาตการเชื่อมต่อจากภายนอก
- หากใช้ NAT ต้องมี public IP address และตั้งค่า port forwarding
- ต้องเปิดใช้งาน Network Level Authentication (NLA) ตามค่าเริ่มต้น

**ข้อควรระวังด้านความปลอดภัย:**
แม้ว่า RDP จะรองรับ TLS/SSL แต่หลายระบบยังคงยอมรับการเข้ารหัสที่ไม่เพียงพอผ่าน RDP Security นอกจากนี้ certificate ที่ใช้มักเป็น self-signed ทำให้ผู้ใช้ไม่สามารถแยกแยะ certificate ปลอมจากของจริงได้ ระบบจึงแสดงคำเตือนให้ผู้ใช้

**การติดตั้ง:**
Remote Desktop service ติดตั้งมาให้โดยค่าเริ่มต้นบน Windows servers ไม่ต้องใช้โปรแกรมเพิ่มเติม สามารถเปิดใช้งานผ่าน Server Manager ได้เลย

### 2. **Windows Remote Management (WinRM)**
ระบบจัดการระยะไหลของ Windows ที่ใช้โปรโตคอล WS-Management

### 3. **Windows Management Instrumentation (WMI)**
เครื่องมือสำหรับจัดการและดูแลระบบ Windows

---
# การสำรวจและทดสอบ RDP Service

เอกสารนี้อธิบายวิธีการสำรวจ (Footprinting) และทดสอบบริการ RDP เพื่อรวบรวมข้อมูลเกี่ยวกับเซิร์ฟเวอร์เป้าหมาย

## 1. การสแกนด้วย Nmap

### การสแกนพื้นฐาน
คำสั่ง Nmap สามารถให้ข้อมูลมากมายเกี่ยวกับเซิร์ฟเวอร์ RDP เช่น:
- สถานะการเปิดใช้งาน NLA (Network Level Authentication)
- เวอร์ชันของผลิตภัณฑ์
- ชื่อโฮสต์ (hostname)

```bash
Watunyoo@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --script rdp*

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 15:45 CET
Nmap scan report for 10.129.201.248
Host is up (0.036s latency).

PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-enum-encryption: 
|   Security layer
|     CredSSP (NLA): SUCCESS
|     CredSSP with Early User Auth: SUCCESS
|_    RDSTLS: SUCCESS
| rdp-ntlm-info: 
|   Target_Name: ILF-SQL-01
|   NetBIOS_Domain_Name: ILF-SQL-01
|   NetBIOS_Computer_Name: ILF-SQL-01
|   DNS_Domain_Name: ILF-SQL-01
|   DNS_Computer_Name: ILF-SQL-01
|   Product_Version: 10.0.17763
|_  System_Time: 2021-11-06T13:46:00+00:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.26 seconds
```

**ข้อมูลที่ได้จากการสแกน:**
- **Security Layer**: ระบุว่ารองรับ CredSSP (NLA), CredSSP with Early User Auth, และ RDSTLS หรือไม่
- **ข้อมูล NTLM**: ชื่อเป้าหมาย, ชื่อโดเมน NetBIOS, ชื่อคอมพิวเตอร์, เวอร์ชันผลิตภัณฑ์, และเวลาของระบบ
- **ข้อมูลระบบปฏิบัติการ**: ระบุว่าเป็น Windows

### การติดตามแพ็กเก็ต (Packet Tracing)

ใช้ `--packet-trace` เพื่อติดตามและตรวจสอบแพ็กเก็ตแต่ละตัว:

```bash
Watunyoo@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 16:23 CET
SENT (0.2506s) ICMP [10.10.14.20 > 10.129.201.248 Echo request (type=8/code=0) id=8338 seq=0] IP [ttl=53 id=5122 iplen=28 ]
SENT (0.2507s) TCP 10.10.14.20:55516 > 10.129.201.248:443 S ttl=42 id=24195 iplen=44  seq=1926233369 win=1024 <mss 1460>
SENT (0.2507s) TCP 10.10.14.20:55516 > 10.129.201.248:80 A ttl=55 id=50395 iplen=40  seq=0 win=1024
SENT (0.2517s) ICMP [10.10.14.20 > 10.129.201.248 Timestamp request (type=13/code=0) id=8247 seq=0 orig=0 recv=0 trans=0] IP [ttl=38 id=62695 iplen=40 ]
RCVD (0.2814s) ICMP [10.129.201.248 > 10.10.14.20 Echo reply (type=0/code=0) id=8338 seq=0] IP [ttl=127 id=38158 iplen=28 ]
SENT (0.3264s) TCP 10.10.14.20:55772 > 10.129.201.248:3389 S ttl=56 id=274 iplen=44  seq=2635590698 win=1024 <mss 1460>
RCVD (0.3565s) TCP 10.129.201.248:3389 > 10.10.14.20:55772 SA ttl=127 id=38162 iplen=44  seq=3526777417 win=64000 <mss 1357>
NSOCK INFO [0.4500s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.4500s] nsock_connect_tcp(): TCP connection requested to 10.129.201.248:3389 (IOD #1) EID 8
NSOCK INFO [0.4820s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 8 [10.129.201.248:3389]
Service scan sending probe NULL to 10.129.201.248:3389 (tcp)
NSOCK INFO [0.4830s] nsock_read(): Read request from IOD #1 [10.129.201.248:3389] (timeout: 6000ms) EID 18
NSOCK INFO [6.4880s] nsock_trace_handler_callback(): Callback: READ TIMEOUT for EID 18 [10.129.201.248:3389]
Service scan sending probe TerminalServerCookie to 10.129.201.248:3389 (tcp)
NSOCK INFO [6.4880s] nsock_write(): Write request for 42 bytes to IOD #1 EID 27 [10.129.201.248:3389]
NSOCK INFO [6.4880s] nsock_read(): Read request from IOD #1 [10.129.201.248:3389] (timeout: 5000ms) EID 34
NSOCK INFO [6.4880s] nsock_trace_handler_callback(): Callback: WRITE SUCCESS for EID 27 [10.129.201.248:3389]
NSOCK INFO [6.5240s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 34 [10.129.201.248:3389] (19 bytes): .........4.........
Service scan match (Probe TerminalServerCookie matched with TerminalServerCookie line 13640): 10.129.201.248:3389 is ms-wbt-server.  Version: |Microsoft Terminal Services|||

...SNIP...

NSOCK INFO [6.5610s] nsock_write(): Write request for 54 bytes to IOD #1 EID 27 [10.129.201.248:3389]
NSE: TCP 10.10.14.20:36630 > 10.129.201.248:3389 | 00000000: 03 00 00 2a 25 e0 00 00 00 00 00 43 6f 6f 6b 69    *%      Cooki
00000010: 65 3a 20 6d 73 74 73 68 61 73 68 3d 6e 6d 61 70 e: mstshash=nmap
00000020: 0d 0a 01 00 08 00 0b 00 00 00  

...SNIP...

NSOCK INFO [6.6820s] nsock_write(): Write request for 57 bytes to IOD #2 EID 67 [10.129.201.248:3389]
NSOCK INFO [6.6820s] nsock_trace_handler_callback(): Callback: WRITE SUCCESS for EID 67 [10.129.201.248:3389]
NSE: TCP 10.10.14.20:36630 > 10.129.201.248:3389 | SEND
NSOCK INFO [6.6820s] nsock_read(): Read request from IOD #2 [10.129.201.248:3389] (timeout: 5000ms) EID 74
NSOCK INFO [6.7180s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 74 [10.129.201.248:3389] (211 bytes)
NSE: TCP 10.10.14.20:36630 < 10.129.201.248:3389 | 
00000000: 30 81 d0 a0 03 02 01 06 a1 81 c8 30 81 c5 30 81 0          0  0
00000010: c2 a0 81 bf 04 81 bc 4e 54 4c 4d 53 53 50 00 02        NTLMSSP
00000020: 00 00 00 14 00 14 00 38 00 00 00 35 82 8a e2 b9        8   5
00000030: 73 b0 b3 91 9f 1b 0d 00 00 00 00 00 00 00 00 70 s              p
00000040: 00 70 00 4c 00 00 00 0a 00 63 45 00 00 00 0f 49  p L     cE    I
00000050: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
00000060: 00 31 00 02 00 14 00 49 00 4c 00 46 00 2d 00 53  1     I L F - S
00000070: 00 51 00 4c 00 2d 00 30 00 31 00 01 00 14 00 49  Q L - 0 1     I
00000080: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
00000090: 00 31 00 04 00 14 00 49 00 4c 00 46 00 2d 00 53  1     I L F - S
000000a0: 00 51 00 4c 00 2d 00 30 00 31 00 03 00 14 00 49  Q L - 0 1     I
000000b0: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
000000c0: 00 31 00 07 00 08 00 1d b3 e8 f2 19 d3 d7 01 00  1
000000d0: 00 00 00

...SNIP...
```

**ข้อควรระวัง:** 
RDP cookies (`mstshash=nmap`) ที่ Nmap ใช้สามารถถูกตรวจจับได้โดย:
- Threat hunters (นักล่าภัยคุกคาม)
- ระบบรักษาความปลอดภัยต่างๆ เช่น EDR (Endpoint Detection and Response)

สิ่งนี้อาจทำให้การเข้าถึงถูกบล็อกได้ในเครือข่ายที่มีความปลอดภัยสูง

## 2. การตรวจสอบความปลอดภัยด้วย rdp-sec-check.pl

### ติดตั้งเครื่องมือ

**ขั้นตอนที่ 1:** ติดตั้ง Perl module ที่จำเป็น
```bash
sudo cpan
cpan[1]> install Encoding::BER
```

**ขั้นตอนที่ 2:** ดาวน์โหลด rdp-sec-check
```bash
git clone https://github.com/CiscoCXSecurity/rdp-sec-check.git && cd rdp-sec-check
```

### การใช้งาน

```bash
Watunyoo@htb[/htb]$ ./rdp-sec-check.pl 10.129.201.248

Starting rdp-sec-check v0.9-beta ( http://labs.portcullis.co.uk/application/rdp-sec-check/ ) at Sun Nov  7 16:50:32 2021

[+] Scanning 1 hosts

Target:    10.129.201.248
IP:        10.129.201.248
Port:      3389

[+] Checking supported protocols

[-] Checking if RDP Security (PROTOCOL_RDP) is supported...Not supported - HYBRID_REQUIRED_BY_SERVER
[-] Checking if TLS Security (PROTOCOL_SSL) is supported...Not supported - HYBRID_REQUIRED_BY_SERVER
[-] Checking if CredSSP Security (PROTOCOL_HYBRID) is supported [uses NLA]...Supported

[+] Checking RDP Security Layer

[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_NONE...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_40BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_128BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_56BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_FIPS...Not supported

[+] Summary of protocol support

[-] 10.129.201.248:3389 supports PROTOCOL_SSL   : FALSE
[-] 10.129.201.248:3389 supports PROTOCOL_HYBRID: TRUE
[-] 10.129.201.248:3389 supports PROTOCOL_RDP   : FALSE

[+] Summary of RDP encryption support

[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_NONE   : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_40BIT  : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_128BIT : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_56BIT  : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_FIPS   : FALSE

[+] Summary of security issues


rdp-sec-check v0.9-beta completed at Sun Nov  7 16:50:33 2021
```

**เครื่องมือนี้ตรวจสอบ:**

**โปรโตคอลที่รองรับ:**
- RDP Security (PROTOCOL_RDP)
- TLS Security (PROTOCOL_SSL)
- CredSSP Security (PROTOCOL_HYBRID) - ใช้ NLA

**ระดับการเข้ารหัส RDP:**
- ENCRYPTION_METHOD_NONE (ไม่เข้ารหัส)
- ENCRYPTION_METHOD_40BIT
- ENCRYPTION_METHOD_128BIT
- ENCRYPTION_METHOD_56BIT
- ENCRYPTION_METHOD_FIPS

**จากตัวอย่าง** เซิร์ฟเวอร์รองรับเฉพาะ PROTOCOL_HYBRID (NLA) และไม่รองรับวิธีการเข้ารหัสอื่นๆ ซึ่งเป็นการตั้งค่าที่ปลอดภัย

## 3. การเชื่อมต่อ RDP

### เครื่องมือที่ใช้บน Linux:
- **xfreerdp** (แนะนำ)
- rdesktop
- Remmina

### ตัวอย่างการเชื่อมต่อด้วย xfreerdp:

```bash
xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248
```

**สิ่งที่เกิดขึ้นขณะเชื่อมต่อ:**

1. **โหลด Channel Plugins**: rdpdr, rdpsnd, cliprdr
2. **ตรวจสอบ Certificate**: จะพบคำเตือน "self-signed certificate" และ "CERTIFICATE NAME MISMATCH"
   - Common Name (CN) อาจไม่ตรงกับ IP address
   - ต้องยืนยันว่าเชื่อถือ certificate (Y/T/N)
3. **ข้อมูล NTLM Version**: แสดงเวอร์ชัน Windows (เช่น 6.1.7601 = Windows 7/Server 2008 R2)
4. **เชื่อมต่อสำเร็จ**: หน้าต่างใหม่จะเปิดขึ้นแสดง desktop ของเซิร์ฟเวอร์

---


# WinRM และ WMI - เครื่องมือจัดการระยะไหลของ Windows

## WinRM (Windows Remote Management)

### ภาพรวม
WinRM เป็นโปรโตคอลการจัดการระยะไหลของ Windows ที่ทำงานผ่าน command line โดยใช้ **SOAP (Simple Object Access Protocol)** ในการสร้างการเชื่อมต่อไปยังโฮสต์ระยะไหลและแอปพลิเคชันต่างๆ

### พอร์ตที่ใช้งาน
- **TCP 5985**: HTTP (ไม่เข้ารหัส)
- **TCP 5986**: HTTPS (เข้ารหัส)

**หมายเหตุ:** ในอดีตใช้พอร์ต 80 และ 443 แต่เนื่องจากพอร์ต 80 ถูกบล็อกด้วยเหตุผลด้านความปลอดภัย จึงเปลี่ยนมาใช้พอร์ต 5985 และ 5986 แทน

### Windows Remote Shell (WinRS)
- เป็นส่วนประกอบที่ทำงานร่วมกับ WinRM
- ให้สามารถรันคำสั่งใดๆ บนระบบระยะไหลได้
- ติดตั้งมาพร้อมกับ Windows 7 โดยค่าเริ่มต้น

### การเปิดใช้งาน
- **Windows Server 2012 ขึ้นไป**: เปิดใช้งานโดยอัตโนมัติ
- **Windows 10 และเวอร์ชันเก่ากว่า**: ต้องเปิดใช้งานและตั้งค่าด้วยตนเอง พร้อมสร้าง firewall exceptions


### บริการที่ต้องใช้ WinRM
- Remote sessions ผ่าน PowerShell
- Event log merging (การรวมบันทึกเหตุการณ์)

---

## การสำรวจ WinRM Service

### 1. สแกนด้วย Nmap

```bash
Watunyoo@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p5985,5986 --disable-arp-ping -n

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 16:31 CET
Nmap scan report for 10.129.201.248
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.34 seconds
```

**ผลลัพธ์ที่ได้:**
- แสดงว่าพอร์ต 5985 (HTTP) เปิดใช้งาน
- บริการ: Microsoft HTTPAPI httpd 2.0
- ระบุข้อมูลระบบปฏิบัติการ Windows

**ข้อสังเกต:** บ่อยครั้งที่จะพบว่ามีเพียง HTTP (TCP 5985) เท่านั้นที่ถูกใช้งาน แทนที่จะเป็น HTTPS (TCP 5986)

### 2. ทดสอบการเชื่อมต่อ

**บน Windows (ใช้ PowerShell):**
```powershell
Test-WsMan <hostname>
```

**บน Linux (ใช้ Evil-WinRM):**
```bash
evil-winrm -i 10.129.201.248 -u Cry0l1t3 -p P455w0rD!
```

Evil-WinRM เป็นเครื่องมือ penetration testing ที่ออกแบบมาเพื่อโต้ตอบกับ WinRM โดยเฉพาะ

**เมื่อเชื่อมต่อสำเร็จ:** จะได้ PowerShell shell ที่สามารถรันคำสั่งบนเซิร์ฟเวอร์ระยะไหลได้

---

## WMI (Windows Management Instrumentation)

### ภาพรวม
WMI เป็นการพัฒนาของ Microsoft ที่ขยายมาจาก **CIM (Common Information Model)** ซึ่งเป็นส่วนหลักของ **WBEM (Web-Based Enterprise Management)** สำหรับแพลตฟอร์ม Windows

### ความสามารถ
- อนุญาตให้อ่านและเขียนได้เกือบทุกการตั้งค่าบนระบบ Windows
- เป็นอินเทอร์เฟซที่สำคัญที่สุดสำหรับการบริหารจัดการและบำรุงรักษาระยะไหลของคอมพิวเตอร์ Windows
- ใช้ได้ทั้ง PC และ Server

### วิธีการเข้าถึง WMI
- **PowerShell**
- **VBScript**
- **WMIC (Windows Management Instrumentation Console)**

### โครงสร้าง
WMI ไม่ใช่โปรแกรมเดียว แต่ประกอบด้วย:
- หลายโปรแกรม
- ฐานข้อมูลต่างๆ (repositories)

---

## การสำรวจ WMI Service

### พอร์ตที่ใช้
- **TCP 135**: สำหรับการเริ่มต้นการสื่อสาร WMI
- **พอร์ตแบบสุ่ม (Random Port)**: หลังจากการเชื่อมต่อสำเร็จ การสื่อสารจะย้ายไปใช้พอร์ตแบบสุ่ม

### การใช้งานด้วย wmiexec.py (Impacket)

```bash
/usr/share/doc/python3-impacket/examples/wmiexec.py Cry0l1t3:"P455w0rD!"@10.129.201.248 "hostname"
```

**ผลลัพธ์:**
- แสดงว่าใช้ SMBv3.0 dialect
- แสดงชื่อโฮสต์ของเครื่องเป้าหมาย (เช่น ILF-SQL-01)

---


## สรุปเปรียบเทียบ

| คุณสมบัติ | WinRM | WMI |
|---------|-------|-----|
| **พอร์ตหลัก** | 5985 (HTTP), 5986 (HTTPS) | 135 แล้วย้ายไปพอร์ตสุ่ม |
| **โปรโตคอล** | SOAP | CIM/WBEM |
| **เครื่องมือ Linux** | evil-winrm | wmiexec.py (Impacket) |
| **การเข้าถึง** | Command line, PowerShell | PowerShell, VBScript, WMIC |
| **ความสามารถ** | Remote command execution | อ่าน/เขียนการตั้งค่าระบบ |