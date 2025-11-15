# การล่าข้อมูลรับรอง (Credentials) ในการจราจรเครือข่าย

## ภาพรวม

ในโลกที่ให้ความสำคัญกับความปลอดภัยในปัจจุบัน แอปพลิเคชันส่วนใหญ่ใช้ TLS เพื่อเข้ารหัสข้อมูลสำคัญขณะส่งผ่าน อย่างไรก็ตาม ยังมีสภาพแวดล้อมที่ไม่ได้รับการรักษาความปลอดภัยอย่างเต็มที่ เช่น:

- **ระบบเดิม (Legacy Systems)**
- **บริการที่ตั้งค่าผิดพลาด**
- **แอปพลิเคชันทดสอบที่ไม่ได้ใช้ HTTPS**

ช่องโหว่เหล่านี้สร้างโอกาสให้ผู้โจมตีสามารถล่าข้อมูลรับรองในรูปแบบ cleartext จากการจราจรเครือข่าย

## โปรโตคอลที่เสี่ยงต่อการดักจับข้อมูล

### ตารางเปรียบเทียบโปรโตคอล

| โปรโตคอลไม่เข้ารหัส | โปรโตคอลที่เข้ารหัส | คำอธิบาย |
|---|---|---|
| **HTTP** | HTTPS | ใช้สำหรับส่งผ่านเว็บเพจและทรัพยากรบนอินเทอร์เน็ต |
| **FTP** | FTPS/SFTP | ใช้สำหรับถ่ายโอนไฟล์ระหว่าง Client กับ Server |
| **SNMP** | SNMPv3 (with encryption) | ใช้สำหรับตรวจสอบและจัดการอุปกรณ์เครือข่าย เช่น Router และ Switch |
| **POP3** | POP3S | ดึงอีเมลจาก Mail Server มายัง Local Client |
| **IMAP** | IMAPS | เข้าถึงและจัดการข้อความอีเมลบน Mail Server โดยตรง |
| **SMTP** | SMTPS | ส่งอีเมลจาก Client ไป Server หรือระหว่าง Mail Server |
| **LDAP** | LDAPS | สืบค้นและแก้ไข Directory Services เช่น ข้อมูลรับรองและบทบาทผู้ใช้ |
| **RDP** | RDP (with TLS) | ให้การเข้าถึง Remote Desktop บนระบบ Windows |
| **DNS (Traditional)** | DNS over HTTPS (DoH) | แปลงชื่อโดเมนเป็น IP Address |
| **SMB** | SMB over TLS (SMB 3.0) | แชร์ไฟล์ เครื่องพิมพ์ และทรัพยากรอื่นๆ ผ่านเครือข่าย |
| **VNC** | VNC with TLS/SSL | อนุญาตให้ควบคุมคอมพิวเตอร์อื่นแบบกราฟิกระยะไกล |

## เครื่องมือสำหรับล่าข้อมูลรับรอง

### 1. Wireshark

Wireshark เป็น Packet Analyzer ที่มีชื่อเสียงและติดตั้งมาพร้อมกับ Linux Distribution สำหรับ Penetration Testing เกือบทั้งหมด มี Filter Engine ที่ทรงพลังสำหรับค้นหาข้อมูลในการจราจรเครือข่ายแบบ Live หรือที่บันทึกไว้

#### Wireshark Filters พื้นฐานที่มีประโยชน์

| Filter | คำอธิบาย |
|---|---|
| `ip.addr == 56.48.210.13` | กรอง Packet ที่มี IP Address ที่ระบุ |
| `tcp.port == 80` | กรอง Packet ตาม Port (HTTP ในกรณีนี้) |
| `http` | กรองเฉพาะ HTTP Traffic |
| `dns` | กรอง DNS Traffic เพื่อตรวจสอบการแปลงชื่อโดเมน |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | กรอง SYN Packets (ใช้ใน TCP Handshake) เหมาะสำหรับตรวจจับการ Scan |
| `icmp` | กรอง ICMP Packets (ใช้สำหรับ Ping) |
| `http.request.method == "POST"` | กรองเฉพาะ HTTP POST Requests ซึ่งอาจมีรหัสผ่านหรือข้อมูลสำคัญ |
| `tcp.stream eq 53` | กรอง TCP Stream ที่ระบุ ช่วยติดตามการสื่อสารระหว่างสอง Host |
| `eth.addr == 00:11:22:33:44:55` | กรอง Packet จาก/ไป MAC Address ที่ระบุ |
| `ip.src == 192.168.24.3 && ip.dst == 56.48.210.3` | กรองการจราจรระหว่างสอง IP Address ที่ระบุ |

#### การค้นหาข้อมูลรับรองใน Wireshark

**วิธีที่ 1: ใช้ Display Filter**
```
http contains "passw"
```

**วิธีที่ 2: ใช้เมนู Find Packet**
- ไปที่ `Edit > Find Packet`
- ป้อนคำค้นหาที่ต้องการ เช่น "passw"

**ตัวอย่างการใช้งาน:**
- ค้นหา POST Request ที่มีข้อมูลฟอร์ม HTML ที่ประกอบด้วย Username และ Password
- ตรวจสอบ HTTP Traffic ที่ไม่ได้เข้ารหัส

#### ข้อแนะนำ
ควรทำความคุ้นเคยกับไวยากรณ์ของ Wireshark Filtering Engine โดยเฉพาะอย่างยิ่งหากต้องทำการวิเคราะห์การจราจรเครือข่าย

---

### 2. Pcredz

Pcredz เป็นเครื่องมือที่ใช้สำหรับแยกข้อมูลรับรองจาก Live Traffic หรือไฟล์ Packet Capture

#### ข้อมูลที่ Pcredz สามารถแยกได้

✅ **ข้อมูลทางการเงิน:**
- เลขบัตรเครดิต

✅ **ข้อมูลรับรองอีเมล:**
- POP credentials
- SMTP credentials
- IMAP credentials

✅ **ข้อมูลรับรองเครือข่าย:**
- SNMP community strings
- FTP credentials
- HTTP NTLM/Basic authentication headers
- HTTP Form credentials

✅ **Hash และข้อมูลขั้นสูง:**
- NTLMv1/v2 hashes จาก DCE-RPC, SMBv1/2, LDAP, MSSQL, HTTP
- Kerberos (AS-REQ Pre-Auth etype 23) hashes

#### การติดตั้ง Pcredz

**ตัวเลือก 1:** Clone Repository และติดตั้ง Dependencies

**ตัวเลือก 2:** ใช้ Docker Container (ดูรายละเอียดใน README)

#### การใช้งาน Pcredz

**คำสั่งพื้นฐาน:**
```bash
./Pcredz -f demo.pcapng -t -v
```

**ตัวอย่างผลลัพธ์:**
```
Pcredz 2.0.2
Author: Laurent Gaffie
Please send bugs/comments/pcaps to: laurent.gaffie@gmail.com
This script will extract NTLM (HTTP,LDAP,SMB,MSSQL,RPC, etc), Kerberos,
FTP, HTTP Basic and credit card data from a given pcap file or from a live interface.

CC number scanning activated

Unknown format, trying TCPDump format

[1746131482.601354] protocol: udp 192.168.31.211:59022 > 192.168.31.238:161
Found SNMPv2 Community string: s3cr...SNIP...

[1746131482.601640] protocol: udp 192.168.31.211:59022 > 192.168.31.238:161
Found SNMPv2 Community string: s3cr...SNIP...

<SNIP>

[1746131482.658938] protocol: tcp 192.168.31.243:55707 > 192.168.31.211:21
FTP User: le...SNIP...
FTP Pass: qw...SNIP...

demo.pcapng parsed in: 1.82 seconds (File size 15.5 Mo).
```

#### คำอธิบายผลลัพธ์

- **SNMP Community String:** พบข้อมูลรับรองจากโปรโตคอล SNMP
- **FTP Credentials:** พบ Username และ Password จากการเชื่อมต่อ FTP
- **เวลาประมวลผล:** วิเคราะห์ไฟล์ขนาด 15.5 MB ใน 1.82 วินาที

---

https://github.com/lgandx/PCredz?tab=readme-ov-file#install