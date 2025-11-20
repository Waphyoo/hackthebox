# การทำความเข้าใจ Pivoting, Tunneling และ Port Forwarding

## สถานการณ์ที่ใช้เทคนิคเหล่านี้

ในการทำ Red Team Engagement, Penetration Testing หรือการประเมิน Active Directory เรามักจะพบสถานการณ์ที่เราได้ credentials, SSH keys, hashes หรือ access tokens มาแล้ว แต่ไม่สามารถเข้าถึงเครื่องเป้าหมายถัดไปได้โดยตรงจาก attack host ของเรา ในกรณีนี้เราต้องใช้ pivot host (เครื่องที่เราควบคุมได้แล้ว) เป็นตัวกลางในการเข้าถึงเป้าหมายถัดไป

**สิ่งสำคัญที่ต้องตรวจสอบเมื่อเข้าถึงเครื่องใหม่:**
- ระดับสิทธิ์ของเรา (privilege level)
- การเชื่อมต่อเครือข่าย (network connections)
- ซอฟต์แวร์ VPN หรือ remote access อื่นๆ
- จำนวน network adapter (ถ้ามีมากกว่า 1 ตัว = โอกาสในการ pivot)

## คำศัพท์ที่ใช้เรียก Pivot Host

เครื่องที่เราใช้เป็นตัวกลางในการ pivot มีหลายชื่อเรียก:
- **Pivot Host**
- **Proxy**
- **Foothold**
- **Beach Head System**
- **Jump Host**

## Pivoting คืออะไร?

Pivoting คือการเคลื่อนย้ายไปยังเครือข่ายอื่นๆ ผ่านเครื่องที่เราควบคุมได้แล้ว เพื่อค้นหาเป้าหมายใน network segment ที่แตกต่างกัน

**จุดประสงค์หลัก:** ทำลายการแบ่งแยกเครือข่าย (network segmentation) ทั้งแบบ physical และ virtual เพื่อเข้าถึง isolated network

## Tunneling คืออะไร?

Tunneling เป็น subset ของ pivoting โดยทำหน้าที่ห่อหุ้ม (encapsulate) network traffic ให้อยู่ในรูปแบบของ protocol อื่น

**ตัวอย่างการอุปมา:**
- สมมติเราต้องส่งกุญแจให้หุ้นส่วน แต่ไม่อยากให้คนอื่นรู้ว่าเป็นกุญแจ
- เราซ่อนกุญแจไว้ในตุ๊กตา พร้อมคำแนะนำการใช้งาน
- บรรจุตุ๊กตาลงกล่องและส่งไป
- คนที่เห็นจะคิดว่าเป็นแค่ตุ๊กตาธรรมดา ไม่รู้ว่ามีอะไรซ่อนอยู่
- เฉพาะหุ้นส่วนเท่านั้นที่รู้ว่ากุญแจซ่อนอยู่ข้างในและจะใช้งานได้

**ตัวอย่างแอปพลิเคชัน:** VPN หรือ specialized browsers ก็เป็นรูปแบบหนึ่งของ tunneling

## Lateral Movement vs Pivoting vs Tunneling

### Lateral Movement (การเคลื่อนที่แนวนอน)

**คำจำกัดความ:** เทคนิคที่ใช้เพื่อขยายการเข้าถึงไปยัง hosts, applications และ services เพิ่มเติมภายในเครือข่าย

**จุดประสงค์:**
- เข้าถึง domain resources เพื่อยกระดับสิทธิ์
- ทำ privilege escalation ข้ามหลายๆ hosts
- แพร่กระจายการควบคุมในแนวกว้าง

**ตัวอย่างการใช้งาน:**
```
1. เราได้ initial access และควบคุม local administrator account
2. ทำ network scan เจอ Windows hosts อีก 3 เครื่อง
3. ลอง credentials เดิม พบว่า 1 เครื่องใช้ admin account เดียวกัน
4. ใช้ credentials เข้าควบคุมเครื่องนั้น → สามารถ compromise domain ต่อไปได้
```

**อ้างอิง:**
- [Palo Alto Network's Explanation](https://www.paloaltonetworks.com)
- [MITRE's Explanation](https://attack.mitre.org)

### Pivoting (การหมุนเวียน)

**คำจำกัดความ:** การใช้หลายๆ hosts เพื่อข้ามขอบเขตเครือข่ายที่ปกติเราเข้าไม่ถึง

**จุดประสงค์:**
- เป็นเป้าหมายเฉพาะเจาะจง (targeted objective)
- เจาะลึกเข้าไปในเครือข่ายโดยการ compromise hosts หรือ infrastructure ที่เป็นเป้าหมาย

**ตัวอย่างการใช้งาน:**
```
สถานการณ์: เครือข่ายเป้าหมายถูกแบ่งแยกทั้ง physical และ logical

1. เราค้นหาและ compromise engineering workstation
2. เครื่องนี้ใช้ดูแลอุปกรณ์ใน operational environment
3. พบว่าเป็น dual-homed host (มี NIC เชื่อมต่อหลาย networks)
   - มีการเชื่อมต่อทั้ง enterprise network และ operational network
4. ใช้เครื่องนี้เป็น pivot เพื่อเข้าถึงทั้งสอง network
5. หากไม่มีเครื่องนี้ เราจะไม่สามารถทำ assessment ได้สำเร็จ
```

### Tunneling (การสร้างอุโมงค์)

**คำจำกัดความ:** การใช้ protocols ต่างๆ เพื่อส่ง traffic เข้า/ออกเครือข่าย โดยพยายามหลีกเลี่ยงการตรวจจับ

**จุดประสงค์:**
- ซ่อนเร้น (obfuscation) การกระทำของเราเพื่อหลีกเลี่ยงการตรวจจับ
- ใช้ protocols ที่มีการเข้ารหัส เช่น HTTPS over TLS หรือ SSH
- ช่วยใน exfiltration ข้อมูล หรือส่ง payloads/instructions เข้าเครือข่าย

**ตัวอย่างการใช้งาน:**
```
การใช้ Tunneling เพื่อ Command and Control (C2):

1. ปลอมแปลง traffic ให้ซ่อนอยู่ใน HTTP/HTTPS
2. ซ่อนคำสั่งใน GET และ POST requests
3. ทำให้ดูเหมือน web traffic ธรรมดา
4. ถ้า packet ถูกต้อง → forward ไป C2 server
5. ถ้าไม่ถูกต้อง → redirect ไป website อื่น (หลอก defender)
6. ผู้ตรวจสอบที่ไม่มีประสบการณ์จะคิดว่าเป็น web request ปกติ
```

## สรุปความแตกต่าง

| เทคนิค | จุดประสงค์ | ลักษณะการใช้งาน |
|--------|-----------|----------------|
| **Lateral Movement** | แพร่กระจายในแนวกว้าง | ขยายการควบคุม, ยกระดับสิทธิ์ข้าม hosts |
| **Pivoting** | เจาะลึกเข้าไปในเครือข่าย | ข้ามขอบเขต network, เข้าถึง isolated environments |
| **Tunneling** | ซ่อนเร้นและหลบหลีกการตรวจจับ | ปกปิด traffic, exfiltrate data, maintain C2 |



# แนวคิดพื้นฐานเรื่อง Networking สำหรับ Pivoting

## IP Addressing & NICs (Network Interface Controllers)

### หลักการพื้นฐาน

**ทุกคอมพิวเตอร์ที่สื่อสารในเครือข่ายต้องมี IP address** - ถ้าไม่มี แสดงว่าไม่ได้อยู่ในเครือข่าย

### การกำหนด IP Address

IP address สามารถกำหนดได้ 2 แบบ:

1. **Dynamic Assignment (DHCP)**
   - ได้รับ IP อัตโนมัติจาก DHCP server
   - ใช้กับอุปกรณ์ทั่วไป

2. **Static Assignment (กำหนดคงที่)**
   - ใช้กับอุปกรณ์สำคัญ เช่น:
     - Servers
     - Routers
     - Switch virtual interfaces
     - Printers
     - อุปกรณ์ที่ให้บริการสำคัญกับเครือข่าย

### Network Interface Controller (NIC)

**ชื่อเรียกต่างๆ:**
- Network Interface Card
- Network Adapter
- Network Interface Controller

**ข้อสำคัญ:**
- คอมพิวเตอร์สามารถมี NIC ได้หลายตัว (ทั้ง physical และ virtual)
- แต่ละ NIC สามารถมี IP address ได้
- การมี NIC หลายตัว = สามารถสื่อสารกับหลาย networks ได้
- **การระบุโอกาสในการ pivoting จะขึ้นอยู่กับ IP addresses ที่ถูกกำหนดให้กับ hosts ที่เรา compromise**
- IP addresses บ่งบอกว่า compromised hosts สามารถเข้าถึง networks ไหนได้บ้าง

### คำสั่งตรวจสอบ NICs

- **Linux/macOS:** `ifconfig`
- **Windows:** `ipconfig`

---

## ตัวอย่างการใช้ ifconfig (Linux)

```bash
$ ifconfig

# eth0 - Network Interface แรก
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 134.122.100.200  netmask 255.255.240.0  broadcast 134.122.111.255
        inet6 fe80::e973:b08d:7bdf:dc67  prefixlen 64  scopeid 0x20<link>
        ether 12:ed:13:35:68:f5  txqueuelen 1000  (Ethernet)

# eth1 - Network Interface ที่สอง
eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.106.0.172  netmask 255.255.240.0  broadcast 10.106.15.255
        inet6 fe80::a5bf:1cd4:9bca:b3ae  prefixlen 64  scopeid 0x20<link>
        ether 4e:c7:60:b0:01:8d  txqueuelen 1000  (Ethernet)

# lo - Loopback Interface
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)

# tun0 - VPN Tunnel Interface
tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.15.54  netmask 255.255.254.0  destination 10.10.15.54
        inet6 fe80::c85a:5717:5e3a:38de  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::1034  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
```

### การวิเคราะห์ Output

**แต่ละ NIC จะแสดง:**
- **Identifier:** ชื่อ interface (eth0, eth1, lo, tun0)
- **Addressing Information:** ข้อมูล IP address, netmask, broadcast
- **Traffic Statistics:** สถิติการรับส่งข้อมูล (RX/TX packets, bytes, errors)

**จุดสำคัญในตัวอย่าง:**

1. **tun0 (Tunnel Interface)**
   - บ่งบอกว่ามี VPN connection ทำงานอยู่
   - เมื่อเชื่อมต่อ HTB VPN จะมี tunnel interface ถูกสร้างและได้รับ IP
   - VPN ทำให้เราเข้าถึง lab networks ได้
   - VPN เข้ารหัส traffic และสร้าง tunnel ผ่าน public network

2. **eth0: 134.122.100.200**
   - **Public IP Address** (routable บน Internet)
   - ISPs จะ route traffic จาก IP นี้ผ่าน Internet
   - มักพบบนอุปกรณ์ที่อยู่ DMZ หรือหันหน้าสู่ Internet โดยตรง

3. **eth1, tun0: Private IP Addresses**
   - **Private IPs** (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
   - Route ได้ภายใน internal networks เท่านั้น
   - ไม่สามารถ route ผ่าน public Internet โดยตรง
   - ต้องใช้ NAT เพื่อแปลง private IP เป็น public IP

---

## ตัวอย่างการใช้ ipconfig (Windows)

```powershell
PS C:\Users\htb-student> ipconfig

Windows IP Configuration

# Adapter ที่ไม่ได้เชื่อมต่อ
Unknown adapter NordLynx:
   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

# Ethernet Adapter ที่ใช้งานอยู่
Ethernet adapter Ethernet0 2:
   Connection-specific DNS Suffix  . : .htb
   IPv6 Address. . . . . . . . . . . : dead:beef::1a9
   IPv6 Address. . . . . . . . . . . : dead:beef::f58b:6381:c648:1fb0
   Temporary IPv6 Address. . . . . . : dead:beef::dd0b:7cda:7118:3373
   Link-local IPv6 Address . . . . . : fe80::f58b:6381:c648:1fb0%8
   IPv4 Address. . . . . . . . . . . : 10.129.221.36
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb9:df81%8
                                       10.129.0.1

# Ethernet Adapter ที่ไม่ได้ใช้งาน
Ethernet adapter Ethernet:
   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
```

### การวิเคราะห์ Output

**จุดสังเกต:**
- ระบบมี adapters หลายตัว แต่มีแค่ตัวเดียวที่มี IP addresses
- มีทั้ง IPv6 และ IPv4 addresses
- **Dual-stack configuration** - ทรัพยากรเข้าถึงได้ทั้ง IPv4 และ IPv6

### Subnet Mask และ Default Gateway

**Subnet Mask:**
- ทุก IPv4 address จะมี subnet mask คู่กัน
- เปรียบเหมือน IP เป็นเบอร์โทรศัพท์, Subnet mask เป็นรหัสพื้นที่
- **กำหนด network portion และ host portion ของ IP address**

**Default Gateway:**
- เมื่อ traffic ไปยัง IP ที่อยู่คนละ network
- คอมพิวเตอร์จะส่ง traffic ไปที่ default gateway
- มักเป็น IP ของ NIC บน router ของ LAN นั้นๆ

**ความสำคัญสำหรับ Pivoting:**
- ต้องระวังว่า host ที่เรา compromise สามารถเข้าถึง networks ไหนได้บ้าง
- ควรบันทึกข้อมูล IP addressing ให้ครบถ้วน

---

## Routing (การกำหนดเส้นทาง)

### แนวคิด Router

**ความเข้าใจทั่วไป:**
- Router = อุปกรณ์ที่เชื่อมต่อเราสู่ Internet

**ความจริง:**
- คอมพิวเตอร์ทุกเครื่องสามารถกลายเป็น router ได้
- ทุกเครื่องสามารถมีส่วนร่วมใน routing ได้

### Pivoting และ Routing

**ความท้าทาย:**
- ในโมดูลนี้เราจะต้องทำให้ pivot host route traffic ไปยัง network อื่น

**ตัวอย่างเครื่องมือ:**
- **AutoRoute:** ทำให้ attack box มี routes ไปยัง target networks ที่เข้าถึงได้ผ่าน pivot host

### Routing Table

**คุณสมบัติสำคัญของ Router:**
- มี **routing table** เพื่อใช้ forward traffic ตาม destination IP address

**คำสั่งตรวจสอบ Routing Table:**
- `netstat -r`
- `ip route`

---

## ตัวอย่าง Routing Table

```bash
$ netstat -r

Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         178.62.64.1     0.0.0.0         UG        0 0          0 eth0
10.10.10.0      10.10.14.1      255.255.254.0   UG        0 0          0 tun0
10.10.14.0      0.0.0.0         255.255.254.0   U         0 0          0 tun0
10.106.0.0      0.0.0.0         255.255.240.0   U         0 0          0 eth1
10.129.0.0      10.10.14.1      255.255.0.0     UG        0 0          0 tun0
178.62.64.0     0.0.0.0         255.255.192.0   U         0 0          0 eth0
```

### การทำงานของ Routing Table

**กระบวนการตัดสินใจ:**
1. เมื่อ packet ถูกสร้างและมี destination
2. ก่อนออกจากคอมพิวเตอร์ จะใช้ routing table ตัดสินใจว่าจะส่งไปทางไหน

**ตัวอย่างการใช้งาน:**
```
เป้าหมาย: 10.129.10.25

การตรวจสอบ Routing Table:
- หา network ที่ตรงกับ destination
- พบว่าตรงกับ route: 10.129.0.0/16
- จะถูก forward ไปยัง Gateway: 10.10.14.1
- ออกทาง Interface: tun0
```

### การเรียนรู้ Routes

**Pwnbox (และเครื่องทั่วไป):**
- ไม่ใช้ routing protocols (EIGRP, OSPF, BGP)
- เรียนรู้ routes จาก directly connected interfaces (eth0, eth1, tun0)

**Routers แบบ Stand-alone:**
- เรียนรู้ routes ผ่าน:
  - Static routes (กำหนดเอง)
  - Dynamic routing protocols
  - Directly connected interfaces

### Default Route (Gateway of Last Resort)

**คำจำกัดความ:**
- Traffic ที่ไปยัง networks ที่ไม่มีใน routing table
- จะถูกส่งไปยัง **default route**

**ชื่อเรียกอื่นๆ:**
- Default gateway
- Gateway of last resort

**ประโยชน์สำหรับ Pivoting:**
- ดู routing table เพื่อระบุ networks ที่เราสามารถเข้าถึงได้
- ระบุ routes ที่อาจต้องเพิ่มเข้าไป

---

## Protocols, Services & Ports

### แนวคิดพื้นฐาน

**Protocols:**
- กฎที่ควบคุมการสื่อสารเครือข่าย

**Ports:**
- ตัวระบุที่สอดคล้องกับ protocols และ services
- **ไม่ใช่สิ่งที่จับต้องได้ทางกายภาพ**
- เป็นการกำหนดใน software ให้กับ applications

### การทำงานของ IP Address และ Port

**เปรียบเทียบ:**
- **IP Address** = บ้านเลขที่ (ระบุว่าคอมพิวเตอร์อยู่ที่ไหน)
- **Port** = ประตู/ห้อง (ระบุว่า application ไหนกำลังทำงาน)

**ตัวอย่าง:**
```
10.129.221.36:80
│            │
│            └─ Port 80 (HTTP service)
└─ IP Address (ตัวคอมพิวเตอร์)
```

### การใช้ Ports ใน Pivoting

**กลยุทธ์:**
- เชื่อมต่อกับ ports ที่ firewall อนุญาต
- ใช้ ports/protocols ที่ได้รับอนุญาตเพื่อเข้าสู่เครือข่าย

**ตัวอย่างจริง: Web Server**
```
Scenario: Web server ใช้ HTTP (port 80)

ปัญหา:
- Admin ต้องไม่บล็อก traffic ที่เข้ามาทาง port 80
- ถ้าบล็อก = ผู้ใช้จะเข้าเว็บไซต์ไม่ได้

โอกาสสำหรับเรา:
- Port 80 เปิดอยู่เพื่อ legitimate traffic
- เราสามารถใช้ช่องทางเดียวกันนี้เข้าสู่เครือข่าย
- ส่ง payload ผ่าน port เดียวกันกับ traffic ปกติ
```

### Source Ports และ Listeners

**ข้อควรระวัง:**
- **Source port** ถูกสร้างขึ้นเพื่อติดตาม established connections
- ต้องระวังว่าเราใช้ ports ไหน
- เมื่อ execute payloads ต้องแน่ใจว่าจะ connect กลับมาที่ listeners ที่เราตั้งไว้
- ต้องใช้ความคิดสร้างสรรค์กับการใช้ ports

---

## คำแนะนำจาก LTNB0B

### แนวทางการเรียนรู้

**จุดประสงค์ของโมดูล:**
- ฝึกใช้เครื่องมือและเทคนิคต่างๆ
- Pivot ผ่าน hosts
- Forward local/remote services ไปยัง attack host
- เข้าถึง targets ที่เชื่อมต่อกับ networks ต่างๆ

**ระดับความยาก:**
- เพิ่มขึ้นแบบค่อยเป็นค่อยไป
- มี multi-host networks ให้ฝึกฝน

### เทคนิคการเรียนรู้ที่แนะนำ

1. **ฝึกหลายวิธี:**
   - ลองใช้เครื่องมือต่างๆ
   - คิดสร้างสรรค์
   - ทดลองหลาย approaches

2. **วาด Network Topology:**
   - ใช้เครื่องมือ network diagramming
   - เช่น **Draw.io**
   - ประโยชน์:
     - เห็นภาพรวมของเครือข่าย
     - เป็น documentation ที่ดี
     - ช่วยค้นหาโอกาส pivot

3. **สร้าง Visual Network Environment:**
   - วาดแผนผังเครือข่ายที่เรากำลังทำงานด้วย
   - เป็นเครื่องมือ documentation ที่เยี่ยม

### ข้อความสำคัญ

> "This module is a lot of fun and will put your networking skills to the test. Have fun, and never stop learning!"
> 
> *โมดูลนี้สนุกมาก และจะทดสอบทักษะ networking ของคุณ สนุกไปกับมัน และอย่าหยุดเรียนรู้!*

---

## สรุปประเด็นสำคัญ

### เพื่อความสำเร็จใน Pivoting ต้องเข้าใจ:

1. **IP Addressing & NICs**
   - ตรวจสอบ NICs ด้วย `ifconfig`/`ipconfig` เสมอ
   - มองหา dual-homed hosts (มีหลาย NICs)
   - แยกแยะ public vs private IPs

2. **Routing**
   - ศึกษา routing table ด้วย `netstat -r`
   - เข้าใจว่า traffic จะไปทางไหน
   - ระบุ networks ที่เข้าถึงได้

3. **Protocols & Ports**
   - ใช้ ports ที่ firewall อนุญาต
   - เข้าใจ source/destination ports
   - คิดสร้างสรรค์กับการใช้ services ที่เปิดอยู่

4. **Documentation**
   - บันทึก IP addressing ทั้งหมด
   - วาดแผนผัง network topology
   - ติดตาม routes และ connections