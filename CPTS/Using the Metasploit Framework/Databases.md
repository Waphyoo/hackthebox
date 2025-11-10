# Databases ใน Metasploit

## ทำไมต้องใช้ Database?

ในการประเมินความปลอดภัย โดยเฉพาะกับเครือข่ายขนาดใหญ่ เราจะพบข้อมูลมากมาย เช่น:
- ผลการสแกน
- จุดเข้าระบบ (Entry Points)
- ช่องโหว่ที่พบ
- ข้อมูล Credentials ที่ค้นพบ

**Database ช่วยให้เราจัดการข้อมูลเหล่านี้ได้อย่างเป็นระบบ**

### ความสามารถของ Database ใน msfconsole:

✅ เข้าถึงผลการสแกนได้รวดเร็ว  
✅ Import/Export ข้อมูลร่วมกับเครื่องมืออื่นได้  
✅ ใช้ข้อมูลที่มีอยู่ตั้งค่า Parameter ของ Exploit Module ได้โดยตรง  
✅ รองรับ **PostgreSQL** database system

---

## การตั้งค่า Database

### 1. ตรวจสอบสถานะ PostgreSQL

```bash
sudo service postgresql status
```

**ผลลัพธ์ที่ควรได้:**
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; disabled; vendor preset: disabled)
     Active: active (exited) since Fri 2022-05-06 14:51:30 BST; 3min 51s ago
```

### 2. เริ่มต้น PostgreSQL

```bash
sudo systemctl start postgresql
```

### 3. สร้างและ Initialize MSF Database

```bash
sudo msfdb init
```

**ผลลัพธ์ที่ควรได้ (การติดตั้งใหม่):**
```
[+] Starting database
[+] Creating database user 'msf'
[+] Creating databases 'msf'
[+] Creating databases 'msf_test'
[+] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[+] Creating initial database schema
```

### 4. แก้ไขปัญหาที่อาจเจอ

#### กรณีเจอ Error หรือ Database ถูกตั้งค่าไปแล้ว:

**อัพเดท Metasploit:**
```bash
apt update
```

**ตรวจสอบสถานะ:**
```bash
sudo msfdb status
```

**Reinitialize Database (ถ้าจำเป็น):**
```bash
msfdb reinit
cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
sudo service postgresql restart
msfconsole -q
```

### 5. เชื่อมต่อกับ Database

```bash
sudo msfdb run
```

**ตรวจสอบการเชื่อมต่อ:**
```
msf6 > db_status
[*] Connected to msf. Connection type: PostgreSQL.
```

---

## คำสั่งพื้นฐานสำหรับ Database

### คำสั่งหลักทั้งหมด:

```
msf6 > help database
```

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `db_connect` | เชื่อมต่อกับ database ที่มีอยู่ |
| `db_disconnect` | ตัดการเชื่อมต่อจาก database |
| `db_export` | Export ไฟล์ที่มีเนื้อหาของ database |
| `db_import` | Import ผลการสแกน (ตรวจจับ filetype อัตโนมัติ) |
| `db_nmap` | รัน Nmap และบันทึกผลลัพธ์อัตโนมัติ |
| `db_rebuild_cache` | สร้าง module cache ใหม่ |
| `db_status` | แสดงสถานะ database ปัจจุบัน |
| `hosts` | แสดงรายการ hosts ทั้งหมด |
| `loot` | แสดงรายการ loot ทั้งหมด |
| `notes` | แสดงรายการ notes ทั้งหมด |
| `services` | แสดงรายการ services ทั้งหมด |
| `vulns` | แสดงรายการช่องโหว่ทั้งหมด |
| `workspace` | สลับระหว่าง workspaces |

---

## Workspaces

**Workspace เปรียบเสมือนโฟลเดอร์ในโปรเจค** - ใช้แยกข้อมูลตาม IP, Subnet, Network หรือ Domain

### คำสั่งพื้นฐาน:

**ดู Workspace ทั้งหมด:**
```
msf6 > workspace
* default
```
(*สัญลักษณ์ * = กำลังใช้งานอยู่*)

**สร้าง Workspace ใหม่:**
```
msf6 > workspace -a Target_1
[*] Added workspace: Target_1
```

**สลับ Workspace:**
```
msf6 > workspace Target_1
[*] Workspace: Target_1
```

**ลบ Workspace:**
```
msf6 > workspace -d Target_1
```

### คำสั่ง Workspace ทั้งหมด:

```
msf6 > workspace -h

Usage:
    workspace                    List workspaces
    workspace -v                 List workspaces verbosely
    workspace [name]             Switch workspace
    workspace -a [name] ...      Add workspace(s)
    workspace -d [name] ...      Delete workspace(s)
    workspace -D                 Delete all workspaces
    workspace -r <old> <new>     Rename workspace
    workspace -h                 Show this help information
```

---

## Import ผลการสแกน

### 1. Import ไฟล์ Nmap XML

**ไฟล์ Nmap ตัวอย่าง (Target.nmap):**
```
Starting Nmap 7.80
Nmap scan report for 10.10.10.40
Host is up (0.017s latency)
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows 7 - 10
```

**Import เข้า Database:**
```
msf6 > db_import Target.xml
[*] Importing 'Nmap XML' data
[*] Import: Parsing with 'Nokogiri v1.10.9'
[*] Importing host 10.10.10.40
[*] Successfully imported ~/Target.xml
```

**ตรวจสอบข้อมูลที่ Import:**
```
msf6 > hosts

Hosts
=====
address      mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.40             Unknown                    device
```

```
msf6 > services

Services
========
host         port   proto  name          state  info
----         ----   -----  ----          -----  ----
10.10.10.40  135    tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  139    tcp    netbios-ssn   open   Microsoft Windows netbios-ssn
10.10.10.40  445    tcp    microsoft-ds  open   Microsoft Windows 7 - 10
```

**⚠️ หมายเหตุ:** ควรใช้ไฟล์ **.xml** สำหรับ `db_import`

---

## ใช้ Nmap ภายใน MSFconsole

**ไม่ต้อง Exit หรือ Background Console!**

```
msf6 > db_nmap -sV -sS 10.10.10.8

[*] Nmap: Starting Nmap 7.80
[*] Nmap: Nmap scan report for 10.10.10.8
[*] Nmap: Host is up (0.016s latency)
[*] Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 80/tcp open  http    HttpFileServer httpd 2.3
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 11.12 seconds
```

**ข้อมูลจะถูกบันทึกใน Database อัตโนมัติ!**

```
msf6 > hosts

Hosts
=====
address      mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.8              Unknown                    device
10.10.10.40             Unknown                    device
```

---

## Backup ข้อมูล

### Export Database

```
msf6 > db_export -f xml backup.xml

[*] Starting export of workspace default to backup.xml [ xml ]...
[*] Finished export of workspace default to backup.xml [ xml ]...
```

**รูปแบบที่รองรับ:**
- `xml` - รูปแบบ XML
- `pwdump` - รูปแบบ password dump

---

## คำสั่งจัดการข้อมูลขั้นสูง

### 1. **Hosts Command**

แสดงและจัดการข้อมูล hosts ใน database

```
msf6 > hosts -h

OPTIONS:
  -a,--add          Add the hosts instead of searching
  -d,--delete       Delete the hosts instead of searching
  -c <col1,col2>    Only show the given columns
  -h,--help         Show this help information
  -u,--up           Only show hosts which are up
  -o <file>         Send output to a file in CSV format
  -R,--rhosts       Set RHOSTS from the results of the search
  -S,--search       Search string to filter by
```

**คอลัมน์ที่มี:** address, arch, os_name, os_flavor, info, mac, name, comments, created_at, updated_at, service_count, vuln_count, tags, และอื่นๆ

### 2. **Services Command**

แสดงและจัดการข้อมูล services

```
msf6 > services -h

OPTIONS:
  -a,--add          Add the services instead of searching
  -d,--delete       Delete the services instead of searching
  -p <port>         Search for a list of ports
  -s <name>         Name of the service to add
  -u,--up           Only show services which are up
  -R,--rhosts       Set RHOSTS from the results of the search
```

### 3. **Credentials Command**

แสดงและจัดการข้อมูล credentials ที่รวบรวมได้

```
msf6 > creds -h

Usage - Adding credentials:
  creds add user:admin password:notpassword realm:workgroup
  creds add user:admin ntlm:E2FC15074BF7751DD408E6B105741864
  creds add user:sshadmin ssh-key:/path/to/id_rsa
```

**ตัวอย่างการใช้งาน:**
```bash
# เพิ่ม username และ password
creds add user:admin password:notpassword realm:workgroup

# เพิ่ม NTLM Hash
creds add user:admin ntlm:E2FC15074BF7751DD408E6B105741864

# เพิ่ม SSH Key
creds add user:sshadmin ssh-key:/path/to/id_rsa

# กรองตาม port
creds -p 22-25,445

# กรองตาม service
creds -s ssh,smb

# กรองตาม type
creds -t NTLM
```

**Hash types ที่รองรับ:**
- Blowfish ($2a$) : bf
- MD5 ($1$) : md5
- SHA256 ($5$) : sha256
- SHA512 ($6$) : sha512
- MSSQL, MySQL, Oracle, Postgres

### 4. **Loot Command**

แสดงรายการข้อมูลสำคัญที่ได้จากการโจมตี เช่น:
- Hash dumps
- Password files
- Shadow files

```
msf6 > loot -h

Usage: loot [options]
  Add: loot -f [fname] -i [info] -a [addr1 addr2 ...] -t [type]
  Del: loot -d [addr1 addr2 ...]

OPTIONS:
  -a,--add          Add loot to the list of addresses
  -d,--delete       Delete loot matching host and type
  -f,--file         File with contents of the loot to add
  -t <type>         Search for a list of types
```

---

