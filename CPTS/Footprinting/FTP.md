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

# rpcclient - Remote Procedure Call Client

## ความหมายและวัตถุประสงค์

### คืออะไร
**rpcclient** เป็นเครื่องมือที่:
- เป็นส่วนหนึ่งของ **Samba suite**
- ใช้สำหรับ execute **MS-RPC (Microsoft Remote Procedure Call)** functions
- ทดสอบและ interact กับ SMB/CIFS services บน Windows และ Samba servers
- ทำงานผ่าน **named pipes** over SMB

### วัตถุประสงค์หลัก
```
rpcclient Use Cases:
├── Enumeration (ค้นหาข้อมูล)
├── Testing SMB services
├── Administrative tasks
└── Security assessment/penetration testing
```

## การติดตั้งและใช้งานพื้นฐาน

### ติดตั้ง
```bash
# Debian/Ubuntu
sudo apt install samba-common-bin

# Red Hat/CentOS
sudo yum install samba-client

# ตรวจสอบการติดตั้ง
rpcclient --version
```

### Syntax พื้นฐาน
```bash
rpcclient -U <username> <target_ip>
rpcclient -U <username>%<password> <target_ip>
rpcclient -U "" -N <target_ip>  # Anonymous/null session
```

## คำสั่งที่สำคัญ

### 1. Server Information
```bash
# ข้อมูลเซิร์ฟเวอร์
srvinfo          # แสดงข้อมูล server
querydispinfo    # แสดงข้อมูล display
netshareenum     # แสดง shares ที่มี
netshareenumall  # แสดง shares ทั้งหมดรวม hidden
```

### 2. User Enumeration
```bash
# ข้อมูลผู้ใช้
enumdomusers     # แสดงรายชื่อ domain users
queryuser <RID>  # ข้อมูลผู้ใช้เฉพาะ
enumdomgroups    # แสดง domain groups
querygroupmem <RID>  # แสดงสมาชิกในกลุ่ม

# ตัวอย่าง
queryuser 0x1f4  # Query Administrator (RID 500)
```

### 3. Password Policy
```bash
# นโยบายรหัสผ่าน
getdompwinfo     # แสดง domain password policy
getusrdompwinfo <RID>  # password info ของ user
```

### 4. Share Information
```bash
# ข้อมูล shares
netshareenum     # แสดง network shares
netsharegetinfo <share>  # รายละเอียดของ share เฉพาะ
```

### 5. Domain Information
```bash
# ข้อมูล domain
lsaquery         # LSA query
lookupsids <SID> # แปลง SID เป็นชื่อ
lookupnames <name>  # แปลงชื่อเป็น SID
enumdomains      # แสดง domains
querydominfo     # ข้อมูล domain
```

### 6. Printer Information
```bash
# ข้อมูล printers
enumprinters     # แสดง printers
enumdrivers      # แสดง printer drivers
```

## ตัวอย่างการใช้งานจริง

### Example 1: Anonymous Enumeration
```bash
# เชื่อมต่อแบบ anonymous
rpcclient -U "" -N 10.10.10.100

rpcclient $> srvinfo
        SMBSERVER      Wk Sv PrQ Unx NT SNT samba.example.com
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03

rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[john] rid:[0x1f6]
user:[mary] rid:[0x1f7]
```

### Example 2: User Information Query
```bash
rpcclient $> queryuser 0x1f6
        User Name   :   john
        Full Name   :   John Doe
        Home Drive  :   \\server\john
        Dir Drive   :   
        Profile Path:   \\server\profiles\john
        Logon Script:   
        Description :   Sales Manager
        Workstations:   
        Comment     :   
        Remote Dial :
        Logon Time               :      Mon, 01 Jan 2024 08:00:00 GMT
        Logoff Time              :      Wed, 31 Dec 2024 23:59:59 GMT
        Kickoff Time             :      Wed, 13 Sep 30828 02:48:05 GMT
        Password last set Time   :      Mon, 15 Jan 2024 14:30:22 GMT
        Password can change Time :      Tue, 16 Jan 2024 14:30:22 GMT
        Password must change Time:      Wed, 13 Sep 30828 02:48:05 GMT
```

### Example 3: Password Policy Check
```bash
rpcclient $> getdompwinfo
min_password_length: 7
password_properties: 0x00000001
        DOMAIN_PASSWORD_COMPLEX
```

### Example 4: Share Enumeration
```bash
rpcclient $> netshareenumall
netname: ADMIN$
        remark: Remote Admin
        path:   C:\Windows
        password:       

netname: C$
        remark: Default share
        path:   C:\
        password:       

netname: IPC$
        remark: Remote IPC
        path:   
        password:       

netname: shared
        remark: Company Files
        path:   C:\shared
        password:
```

## การใช้งานในด้าน Security Testing

### Penetration Testing Workflow
```bash
# 1. ตรวจสอบว่า null session ทำงานได้หรือไม่
rpcclient -U "" -N <target>

# 2. Enumerate users
rpcclient $> enumdomusers

# 3. ดึงข้อมูลแต่ละ user
rpcclient $> queryuser <RID>

# 4. ตรวจสอบ password policy
rpcclient $> getdompwinfo

# 5. ดู shares
rpcclient $> netshareenumall

# 6. Enumerate groups
rpcclient $> enumdomgroups
```

### Common RIDs (Relative Identifiers)
```
Well-known RIDs:
├── 500 = Administrator
├── 501 = Guest
├── 512 = Domain Admins
├── 513 = Domain Users
├── 514 = Domain Guests
├── 515 = Domain Computers
└── 516 = Domain Controllers
```

## คำสั่งที่เป็นประโยชน์เพิ่มเติม

### ตารางคำสั่งสรุป
| คำสั่ง | หน้าที่ | ข้อมูลที่ได้ |
|--------|---------|--------------|
| `srvinfo` | Server info | OS version, platform |
| `enumdomusers` | List users | Username, RID |
| `queryuser <RID>` | User details | Full name, description, login times |
| `enumdomgroups` | List groups | Group names, RIDs |
| `querygroupmem <RID>` | Group members | Members in group |
| `getdompwinfo` | Password policy | Min length, complexity |
| `netshareenum` | List shares | Share names, remarks |
| `lsaquery` | LSA info | Domain SID |
| `lookupsids <SID>` | SID to name | Resolve SID |
| `lookupnames <name>` | Name to SID | Get SID from name |




## สรุป

**rpcclient** เป็นเครื่องมือที่ทรงพลังสำหรับ:
- ✅ **Enumeration**: ค้นหา users, groups, shares
- ✅ **Information Gathering**: รวบรวมข้อมูล domain และ system
- ✅ **Security Testing**: ตรวจสอบช่องโหว่และ misconfigurations
- ✅ **Administration**: จัดการ SMB/CIFS services

