


![alt text](image.png)




## Infrastructure Based Enumeration

### Domain Information 
-  SSL certificate --> https://crt.sh/
- shodan
- dig --> txt record

```
ใช้หา subdomain ได้แบบ public

curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u
```

### Cloud Resources
- S3 buckets (AWS), blobs (Azure), cloud storage (GCP) Object ที่เก็บข้อมูลและเข้าถึงผ่าน URL
- https://domain.glass/    
- https://buckets.grayhatwarfare.com/

**ตัวอย่าง URL:**
```
AWS S3: https://bucket-name.s3.amazonaws.com/file.pdf
Azure: https://account.blob.core.windows.net/container/file.pdf  
GCP: https://storage.googleapis.com/bucket-name/file.pdf
```

**หลักการ:**
- แต่ละไฟล์ = 1 Object
- แต่ละ Object มี URL เฉพาะตัว
- เข้าถึงผ่าน HTTP/HTTPS

**ในมุมมอง Pentester:**
- URL เดาได้ → เข้าถึงไฟล์ได้
- Misconfiguration → Public access
- Directory listing → เห็นไฟล์ทั้งหมด

**สรุป:** Object storage = ไฟล์ + URL = เป้าหมายสำคัญใน OSINT/Recon!

# Host Based Enumeration

## File Transfer Protocol (FTP)
- application layer of the TCP/IP protocol stack
- เป็น clear-text protocol สามารถ sniff ได้
- ต้องการ credentials แต่อาจมี anonymous access

#### FTP Active Mode

1. **Client เริ่มต้นการเชื่อมต่อ**
   - Client เชื่อมต่อไปยัง Server ผ่าน port 21 (Control Channel)
   - Client ส่งคำสั่ง PORT พร้อมบอก IP และ port ของตัวเอง

2. **Server เริ่ม Data Connection**
   - Server เชื่อมต่อกลับไปยัง Client จาก port 20
   - Server เป็นฝ่ายเริ่ม data connection

```
Client (1234) -----> Server (21)  [Control Connection]
Client (5678) <----- Server (20)  [Data Connection - Server เริ่ม]
```

#### ปัญหาที่พบ
- **Firewall/NAT Issues**: Server ไม่สามารถเชื่อมต่อกลับมายัง Client ได้
- Client ที่อยู่หลัง firewall จะบล็อกการเชื่อมต่อจากภายนอก
- ไม่เหมาะสำหรับ Client ที่อยู่หลัง NAT

#### FTP Passive Mode (PASV)


1. **Client เริ่มต้นการเชื่อมต่อ**
   - Client เชื่อมต่อไปยัง Server ผ่าน port 21
   - Client ส่งคำสั่ง PASV

2. **Server แจ้ง Port**
   - Server ตอบกลับด้วย IP และ port ที่เปิดรอ
   - Client เชื่อมต่อไปยัง port ที่ Server กำหนด

```
Client (1234) -----> Server (21)    [Control Connection]
Client (5678) -----> Server (2000)  [Data Connection - Client เริ่ม]
```

#### ข้อดี
- แก้ปัญหา firewall ฝั่ง Client
- Client เป็นฝ่ายเริ่มการเชื่อมต่อทั้งหมด
- ทำงานได้ดีกับ NAT

## TFTP (Trivial File Transfer Protocol)

- **ความเรียบง่าย**: TFTP ง่ายกว่า FTP มาก
- **ไม่มี Authentication**: ไม่ต้องการ username/password
- **ใช้ UDP**: แทนที่จะใช้ TCP เหมือน FTP
- **ไม่น่าเชื่อถือ**: เนื่องจากใช้ UDP ที่ไม่รับประกันการส่งข้อมูล
#### การควบคุมการเข้าถึง
- **ไม่มี Password Protection**: ไม่สามารถตั้งรหัสผ่านได้
- **พึ่งพา File Permissions**: ใช้สิทธิ์ไฟล์ของ OS เป็นหลัก
- **Public Access Only**: ทำงานได้เฉพาะกับไฟล์ที่เปิดให้ทุกคนเข้าถึง
- **Local Network Only**: ใช้ได้เฉพาะในเครือข่ายท้องถิ่นที่ปลอดภัย

Download All Available Files
```
wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136
```

```
http://vsftpd.beasts.org/vsftpd_conf.html
```

### การเชื่อมต่อ FTP ผ่าน TLS/SSL

เมื่อ FTP server ใช้การเข้ารหัส TLS/SSL (เรียกว่า FTPS) จำเป็นต้องใช้ client ที่รองรับการเข้ารหัส โดย `openssl` เป็นเครื่องมือที่มีประโยชน์ในการทดสอบและดูข้อมูล SSL certificate

#### การใช้ OpenSSL กับ FTPS


```bash
openssl s_client -connect IP:21 -starttls ftp
```

จากตัวอย่างในโจทย์:
```
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
```

#### การแปลความหมาย Certificate Fields

| Field | ความหมาย | ตัวอย่าง |
|-------|----------|----------|
| **C** | Country | US |
| **ST** | State/Province | California |
| **L** | Locality/City | Sacramento |
| **O** | Organization | Inlanefreight |
| **OU** | Organizational Unit | Dev |
| **CN** | Common Name | master.inlanefreight.htb |
| **emailAddress** | Email Contact | admin@inlanefreight.htb |




## Server Message Block (SMB) 


# สรุป Server Message Block (SMB)

## ความเป็นมาและพื้นฐาน

### นิยาม
**SMB (Server Message Block)** เป็น client-server protocol ที่ควบคุมการเข้าถึง:
- ไฟล์และไดเรกทอรี
- ทรัพยากรเครือข่ายอื่นๆ เช่น เครื่องพิมพ์, เราเตอร์, interfaces
- การแลกเปลี่ยนข้อมูลระหว่างระบบต่างๆ

### ประวัติและการพัฒนา
- เริ่มต้นจาก OS/2 network operating system (LAN Manager และ LAN Server)
- ใช้หลักใน Windows operating system series
- รองรับ **downward-compatible** - อุปกรณ์ใหม่สื่อสารกับ Windows รุ่นเก่าได้
- **Samba project** ทำให้ Linux/Unix ใช้ SMB ได้ (cross-platform communication)

## การทำงานของ SMB Protocol

### กลไกการสื่อสาร
1. **การเชื่อมต่อ**: Client สื่อสารกับ participants อื่นในเครือข่ายเดียวกัน
2. **ข้อกำหนด**: ระบบปลายทางต้องมี SMB server application
3. **การจับมือ**: ต้องแลกเปลี่ยน messages เพื่อสร้างการเชื่อมต่อ

### การใช้ TCP ใน IP Networks
```
SMB ใช้ TCP protocol
├── Three-way handshake ระหว่าง client และ server
├── การขนส่งข้อมูลตาม TCP specifications
└── ความน่าเชื่อถือในการส่งข้อมูล
```

## SMB Shares และ File System

### การทำงานของ Shares
- **SMB server** สามารถแบ่งปันส่วนใดส่วนหนึ่งของ local file system เป็น **shares**
- **Hierarchy** ที่ client เห็นอาจไม่เหมือนกับโครงสร้างจริงบน server

### Scenario 1: SMB อนุญาต แต่ Local ปฏิเสธ
```bash
# SMB Share ACL: john = Full Control
# Local File: owner=root, permissions=700
# ผลลัพธ์: john เข้าถึงไม่ได้ (Local ปฏิเสธ)
```

### Scenario 2: SMB ปฏิเสธ แต่ Local อนุญาต
```bash  
# SMB Share ACL: mary = No Access
# Local File: owner=mary, permissions=755
# ผลลัพธ์: mary เข้าถึงไม่ได้ (SMB ปฏิเสธ)
```

### Scenario 3: ทั้งคู่อนุญาต
```bash
# SMB Share ACL: alice = Read/Write  
# Local File: group=staff, alice ∈ staff, permissions=770
# ผลลัพธ์: alice เข้าถึงได้ (ทั้งคู่อนุญาต)
```


## Samba คืออะไร

### นิยามและจุดประสงค์
**Samba** เป็น alternative implementation ของ SMB server ที่:
- พัฒนาสำหรับ Unix-based operating systems
- ใช้ Common Internet File System (CIFS) network protocol
- ทำให้ Unix/Linux สามารถสื่อสารกับ Windows systems ได้

### ความสัมพันธ์ระหว่าง SMB, CIFS, และ Samba
```
SMB Protocol (Microsoft)
├── CIFS = SMB dialect (specific implementation)
│   └── Primary: SMB version 1
└── Samba = Open source implementation
    └── ใช้ CIFS เพื่อสื่อสารกับ Windows
```

## CIFS (Common Internet File System)

### คุณลักษณะ
- **CIFS เป็น dialect ของ SMB** = การใช้งาน SMB protocol แบบเฉพาะ
- สร้างโดย Microsoft เดิม
- ทำให้ Samba สื่อสารกับ Windows systems ได้อย่างมีประสิทธิภาพ
- มักเรียกรวมกันว่า **SMB/CIFS**

### ข้อจำกัด
- CIFS ถือเป็น **SMB version 1** เป็นหลัก
- เป็นเวอร์ชันเก่าที่ยังใช้ในสภาพแวดล้อมเฉพาะ

## Ports และการเชื่อมต่อ

### Traditional SMB/NetBIOS (SMB 1)
**TCP Ports 137, 138, 139** เมื่อ:
- ส่ง SMB commands ผ่าน Samba
- เชื่อมต่อกับ older NetBIOS service
- ใช้ legacy infrastructure

### Modern CIFS/SMB
**TCP Port 445** สำหรับ:
- CIFS operates exclusively
- Direct SMB over TCP/IP
- ไม่ต้องผ่าน NetBIOS layer

### ตารางเปรียบเทียบ Ports
| Protocol | Ports | ใช้สำหรับ |
|----------|-------|-----------|
| **NetBIOS over TCP** | 137, 138, 139 | Legacy SMB, older systems |
| **SMB/CIFS Direct** | 445 | Modern implementations |

## SMB Versions Evolution

### SMB Version Timeline
```
SMB 1 (CIFS)
├── เวอร์ชันเก่า (outdated)
├── ยังใช้ในสภาพแวดล้อมเฉพาะ
└── มีช่องโหว่ด้านความปลอดภัย

SMB 2
├── ปรับปรุงประสิทธิภาพ
├── ความปลอดภัยดีขึ้น
└── รองรับ features ใหม่

SMB 3
├── เป็นที่นิยมใน modern infrastructure
├── การเข้ารหัสที่แข็งแกร่ง
└── ประสิทธิภาพสูงสุด
```

