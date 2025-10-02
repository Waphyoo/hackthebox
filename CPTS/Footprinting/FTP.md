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

