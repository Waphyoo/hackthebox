# Dynamic Port Forwarding ด้วย SSH และ SOCKS Tunneling (ฉบับสมบูรณ์)

## สถานการณ์ (Scenario)

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  ATTACKER       │         │    DMZ          │         │   INTERNAL      │
│  MACHINE        │────────>│  (Pivot Host)   │────────>│   NETWORK       │
│                 │         │                 │         │                 │
│  10.10.15.x     │         │  10.129.202.64  │         │  172.16.5.0/23  │
│                 │         │  172.16.5.129   │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
     (เรา)              (Ubuntu ที่เรายึดได้แล้ว)         (เป้าหมายจริง)
```

---

## Port Forwarding คืออะไร?

Port Forwarding เป็นเทคนิคที่ช่วยให้เราสามารถ redirect การสื่อสารจาก port หนึ่งไปยังอีก port หนึ่งได้

**คุณสมบัติหลัก:**
- ใช้ TCP เป็น primary communication layer สำหรับ interactive communication
- สามารถใช้ application layer protocols อื่นๆ เช่น SSH ในการ encapsulate traffic
- สามารถใช้ non-application layer protocols เช่น SOCKS ในการ encapsulate traffic
- ช่วยข้ามผ่าน firewalls ได้อย่างมีประสิทธิภาพ
- ใช้ existing services บน compromised host เพื่อ pivot ไปยัง networks อื่นๆ

---

## SSH Local Port Forwarding (เทคนิคแรก)

### สถานการณ์เริ่มต้น

**เครื่องที่เกี่ยวข้อง:**
- ATTACKER MACHINE: `10.10.15.x`
- DMZ Ubuntu Server: `10.129.202.64` (compromised แล้ว)

### ขั้นตอนที่ 1: Scan DMZ เพื่อดู Services

```bash
# ที่ ATTACKER MACHINE
nmap -sT -p22,3306 10.129.202.64
```

**ผลลัพธ์:**
```
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:12 EST
Nmap scan report for 10.129.202.64
Host is up (0.12s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
3306/tcp closed mysql

Nmap done: 1 IP address (1 host up) scanned in 0.68 seconds
```

**การวิเคราะห์:**
- SSH port (22) เปิดอยู่ → สามารถ SSH เข้าไปได้
- MySQL port (3306) ปิดอยู่ → แต่จริงๆ MySQL รันอยู่ภายในเครื่อง (localhost only)
- MySQL bind อยู่ที่ `localhost:3306` ของ DMZ เท่านั้น (ไม่ listen จากภายนอก)

### ขั้นตอนที่ 2: ทำ Local Port Forward

```bash
# ที่ ATTACKER MACHINE
ssh -L 1234:localhost:3306 ubuntu@10.129.202.64
```

**Output เมื่อเชื่อมต่อสำเร็จ:**
```
ubuntu@10.129.202.64's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu 24 Feb 2022 05:23:20 PM UTC

  System load:             0.0
  Usage of /:              28.4% of 13.72GB
  Memory usage:            34%
  Swap usage:              0%
  Processes:               175
  Users logged in:         1
  IPv4 address for ens192: 10.129.202.64
  IPv6 address for ens192: dead:beef::250:56ff:feb9:52eb
  IPv4 address for ens224: 172.16.5.129

66 updates can be applied immediately.
45 of these updates are standard security updates.
```

**คำอธิบาย parameter `-L`:**
- `-L 1234:localhost:3306` หมายความว่า:
  - `1234` = port ที่จะเปิดบน ATTACKER MACHINE
  - `localhost` = ชี้ไปที่ localhost ของ DMZ (ไม่ใช่ ATTACKER MACHINE)
  - `3306` = port ปลายทางบน DMZ ที่ต้องการ forward ไป

**การทำงานของ SSH Client:**
- SSH client บอก SSH server (ที่ DMZ) ให้ forward traffic ทั้งหมด
- Traffic ที่ ATTACKER MACHINE ส่งมาที่ port 1234
- จะถูก forward ไปที่ `localhost:3306` บน DMZ

**Diagram การทำงาน:**
```
ATTACKER MACHINE (10.10.15.x)
    │
    │ [1] เชื่อมต่อ SSH ไป DMZ
    │
    ↓
Port 1234 (SSH Client เปิด listen)
    │
    │ [2] เมื่อมี traffic มาที่ port 1234
    │
    ↓
SSH Tunnel (Encrypted)
    │
    │ [3] ส่งผ่าน SSH tunnel
    │
    ↓
DMZ (10.129.202.64)
    │
    │ [4] SSH Server รับ traffic
    │
    ↓
localhost:3306 ที่ DMZ (MySQL Service)
```

### ขั้นตอนที่ 3: ยืนยันว่า Port Forward ทำงาน

**วิธีที่ 1: ใช้ Netstat**

```bash
# ที่ ATTACKER MACHINE
netstat -antp | grep 1234
```

**ผลลัพธ์:**
```
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:1234          0.0.0.0:*               LISTEN      4034/ssh            
tcp6       0      0 ::1:1234                :::*                    LISTEN      4034/ssh
```

**การวิเคราะห์:**
- มี process ssh (PID 4034) กำลัง listen ที่ port 1234
- Listen ทั้ง IPv4 (127.0.0.1) และ IPv6 (::1)
- State เป็น LISTEN = พร้อมรับ connection

**วิธีที่ 2: ใช้ Nmap Scan ตัวเอง**

```bash
# ที่ ATTACKER MACHINE
nmap -v -sV -p1234 localhost
```

**ผลลัพธ์:**
```
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:18 EST
NSE: Loaded 45 scripts for scanning.
Initiating Ping Scan at 12:18
Scanning localhost (127.0.0.1) [2 ports]
Completed Ping Scan at 12:18, 0.01s elapsed (1 total hosts)
Initiating Connect Scan at 12:18
Scanning localhost (127.0.0.1) [1 port]
Discovered open port 1234/tcp on 127.0.0.1
Completed Connect Scan at 12:18, 0.01s elapsed (1 total ports)
Initiating Service scan at 12:18
Scanning 1 service on localhost (127.0.0.1)
Completed Service scan at 12:18, 0.12s elapsed (1 service on 1 host)

PORT     STATE SERVICE VERSION
1234/tcp open  mysql   MySQL 8.0.28-0ubuntu0.20.04.3

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.18 seconds
```

**การวิเคราะห์:**
- Nmap สามารถตรวจจับว่า port 1234 เปิดอยู่
- Service detection แสดงว่าเป็น MySQL version 8.0.28
- นี่หมายความว่า forward สำเร็จ - เราสามารถเข้าถึง MySQL ที่ DMZ ผ่าน localhost:1234 ได้

### การ Forward หลาย Ports พร้อมกัน

```bash
# ที่ ATTACKER MACHINE
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64
```

**คำอธิบาย:**
- `-L 1234:localhost:3306` = Forward MySQL (port 3306) มาที่ port 1234
- `-L 8080:localhost:80` = Forward Apache Web Server (port 80) มาที่ port 8080
- สามารถใช้หลาย `-L` เท่าที่ต้องการ

**ผลลัพธ์:**
- ที่ ATTACKER MACHINE สามารถใช้:
  - `localhost:1234` → เชื่อมต่อ MySQL ที่ DMZ
  - `localhost:8080` → เปิด website ที่ DMZ

---

## การเตรียมพร้อมสำหรับ Pivoting

### ตรวจสอบ Network Interfaces ของ DMZ

```bash
# ที่ DMZ (SSH เข้าไปแล้ว)
ifconfig
```

**ผลลัพธ์:**
```
ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.202.64  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:52:eb  txqueuelen 1000  (Ethernet)
        RX packets 35571  bytes 177919049 (177.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10452  bytes 1474767 (1.4 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:feb9:a9aa  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a9:aa  txqueuelen 1000  (Ethernet)
        RX packets 8251  bytes 1125190 (1.1 MB)
        RX errors 0  dropped 40  overruns 0  frame 0
        TX packets 1538  bytes 123584 (123.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 270  bytes 22432 (22.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 270  bytes 22432 (22.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

**การวิเคราะห์ Network Interfaces:**

1. **ens192 (NIC แรก):**
   - IP: `10.129.202.64`
   - Netmask: `255.255.0.0` (CIDR /16)
   - Network: `10.129.0.0/16`
   - เชื่อมต่อกับ ATTACKER MACHINE
   - MAC: `00:50:56:b9:52:eb`
   - RX: 177.9 MB (รับข้อมูล)
   - TX: 1.4 MB (ส่งข้อมูล)

2. **ens224 (NIC ที่สอง - สำคัญมาก!):**
   - IP: `172.16.5.129`
   - Netmask: `255.255.254.0` (CIDR /23)
   - Network: `172.16.5.0/23` (รองรับ 172.16.5.0 - 172.16.5.255)
   - เชื่อมต่อกับ INTERNAL NETWORK
   - MAC: `00:50:56:b9:a9:aa`
   - มี dropped packets 40 packets (อาจมี network congestion เล็กน้อย)

3. **lo (Loopback):**
   - IP: `127.0.0.1`
   - ใช้สำหรับ internal communication

**ข้อสรุปสำคัญ:**
- DMZ เป็น **dual-homed host** (มี 2 NICs เชื่อมต่อ 2 networks แยกกัน)
- สามารถใช้เป็น pivot point ได้
- มี access ไปยัง INTERNAL NETWORK (172.16.5.0/23) ที่ ATTACKER MACHINE เข้าไม่ถึงโดยตรง

### ปัญหาที่พบ

**สถานการณ์ปัจจุบัน:**
- ATTACKER MACHINE อยู่ใน network `10.10.15.0/24`
- INTERNAL NETWORK อยู่ใน network `172.16.5.0/23`
- **ไม่มี routing path โดยตรงระหว่าง 2 networks นี้**

**สิ่งที่เราต้องการ:**
- Scan INTERNAL NETWORK เพื่อหา hosts และ services
- ต้องการ scan range: `172.16.5.1-200` หรือ entire subnet `172.16.5.0/23`

**ปัญหา:**
- ไม่สามารถ scan โดยตรงจาก ATTACKER MACHINE ได้
- เพราะ ATTACKER MACHINE ไม่มี routes ไปยัง `172.16.5.0/23`
- Local Port Forward ไม่เหมาะ เพราะ:
  - ต้องรู้ target IP และ port ล่วงหน้า
  - ต้อง forward ทีละ port
  - ไม่เหมาะกับการ scan หลาย hosts/ports

**โซลูชัน:**
- ใช้ **Dynamic Port Forwarding** กับ **SOCKS Proxy**
- สามารถส่ง traffic ไปยังหลาย destinations พร้อมกัน
- ไม่ต้องระบุ target ล่วงหน้า

---

## Dynamic Port Forwarding กับ SOCKS Tunneling

### SOCKS Protocol คืออะไร?

**SOCKS (Socket Secure):**
- เป็น protocol ที่ช่วยสื่อสารกับ servers เมื่อมี firewall restrictions
- ออกแบบมาเพื่อ proxy network connections

**ความแตกต่างจากการเชื่อมต่อปกติ:**

**การเชื่อมต่อปกติ:**
```
Client → โดยตรง → Server (Service)
```

**การเชื่อมต่อผ่าน SOCKS:**
```
SOCKS Client → SOCKS Server (ที่เราควบคุม) → Target Server
```

**ขั้นตอนการทำงาน:**
1. SOCKS client สร้าง initial traffic
2. เชื่อมต่อไปยัง SOCKS server (ที่ user ควบคุม)
3. SOCKS server รับ connection request
4. SOCKS server สร้าง connection ไปยัง target service ในนาม client
5. เมื่อเชื่อมต่อสำเร็จ → route network traffic ผ่าน SOCKS server แทน client

**ตัวอย่างการอุปมา:**
- คุณอยากส่งของให้เพื่อน แต่ห้ามส่งโดยตรง
- คุณส่งของให้คนกลาง (SOCKS server)
- คนกลางส่งต่อให้เพื่อนแทนคุณ
- เพื่อนเห็นว่าได้ของจากคนกลาง ไม่ใช่จากคุณโดยตรง

**ประเภทของ SOCKS:**

| Feature | SOCKS4 | SOCKS5 |
|---------|---------|---------|
| **Authentication** | ❌ ไม่รองรับ | ✅ รองรับ (Username/Password) |
| **UDP Support** | ❌ TCP เท่านั้น | ✅ รองรับทั้ง TCP และ UDP |
| **IPv6 Support** | ❌ IPv4 เท่านั้น | ✅ รองรับ IPv6 |
| **DNS Resolution** | Client-side | ✅ Server-side (ปลอดภัยกว่า) |
| **Use Cases** | Basic proxying | Advanced proxying, VPN-like |

**ประโยชน์ของ SOCKS Proxy:**

1. **Circumvent Firewall Restrictions:**
   - ข้ามผ่าน firewall rules ที่บล็อก direct connections
   - ใช้ allowed ports (เช่น SSH port 22) ในการ tunnel

2. **Access Services Behind Firewall:**
   - External entity สามารถ bypass firewall
   - เข้าถึง services ใน firewalled environment

3. **Pivot from NAT Networks:**
   - สามารถสร้าง route จาก NAT networks ไปยัง external servers
   - NAT traversal โดยไม่ต้อง port forwarding

4. **Hide Source IP:**
   - Target เห็นแต่ IP ของ SOCKS server
   - ไม่เห็น IP จริงของ client

---

## การตั้งค่า SSH Dynamic Port Forwarding

### Diagram สถานการณ์

```
┌──────────────────────────────────────────────────────────────┐
│                    ATTACKER MACHINE                          │
│                     (10.10.15.x)                            │
│                                                              │
│  ┌──────────┐         ┌─────────────┐      ┌─────────────┐ │
│  │  Nmap    │────────>│ Proxychains │─────>│ SOCKS Proxy │ │
│  │Metasploit│         │             │      │  Port 9050  │ │
│  │ xfreerdp │         │             │      │             │ │
│  └──────────┘         └─────────────┘      └──────┬──────┘ │
│                                                     │        │
│                                              ┌──────▼──────┐ │
│                                              │ SSH Client  │ │
│                                              └──────┬──────┘ │
└─────────────────────────────────────────────────────┼────────┘
                                                      │
                                    SSH Tunnel (Encrypted)
                                         Port 22
                                                      │
┌─────────────────────────────────────────────────────▼────────┐
│                      DMZ / PIVOT HOST                        │
│                   (10.129.202.64)                           │
│                                                              │
│  ┌─────────────┐                                            │
│  │ SSH Server  │ Port 22                                    │
│  │             │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│         │ Forward packets                                   │
│         │                                                    │
│  ┌──────▼──────────────┐                                    │
│  │  ens224 Interface   │                                    │
│  │   172.16.5.129      │                                    │
│  └──────┬──────────────┘                                    │
└─────────┼─────────────────────────────────────────────────────┘
          │
          │ Route to Internal Network
          │
┌─────────▼─────────────────────────────────────────────────────┐
│                    INTERNAL NETWORK                           │
│                     (172.16.5.0/23)                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Windows DC   │  │ Windows      │  │ Linux        │     │
│  │ 172.16.5.19  │  │ File Server  │  │ Web Server   │     │
│  │              │  │ 172.16.5.20  │  │ 172.16.5.25  │     │
│  │ Ports:       │  │              │  │              │     │
│  │ - 135 (RPC)  │  │ Ports:       │  │ Ports:       │     │
│  │ - 139 (NetB) │  │ - 445 (SMB)  │  │ - 80 (HTTP)  │     │
│  │ - 445 (SMB)  │  │ - 3389 (RDP) │  │ - 443 (HTTPS)│     │
│  │ - 3389 (RDP) │  │              │  │ - 22 (SSH)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────────────────────────────────────────┘
```

### ขั้นตอนที่ 1: Enable Dynamic Port Forwarding

```bash
# ที่ ATTACKER MACHINE
ssh -D 9050 ubuntu@10.129.202.64
```

**คำอธิบาย parameter `-D`:**
- `-D 9050` = เปิด Dynamic Port Forwarding mode
- `9050` = port number ที่จะเปิด SOCKS proxy listener บน ATTACKER MACHINE
- SSH client จะ listen ที่ `localhost:9050`

**การทำงานเบื้องหลัง:**

1. **SSH Client Request:**
```
ATTACKER MACHINE → DMZ
"ขอเปิด Dynamic Port Forwarding นะ ฉันจะส่ง TCP data ผ่าน SSH socket"
```

2. **SSH Server Response:**
```
DMZ → ATTACKER MACHINE
"OK, รับทราบ พร้อมรับ data แล้ว"
```

3. **SOCKS Listener Setup:**
```
SSH Client เปิด listen ที่ localhost:9050 (ATTACKER MACHINE)
พร้อมรับ traffic จาก applications
```

4. **Traffic Broadcasting:**
```
Traffic ที่ส่งมาที่ port 9050 → จะถูก broadcast ไปทั่ว network 172.16.5.0/23
ผ่าน SSH tunnel ไปยัง DMZ
DMZ forward ต่อไปยัง INTERNAL NETWORK
```

**ผลลัพธ์:**
- SSH connection ยังคงเปิดอยู่ (ต้องไม่ปิด terminal นี้)
- SOCKS proxy ทำงานใน background
- พร้อมรับ traffic จาก tools อื่นๆ

### ขั้นตอนที่ 2: ติดตั้งและ Config Proxychains

**Proxychains คืออะไร:**

Proxychains เป็นเครื่องมือที่:
- **Redirect TCP connections** ผ่าน proxy servers
- รองรับ proxy types: TOR, SOCKS4, SOCKS5, HTTP/HTTPS
- สามารถ **chain multiple proxies** เข้าด้วยกัน (proxy ต่อ proxy)
- **Force applications** ให้ส่ง traffic ผ่าน proxy (แม้ app ไม่รองรับ proxy)

**การทำงานของ Proxychains:**
```
Application (เช่น Nmap)
    │
    │ [1] พยายามสร้าง TCP connection
    │
    ↓
Proxychains (Intercept)
    │
    │ [2] ดัก connection request
    │ [3] เปลี่ยนเป็น SOCKS request
    │
    ↓
SOCKS Proxy (localhost:9050)
    │
    │ [4] Forward ผ่าน SSH tunnel
    │
    ↓
Target Host (172.16.5.x)
```

**ประโยชน์:**
- **Hide IP Address:** Target เห็นแต่ IP ของ pivot host
- **Bypass Restrictions:** Applications ที่ไม่รองรับ proxy ก็ใช้ได้
- **Chain Proxies:** สามารถใช้หลาย proxies ต่อกัน

**แก้ไข Config File:**

```bash
# ที่ ATTACKER MACHINE
nano /etc/proxychains.conf
```

**ดู config ปัจจุบัน:**
```bash
tail -4 /etc/proxychains.conf
```

**ผลลัพธ์:**
```
# meanwile
# defaults set to "tor"
socks4 	127.0.0.1 9050
```

**คำอธิบาย config:**
- `socks4` = ใช้ SOCKS4 protocol
- `127.0.0.1` = SOCKS server อยู่ที่ localhost (ATTACKER MACHINE)
- `9050` = port ที่ SOCKS proxy listen อยู่

**หาก config ไม่มี:**
```bash
# เพิ่มบรรทัดนี้ที่ท้ายไฟล์
echo "socks4 127.0.0.1 9050" >> /etc/proxychains.conf
```

**Options อื่นๆ ใน config (ถ้าต้องการปรับแต่ง):**

```ini
# Proxychains Configuration File

# Dynamic Chain
# - แต่ละ proxy ในลิสต์จะถูกใช้ตามลำดับ
# - ถ้า proxy ตัวใดตัวหนึ่ง dead จะข้ามไป
dynamic_chain

# หรือ Strict Chain
# - ต้องใช้ทุก proxy ในลิสต์
# - ถ้า proxy ตัวใดตัวหนึ่ง dead จะเกิด error
#strict_chain

# Proxy DNS requests
proxy_dns

# Timeout in seconds
tcp_read_time_out 15000
tcp_connect_time_out 8000

# [ProxyList]
socks4 127.0.0.1 9050
```

---

## การใช้ Nmap ผ่าน Proxychains

### การ Scan Ping Sweep

```bash
# ที่ ATTACKER MACHINE
proxychains nmap -v -sn 172.16.5.1-200
```

**คำอธิบาย parameters:**
- `proxychains` = รัน nmap ผ่าน proxychains
- `-v` = verbose mode (แสดงรายละเอียด)
- `-sn` = Ping scan (host discovery only, ไม่ scan ports)
- `172.16.5.1-200` = scan IP range 172.16.5.1 ถึง 172.16.5.200

**ผลลัพธ์ตัวอย่าง:**
```
ProxyChains-3.1 (http://proxychains.sf.net)

Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:30 EST
Initiating Ping Scan at 12:30
Scanning 10 hosts [2 ports/host]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.2:80-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.5:80-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.6:80-<--timeout
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0

<SNIP>
```

**การอ่านผลลัพธ์:**
- `|S-chain|` = แสดง SOCKS chain (การ route ผ่าน proxy)
- `127.0.0.1:9050` = SOCKS proxy ที่ ATTACKER MACHINE
- `172.16.5.x:80` = target IP:port
- `<><>-OK` = connection สำเร็จ (host alive)
- `<--timeout` = connection timeout (host อาจจะไม่ alive หรือ firewall block)

**ข้อจำกัดสำคัญของ Proxychains:**

1. **ต้องใช้ Full TCP Connect Scan เท่านั้น:**
```bash
# ✅ ถูกต้อง - Full TCP Connect
proxychains nmap -sT 172.16.5.19

# ❌ ผิด - SYN Scan จะได้ผลลัพธ์ผิด
proxychains nmap -sS 172.16.5.19
```

**เหตุผล:**
- Proxychains ไม่เข้าใจ partial packets (incomplete TCP handshake)
- Half-open scans เช่น SYN scan ส่ง SYN packet เดียว ไม่ complete handshake
- Proxychains ต้องการ full TCP connection (SYN → SYN-ACK → ACK)

2. **Host-Alive Checks อาจไม่ทำงานกับ Windows:**
```bash
# Windows Defender Firewall block ICMP โดย default
# ต้องใช้ -Pn (skip ping) เสมอ
proxychains nmap -Pn -sT 172.16.5.19
```

3. **Scan ช้ากว่าปกติ:**
- เพราะต้องผ่าน: Proxychains → SOCKS → SSH tunnel → DMZ → Target
- Full TCP connect ช้ากว่า SYN scan
- แต่ละ connection ต้อง complete 3-way handshake

**คำแนะนำ:**
- **อย่า** scan entire subnet ด้วย full TCP connect
- Scan เฉพาะ hosts ที่รู้ว่า alive
- หรือ scan small ranges (เช่น 172.16.5.1-50)

### การ Scan Port บน Host เฉพาะ

```bash
# ที่ ATTACKER MACHINE
proxychains nmap -v -Pn -sT 172.16.5.19
```

**ผลลัพธ์:**
```
ProxyChains-3.1 (http://proxychains.sf.net)
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-24 12:33 EST
Initiating Parallel DNS resolution of 1 host. at 12:33
Completed Parallel DNS resolution of 1 host. at 12:33, 0.15s elapsed
Initiating Connect Scan at 12:33
Scanning 172.16.5.19 [1000 ports]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:1720-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:587-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:445-<><>-OK
Discovered open port 445/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:8080-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:23-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:135-<><>-OK
Discovered open port 135/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:110-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:21-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:554-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:25-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:5900-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:1025-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:143-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:199-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:993-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:995-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
Discovered open port 3389/tcp on 172.16.5.19
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:443-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:80-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:113-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:8888-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:139-<><>-OK
Discovered open port 139/tcp on 172.16.5.19
```

**การวิเคราะห์ Ports ที่พบ:**

| Port | Service | Description | Significance |
|------|---------|-------------|--------------|
| **135/tcp** | RPC (Remote Procedure Call) | Windows RPC Endpoint Mapper | เป็น port สำหรับ Windows RPC services, มักเปิดบน Windows servers |
| **139/tcp** | NetBIOS Session Service | NetBIOS over TCP | ใช้สำหรับ file/printer sharing ใน legacy Windows |
| **445/tcp** | SMB (Server Message Block) | Windows File Sharing | เป็น modern file sharing protocol, ใช้เข้าถึง shares, สามารถใช้สำหรับ lateral movement |
| **3389/tcp** | RDP (Remote Desktop Protocol) | Windows Remote Desktop | สามารถ remote control Windows GUI ได้, เป็น target หลักสำหรับ pivoting |

**สิ่งที่น่าสนใจ:**
- เป็น **Windows Server** แน่นอน (จาก ports 135, 139, 445, 3389)
- Port 3389 (RDP) **เปิดอยู่** → สามารถ remote desktop ได้
- Port 445 (SMB) **เปิดอยู่** → อาจมี shared folders
- Port 135 (RPC) **เปิดอยู่** → อาจมี RPC services ที่ exploit ได้

---

## การใช้ Metasploit ผ่าน Proxychains

### เปิด Metasploit Framework

```bash
# ที่ ATTACKER MACHINE
proxychains msfconsole
```

**Output:**
```
ProxyChains-3.1 (http://proxychains.sf.net)
                                                  
     .~+P``````-o+:.                                      -o+:.
.+oooyysyyssyyssyddh++os-`````                        ```````````````          `
+++++++++++++++++++++++sydhyoyso/:.````...`...-///::+ohhyosyyosyy/+om++:ooo///o
++++///////~~~~///////++++++++++++++++ooyysoyysosso+++++++++++++++++++///oossosy
--.`                 .-.-...-////+++++++++++++++////////~~//////++++++++++++///
                                `...............`              `...-/////...`

[... ASCII art ...]

       =[ metasploit v6.1.27-dev                          ]
+ -- --=[ 2196 exploits - 1162 auxiliary - 400 post       ]
+ -- --=[ 596 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 9 evasion                                       ]

Metasploit tip: Adapter names can be used for IP params 
set LHOST eth0

msf6 >
```

**สิ่งที่เกิดขึ้น:**
- Metasploit เริ่มทำงานผ่าน proxychains
- **ทุก module** ที่รันจะส่ง traffic ผ่าน SOCKS proxy โดยอัตโนมัติ
- ไม่ต้อง config เพิ่มเติมใน Metasploit

### ใช้ RDP Scanner Module

```bash
msf6 > search rdp_scanner
```

**ผลลัพธ์:**
```
Matching Modules
================

   #  Name                               Disclosure Date  Rank    Check  Description
   -  ----                               ---------------  ----    -----  -----------
   0  auxiliary/scanner/rdp/rdp_scanner                   normal  No     Identify endpoints speaking the Remote Desktop Protocol (RDP)

Interact with a module by name or index. For example info 0, use 0 or use auxiliary/scanner/rdp/rdp_scanner
```

**Load Module:**
```bash
msf6 > use 0
# หรือ
msf6 > use auxiliary/scanner/rdp/rdp_scanner
```

**Configure Module:**
```bash
msf6 auxiliary(scanner/rdp/rdp_scanner) > set rhosts 172.16.5.19
rhosts => 172.16.5.19

msf6 auxiliary(scanner/rdp/rdp_scanner) > show options

Module options (auxiliary/scanner/rdp/rdp_scanner):

   Name             Current Setting  Required  Description
   ----             ---------------  --------  -----------
   DETECT_NLA       true             yes       Detect Network Level Authentication (NLA)
   RDP_CLIENT_IP    192.168.0.100    yes       The client IPv4 address to report during connect
   RDP_CLIENT_NAME  rdesktop         no        The client computer name to report during connect
   RDP_DOMAIN                        no        The client domain name to report during connect
   RDP_USER                          no        The username to report during connect, or blank for random
   RHOSTS           172.16.5.19      yes       The target host(s)
   RPORT            3389             yes       The target port (TCP)
   THREADS          1                yes       The number of concurrent threads (max one per host)
```

**Run Module:**
```bash
msf6 auxiliary(scanner/rdp/rdp_scanner) > run
```

**ผลลัพธ์:**
```
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK

[*] 172.16.5.19:3389      - Detected RDP on 172.16.5.19:3389      
    (name:DC01) 
    (domain:DC01) 
    (domain_fqdn:DC01) 
    (server_fqdn:DC01) 
    (os_version:10.0.17763) 
    (Requires NLA: No)
[*] 172.16.5.19:3389      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

**การวิเคราะห์ผลลัพธ์:**

| Field | Value | Description |
|-------|-------|-------------|
| **name** | DC01 | Computer name = DC01 (likely Domain Controller) |
| **domain** | DC01 | Domain name |
| **os_version** | 10.0.17763 | Windows Server 2019 (Build 17763) |
| **Requires NLA** | No | ไม่ต้องมี Network Level Authentication = ง่ายต่อการโจมตี |

**ความสำคัญ:**
- **Requires NLA: No** = ไม่ต้อง authenticate ก่อน establish RDP connection
- สามารถใช้ RDP exploits ได้ง่ายขึ้น
- สามารถ brute force RDP ได้โดยตรง

---

## การเชื่อมต่อ RDP ผ่าน SOCKS Tunnel

### ใช้ xfreerdp

```bash
# ที่ ATTACKER MACHINE
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```

**คำอธิบาย parameters:**
- `proxychains` = รัน xfreerdp ผ่าน SOCKS proxy
- `xfreerdp` = FreeRDP client (open-source RDP client)
- `/v:172.16.5.19` = target IP address ใน INTERNAL NETWORK
- `/u:victor` = username
- `/p:pass@123` = password

**Output:**
```
ProxyChains-3.1 (http://proxychains.sf.net)
[13:02:42:481] [4829:4830] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[13:02:42:482] [4829:4830] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
```

**ขั้นตอนการเชื่อมต่อ:**

1. **Certificate Verification:**
```
┌──────────────────────────────────────────────────────────┐
│ Certificate Details                                      │
├──────────────────────────────────────────────────────────┤
│ Subject: CN=DC01                                         │
│ Issuer: CN=DC01                                          │
│ Thumbprint: XX:XX:XX:XX:XX:XX:XX:XX...                  │
│                                                          │
│ Do you trust this certificate? (Y/N)                    │
└──────────────────────────────────────────────────────────┘
```
- กด `Y` เพื่อ accept certificate

2. **Authentication:**
```
Authenticating as user: victor
Domain: DC01
```

3. **RDP Session Established:**
```
┌──────────────────────────────────────────────────────────┐
│ Connected to: DC01 (172.16.5.19)                        │
│ User: DC01\victor                                        │
│ Session: Console                                         │
└──────────────────────────────────────────────────────────┘
```

**สิ่งที่เกิดขึ้นเบื้องหลัง:**

```
ATTACKER MACHINE (10.10.15.x)
    │
    │ [1] xfreerdp สร้าง RDP connection request
    │
    ↓
Proxychains (Intercept)
    │
    │ [2] ดัก RDP traffic
    │ [3] ส่งไปที่ SOCKS proxy
    │
    ↓
SOCKS Proxy (Port 9050)
    │
    │ [4] รับ RDP packets
    │ [5] ห่อหุ้มด้วย SSH protocol
    │
    ↓
SSH Client (Port 22)
    │
    │ [6] ส่งผ่าน SSH tunnel (encrypted)
    │
    ↓
DMZ (10.129.202.64)
    │
    │ [7] SSH Server รับ encrypted packets
    │ [8] Decrypt SSH layer
    │ [9] แกะ RDP packets ออกมา
    │
    ↓
DMZ Network Interface (ens224: 172.16.5.129)
    │
    │ [10] Forward RDP packets ไปยัง INTERNAL NETWORK
    │
    ↓
Windows Server (172.16.5.19:3389)
    │
    │ [11] RDP Server รับ connection
    │ [12] Authenticate user: victor
    │ [13] สร้าง RDP session
    │
    ↓
[✅ RDP Session Active]
```
---

## สรุปเทคนิคทั้งหมด

### SSH Local Port Forward vs Dynamic Port Forward

| Aspect | Local Port Forward | Dynamic Port Forward |
|--------|-------------------|---------------------|
| **คำสั่ง** | `ssh -L [port]:[host]:[port] [user]@[pivot]` | `ssh -D [port] [user]@[pivot]` |
| **Use Case** | รู้ target และ port ล่วงหน้า | ไม่รู้ targets, ต้องการ scan |
| **Flexibility** | ต้องระบุ target/port ตายตัว | ส่ง traffic ไปได้ทุก destination |
| **Setup** | ง่าย, ไม่ต้อง config proxychains | ต้อง setup proxychains |
| **Performance** | เร็วกว่า (direct forward) | ช้ากว่า (ผ่าน proxy layer) |
| **Tools** | ใช้ได้โดยตรง | ต้องรันผ่าน proxychains |

### Traffic Flow Summary

**Local Port Forward:**
```
Application → localhost:[port] → SSH Client → SSH Tunnel → 
DMZ → Forward → Specific Service
```

**Dynamic Port Forward:**
```
Application → Proxychains → SOCKS:[port] → SSH Client → 
SSH Tunnel → DMZ → Forward → Any Destination
```
