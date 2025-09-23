## Timeout ใน Port Scanning

**ปัญหา:**
- เครื่องมือสแกนรอ response จาก service 
- ถ้า timeout → มาร์คเป็น closed/filtered/unknown
- **อันตราย**: ถ้ามาร์คเป็น "closed" → Nmap ไม่แสดงให้เห็น
```
Port เปิดอยู่ → Timeout → มาร์ค "closed" → เราพลาดไป!
```

## TCP-SYN scan (-sS)

จะส่งแพ็กเก็ตที่มีแฟล็ก SYN หนึ่งแพ็กเก็ต ไม่สามารถทำ three-way handshake ได้สำเร็จ
- Nmap ได้ SYN-ACK = port open
- Nmap ได้ RST = close
- Nmap ไม่ได้ อาจจะโดน firewall = filtered

TCP-SYN scan (-sS) เป็นค่าเริ่มต้นในฐานะ root. Nmap จะสแกนพอร์ต TCP 1,000 พอร์ตแรกด้วย
(-sS) ใช้ raw socket 
## Nmap Ping Scan Behavior

**เมื่อปิด Port Scan (`-sn`):**
- Nmap ใช้ ping scan แทน
- **Default**: ส่ง `ICMP Echo Request` (`-PE`)
- **คาดหวัง**: ได้ `ICMP Reply` กลับมา = host มีชีวิต

**ความจริงที่น่าสนใจ:**
```
การสแกนปกติ → ไม่ส่ง ICMP Echo Request
เพราะ → ส่ง ARP ping ก่อน → ได้ ARP reply → จบ
```

**ลำดับการทำงาน:**
1. **ARP ping** → **ARP reply** ✅ (จบเลย)
2. ~~ICMP Echo Request~~ (ไม่ต้องส่ง)

**การตรวจสอบ:**
- ใช้ `--packet-trace` เพื่อดู packet ที่ส่ง
- ใช้ `-PE` เพื่อบังคับส่ง ICMP Echo Request

```
Windows TTL มักใช้ค่า 128 ส่วน Linux อาจใช้ค่า 64 
```

![alt text](image.png)


## ทำไมต้อง Disable ICMP Echo (`-Pn`)

**เหตุผลหลัก:**

### 1. **Host Discovery ปกติ**
```
Nmap → ส่ง ICMP Echo Request → รอ ICMP Reply
ถ้าไม่ได้ Reply → คิดว่า host ตาย → หยุดสแกน!
```

### 2. **ปัญหาที่เกิดขึ้น:**
- **Firewall block ICMP** → ไม่ได้ Reply
- **Host มีชีวิต** แต่ Nmap คิดว่าตาย
- **ไม่สแกน port** เลย!

### 3. **การใช้ `-Pn`:**
```
-Pn = "ถือว่าทุก host มีชีวิต"
→ ข้าม ping test
→ สแกน port ตรงๆ เลย
```



## การสแกน UDP Ports

**TCP vs UDP:**
```
TCP: มี 3-way handshake → ได้ ACK → รวดเร็ว
UDP: ไม่มี handshake → ไม่มี ACK → timeout นาน
```

**ปัญหาใหญ่ของ UDP Scan:**

1. **Nmap ส่ง empty datagrams**
2. **ไม่ได้ response กลับมา**
3. **ไม่รู้ว่า packet ถึงหรือเปล่า**
4.  เมื่อไหร่ได้ response: UDP port เปิด **และ** application ตั้งค่าให้ตอบกลับ

If we get an ICMP response with error code 3 (port unreachable), we know that the port is indeed closed.

For all other ICMP responses, the scanned ports are marked as (open|filtered).



![alt text](image-1.png)


![alt text](image-2.png)


## Bypass Security Measures
Decoys


## Hard Lab

--source-port 53 ทะลุ firewall ได้

```
┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/…/Desktop/hackthebox/CPTS/Nmap]
└─$ ncat --source-port 53 10.129.227.208 50000
220 HTB{kjnsdf2n982n1827eh76238s98di1w6}
```