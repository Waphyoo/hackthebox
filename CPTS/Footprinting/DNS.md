#  DNS (Domain Name System) 

DNS เปรียบเสมือน "สมุดโทรศัพท์ของอินเทอร์เน็ต" ที่ช่วยแปลชื่อเว็บไซต์ (เช่น www.hackthebox.com) ให้เป็นตัวเลข IP address ที่คอมพิวเตอร์เข้าใจได้

**ทำไมต้องมี DNS?**
เพราะคนจำชื่อเว็บไซต์ได้ง่ายกว่าจำตัวเลข IP address (เช่น 192.168.1.1)

## ประเภทของเซิร์ฟเวอร์ DNS

**1. DNS Root Server (เซิร์ฟเวอร์รากหลัก)**
- เป็นตัวจัดการโดเมนระดับบนสุด เช่น .com, .net, .org
- มีทั้งหมด 13 เครื่องทั่วโลก
- ทำงานเป็นตัวกลางระหว่างผู้ใช้กับเนื้อหาบนอินเทอร์เน็ต

**2. Authoritative Nameserver (เซิร์ฟเวอร์ที่มีอำนาจ)**
- เป็นเจ้าของข้อมูลโดเมนจริงๆ
- ให้คำตอบที่เชื่อถือได้ 100% สำหรับโดเมนที่ดูแล

**3. Non-authoritative Nameserver**
- ไม่ใช่เจ้าของข้อมูลโดเมน
- เก็บข้อมูลที่รวบรวมมาจากเซิร์ฟเวอร์อื่นๆ

**4. Caching DNS Server (เซิร์ฟเวอร์แคช)**
- จดจำคำตอบที่เคยค้นหาไว้ชั่วคราว
- ช่วยให้การเข้าเว็บไซต์เร็วขึ้น

**5. Forwarding Server**
- ส่งต่อคำขอไปยังเซิร์ฟเวอร์อื่นเท่านั้น

**6. Resolver**
- ทำงานในคอมพิวเตอร์หรือเราเตอร์ของเรา
- แปลงชื่อโดเมนเป็น IP address

## โครงสร้างลำดับชั้นของโดเมน

จากบนลงล่าง:
1. **Root** (รากหลัก)
2. **Top Level Domain (TLD)** - เช่น .com, .net, .org, .io
3. **Second Level Domain** - เช่น inlanefreight.com
4. **Sub-Domain** - เช่น www.inlanefreight.com, mail.inlanefreight.com
5. **Host** - เช่น WS01.dev.inlanefreight.com

## ประเภทของ DNS Record (บันทึกข้อมูล DNS)

- **A Record** = เก็บ IP address แบบ IPv4
- **AAAA Record** = เก็บ IP address แบบ IPv6
- **MX Record** = บอกว่าเซิร์ฟเวอร์อีเมลอยู่ที่ไหน
- **NS Record** = บอกว่าเซิร์ฟเวอร์ DNS ของโดเมนนี้คือใคร
- **TXT Record** = เก็บข้อมูลเสริมต่างๆ เช่น ยืนยัน SSL หรือป้องกันสแปม
- **CNAME Record** = ชื่อเล่นของโดเมน (Alias) ชี้ไปยังโดเมนอื่น
- **PTR Record** = ทำงานตรงข้าม แปลง IP เป็นชื่อโดเมน
- **SOA Record** = ข้อมูลเกี่ยวกับเขต DNS และอีเมลผู้ดูแล


## SOA Record คืออะไร?

**SOA (Start of Authority)** เป็นบันทึกที่อยู่ในไฟล์ zone ของโดเมน ที่บอกว่า:
- **ใครเป็นผู้รับผิดชอบ**ในการดูแลโดเมนนี้
- **จัดการข้อมูล DNS** ของโดเมนอย่างไร

```
Watunyoo@htb[/htb]$ dig soa www.inlanefreight.com

; <<>> DiG 9.16.27-Debian <<>> soa www.inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15876
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.inlanefreight.com.         IN      SOA

;; AUTHORITY SECTION:
inlanefreight.com.      900     IN      SOA     ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Jan 05 12:56:10 GMT 2023
;; MSG SIZE  rcvd: 128
```

## แปลความหมายแต่ละส่วน:

1. **ns-161.awsdns-20.com** 
   - เซิร์ฟเวอร์ DNS หลัก (Primary nameserver)

2. **awsdns-hostmaster.amazon.com**
   - อีเมลของผู้ดูแลระบบ
   - **วิธีอ่าน:** เปลี่ยนจุด (.) ตัวแรกเป็น @ 
   - **ได้เป็น:** awsdns-hostmaster@amazon.com

3. **1** - Serial number (หมายเลขเวอร์ชันของไฟล์ zone)

4. **7200** - Refresh time (7200 วินาที = 2 ชั่วโมง)
   - เวลาที่เซิร์ฟเวอร์รองจะเช็คอัปเดตจากเซิร์ฟเวอร์หลัก

5. **900** - Retry time (900 วินาที = 15 นาที)
   - หากเช็คไม่สำเร็จ จะลองใหม่ภายในเวลานี้

6. **1209600** - Expire time (1209600 วินาที = 14 วัน)
   - หากติดต่อเซิร์ฟเวอร์หลักไม่ได้นานขนาดนี้ ให้หยุดให้บริการ

7. **86400** - Minimum TTL (86400 วินาที = 1 วัน)
   - เวลาขั้นต่ำที่ข้อมูลจะถูกเก็บแคชไว้



## ไฟล์การตั้งค่า DNS มี 3 ประเภท

1. **Local DNS configuration files** - ไฟล์ตั้งค่าทั่วไป
2. **Zone files** - ไฟล์ข้อมูลโดเมน
3. **Reverse name resolution files** - ไฟล์แปลง IP เป็นชื่อโดเมน

## DNS Server Bind9

Bind9 เป็น DNS server ที่นิยมใช้ใน Linux โดยไฟล์ตั้งค่าหลักคือ **named.conf** แบ่งเป็น 2 ส่วน:
- **Options section** - ตั้งค่าทั่วไป
- **Zone entries** - ข้อมูลแต่ละโดเมน

### ไฟล์ตั้งค่าหลักประกอบด้วย:
- `named.conf.local`
- `named.conf.options`
- `named.conf.log`

---

## 1. Local DNS Configuration (ไฟล์ตั้งค่าโซน)

```bash
cat /etc/bind/named.conf.local
```

**ตัวอย่างเนื้อหา:**
```
zone "domain.com" {
    type master;
    file "/etc/bind/db.domain.com";
    allow-update { key rndc-key; };
};
```

### อธิบาย:
- **zone "domain.com"** - กำหนดโซนสำหรับโดเมน domain.com
- **type master** - เซิร์ฟเวอร์นี้เป็นเจ้าของข้อมูลหลัก
- **file** - ระบุตำแหน่งไฟล์ zone file
- **allow-update** - อนุญาตให้อัปเดตข้อมูลด้วย key

**หมายเหตุ:**
- **Global options** = ตั้งค่าที่ใช้กับทุกโซน
- **Zone options** = ตั้งค่าเฉพาะโซนนั้น (มีความสำคัญเหนือกว่า global options)

---

## 2. Zone Files (ไฟล์ข้อมูลโดเมน)

Zone file เป็นไฟล์ข้อความที่อธิบายข้อมูล DNS zone โดยใช้ BIND file format ซึ่งเป็นมาตรฐานอุตสาหกรรม

**กฎสำคัญ:**
- ต้องมี **SOA record** เพียง 1 รายการ
- ต้องมี **NS record** อย่างน้อย 1 รายการ
- ถ้ามีข้อผิดพลาดในไฟล์ = zone ทั้งหมดจะไม่สามารถใช้งานได้
- DNS server จะตอบด้วย **SERVFAIL** error

```bash
cat /etc/bind/db.domain.com
```

**ตัวอย่าง Zone File:**

```
$ORIGIN domain.com
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial (หมายเลขเวอร์ชัน)
                    21600      ; refresh after 6 hours (รีเฟรชทุก 6 ชม.)
                    3600       ; retry after 1 hour (ลองใหม่ทุก 1 ชม.)
                    604800     ; expire after 1 week (หมดอายุ 1 สัปดาห์)
                    86400 )    ; minimum TTL of 1 day (TTL ขั้นต่ำ 1 วัน)

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

      IN     MX     10     mx.domain.com.
      IN     MX     20     mx2.domain.com.

             IN     A       10.129.14.5

server1      IN     A       10.129.14.5
server2      IN     A       10.129.14.7
ns1          IN     A       10.129.14.2
ns2          IN     A       10.129.14.3

ftp          IN     CNAME   server1
mx           IN     CNAME   server1
mx2          IN     CNAME   server2
www          IN     CNAME   server2
```

### อธิบายแต่ละส่วน:

**$ORIGIN domain.com**
- กำหนดโดเมนหลักของไฟล์นี้

**$TTL 86400**
- Time To Live = 86400 วินาที (1 วัน)
- เวลาที่ข้อมูลจะถูกเก็บแคชไว้

**@ IN SOA**
- @ = หมายถึงโดเมนหลัก (domain.com)
- IN = Internet class
- SOA = Start of Authority

**NS Records**
- ระบุ nameserver ที่ดูแลโดเมนนี้
- มี ns1 และ ns2

**MX Records (Mail Exchange)**
- 10, 20 = ระดับความสำคัญ (ตัวเลขน้อย = สำคัญกว่า)
- mx.domain.com มีความสำคัญมากกว่า mx2.domain.com

**A Records**
- เชื่อมชื่อโฮสต์กับ IP address
- server1 → 10.129.14.5
- server2 → 10.129.14.7

**CNAME Records (Alias)**
- ftp → ชี้ไปที่ server1
- www → ชี้ไปที่ server2
- mx → ชี้ไปที่ server1

---

## 3. Reverse Name Resolution Zone Files (ไฟล์แปลง IP เป็นชื่อ)

ใช้สำหรับแปลง IP address กลับเป็นชื่อโดเมน (FQDN) โดยใช้ **PTR records**

```bash
cat /etc/bind/db.10.129.14
```

**ตัวอย่าง:**

```
$ORIGIN 14.129.10.in-addr.arpa
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

5    IN     PTR    server1.domain.com.
7    IN     MX     mx.domain.com.
```

### อธิบาย:

**$ORIGIN 14.129.10.in-addr.arpa**
- กลับลำดับของ IP address: 10.129.14 → 14.129.10
- เติม .in-addr.arpa ท้าย (มาตรฐานสำหรับ reverse DNS)

**PTR Records**
- **5** → ตัวเลขสุดท้ายของ IP (10.129.14.5)
- ชี้ไปที่ server1.domain.com
- **7** → 10.129.14.7 ชี้ไปที่ mx.domain.com

---

## การตั้งค่าที่อันตราย (Dangerous Settings)

DNS server มีช่องโหว่มากมาย การตั้งค่าผิดพลาดอาจทำให้ระบบถูกโจมตีได้

### ตัวเลือกที่อาจเป็นอันตราย:

| ตัวเลือก | คำอธิบาย |
|---------|----------|
| **allow-query** | กำหนดว่าโฮสต์ไหนบ้างที่ส่งคำขอ (query) มาที่ DNS server ได้ |
| **allow-recursion** | กำหนดว่าโฮสต์ไหนบ้างที่ส่งคำขอแบบ recursive มาได้ |
| **allow-transfer** | กำหนดว่าโฮสต์ไหนบ้างที่รับ zone transfer (คัดลอกข้อมูล zone) ได้ |
| **zone-statistics** | เก็บสถิติข้อมูลของ zone |

### ปัญหาที่พบบ่อย:

🔴 **ความปลอดภัย vs การทำงาน**
- ผู้ดูแลระบบมักตั้งค่าให้ระบบทำงานได้ก่อน (functionality > security)
- การแก้ปัญหาชั่วคราวอาจเปิดช่องโหว่โดยไม่รู้ตัว
- การตั้งค่าผิดพลาด (misconfiguration) เป็นสาเหตุหลักของช่องโหว่

### ตัวอย่างความเสี่ยง:

- **allow-query { any; }** = ทุกคนสามารถ query ได้ → อาจถูกโจมตี DDoS
- **allow-transfer { any; }** = ทุกคนคัดลอกข้อมูล zone ได้ → รั่วไหลข้อมูล
- **allow-recursion { any; }** = ทุกคนใช้เซิร์ฟเวอร์เป็นตัวกลางได้ → ถูกใช้ในการโจมตี

---

## สรุป

✅ **ไฟล์สำคัญ 3 ประเภท:**
1. Local config - ตั้งค่าทั่วไป
2. Zone files - ข้อมูลโดเมน (A, CNAME, MX, NS)
3. Reverse files - แปลง IP เป็นชื่อ (PTR)

⚠️ **ข้อควรระวัง:**
- Zone file ต้องมี SOA และ NS record
- ข้อผิดพลาดในไฟล์ = zone ใช้งานไม่ได้
- การตั้งค่าที่ไม่ระมัดระวังอาจเปิดช่องโหว่

# การสำรวจข้อมูล DNS (DNS Footprinting)

การสำรวจข้อมูล DNS เกิดจากคำขอ (requests) ที่เราส่งไปยัง DNS server เพื่อค้นหาข้อมูลต่างๆ

---

## 1. การค้นหา Name Servers (NS Query)

เราสามารถสอบถาม DNS server ว่ามี name servers อื่นๆ ที่รู้จักหรือไม่ โดยใช้ **NS record**

### คำสั่ง DIG - NS Query

```bash
dig ns inlanefreight.htb @10.129.14.128
```

**คำอธิบาย:**
- `dig` = เครื่องมือสอบถาม DNS
- `ns` = ขอดู NS records
- `inlanefreight.htb` = โดเมนที่ต้องการตรวจสอบ
- `@10.129.14.128` = DNS server ที่จะสอบถาม

### ผลลัพธ์:

```
;; QUESTION SECTION:
;inlanefreight.htb.             IN      NS

;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
```

**แปลความหมาย:**
- โดเมน inlanefreight.htb มี name server คือ **ns.inlanefreight.htb**
- Name server นี้อยู่ที่ IP **10.129.34.136**
- **604800** วินาที = TTL (Time To Live) ประมาณ 7 วัน

**ทำไมต้องรู้จัก NS อื่นๆ?**
- DNS servers อื่นอาจตั้งค่าต่างกัน
- อาจมีข้อมูลเพิ่มเติมสำหรับ zones อื่นๆ
- เราสามารถใช้ server เหล่านี้ในการค้นหาข้อมูลเพิ่มเติม

---

## 2. การตรวจสอบเวอร์ชัน DNS Server (Version Query)

บางครั้งเราสามารถตรวจสอบเวอร์ชันของ DNS server ได้โดยใช้ **class CHAOS** และ **type TXT**

### คำสั่ง DIG - Version Query

```bash
dig CH TXT version.bind 10.129.120.85
```

**คำอธิบาย:**
- `CH` = CHAOS class
- `TXT` = ประเภทของ record
- `version.bind` = คำสั่งพิเศษสำหรับดูเวอร์ชัน

### ผลลัพธ์:

```
;; ANSWER SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1"

;; ADDITIONAL SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1-Debian"
```

**แปลความหมาย:**
- DNS server ใช้ BIND เวอร์ชัน **9.10.6-P1**
- ระบบปฏิบัติการคือ **Debian**

**หมายเหตุ:** การรู้เวอร์ชันช่วยให้เราทราบว่ามีช่องโหว่ความปลอดภัยหรือไม่

---

## 3. การดูข้อมูลทั้งหมด (ANY Query)

ใช้ตัวเลือก **ANY** เพื่อดูข้อมูลทั้งหมดที่ DNS server ยินดีเปิดเผย

### คำสั่ง DIG - ANY Query

```bash
dig any inlanefreight.htb @10.129.14.128
```

### ผลลัพธ์:

```
;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
```

**ข้อมูลที่ได้:**

**TXT Records:**
- **SPF record** - ระบุ mail servers ที่ได้รับอนุญาตให้ส่งอีเมลในนามของโดเมนนี้
  - รวม mailgun.org, Google, Outlook, Atlassian
  - IP addresses: 10.129.124.8, 10.129.127.2, 10.129.42.106
- **Domain verification** - ยืนยันความเป็นเจ้าของโดเมนกับ Atlassian
- **MS record** - ยืนยันกับ Microsoft

**SOA Record:**
- ข้อมูลผู้ดูแลและพารามิเตอร์ของ zone

**NS Record:**
- Name server ของโดเมน

⚠️ **สำคัญ:** การ query แบบ ANY จะไม่แสดงข้อมูลทั้งหมดใน zone เสมอไป

---

## 4. Zone Transfer (AXFR) - การถ่ายโอนข้อมูล Zone

### Zone Transfer คืออะไร?

**Zone Transfer** หรือ **AXFR (Asynchronous Full Transfer Zone)** คือการถ่ายโอนไฟล์ zone ทั้งหมดจาก DNS server หนึ่งไปยังอีก server หนึ่ง

**วัตถุประสงค์:**
- เพิ่ม **ความน่าเชื่อถือ** (reliability)
- **กระจายโหลด** (load distribution)
- **ป้องกัน primary server** จากการโจมตี
- **ซิงค์ข้อมูล** ระหว่าง primary และ secondary servers

### โครงสร้าง DNS Server

**Primary Name Server:**
- มีข้อมูล zone ต้นฉบับ
- สามารถสร้าง แก้ไข หรือลบ DNS records ได้
- เป็น **master** เสมอ

**Secondary Name Server:**
- คัดลอกข้อมูลจาก primary
- สามารถเป็นทั้ง **slave** และ **master**
- ช่วยเพิ่มความน่าเชื่อถือและกระจายโหลด

**Master vs Slave:**
- **Master** = แหล่งข้อมูลหลักสำหรับการซิงค์
- **Slave** = รับข้อมูลจาก master
- Primary เป็น master เสมอ
- Secondary อาจเป็นทั้ง slave และ master

### กระบวนการ Zone Transfer

1. **Slave ดึง SOA record** จาก master ทุกช่วงเวลา (refresh time) โดยปกติ 1 ชั่วโมง
2. **เปรียบเทียบ serial number** ใน SOA record
3. ถ้า serial number ของ master **มากกว่า** slave = ข้อมูลไม่ตรงกัน
4. Slave จะ**ถ่ายโอนข้อมูล zone ทั้งหมด**จาก master

**การใช้งาน:**
- ทำงานผ่าน **TCP port 53**
- ใช้ **secret key (rndc-key)** ยืนยันตัวตน
- บังคับใช้กับ Top-Level Domains (TLDs) บางตัว

---

## 5. การทดสอบ Zone Transfer (AXFR Attack)

### คำสั่ง DIG - AXFR Zone Transfer

```bash
dig axfr inlanefreight.htb @10.129.14.128
```

### ผลลัพธ์:

```
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
internal.inlanefreight.htb. 604800 IN   A       10.129.1.6
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800

;; XFR size: 9 records (messages 1, bytes 520)
```

**ข้อมูลที่ได้รับ:**
- **app.inlanefreight.htb** → 10.129.18.15
- **internal.inlanefreight.htb** → 10.129.1.6
- **mail1.inlanefreight.htb** → 10.129.18.201
- **ns.inlanefreight.htb** → 10.129.34.136

---

## 6. การโจมตี Internal Zone Transfer

### คำสั่ง DIG - AXFR Internal Zone

```bash
dig axfr internal.inlanefreight.htb @10.129.14.128
```

### ผลลัพธ์:

```
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
internal.inlanefreight.htb. 604800 IN   TXT     "MS=ms97310371"
internal.inlanefreight.htb. 604800 IN   TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
internal.inlanefreight.htb. 604800 IN   TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
internal.inlanefreight.htb. 604800 IN   NS      ns.inlanefreight.htb.
dc1.internal.inlanefreight.htb. 604800 IN A     10.129.34.16
dc2.internal.inlanefreight.htb. 604800 IN A     10.129.34.11
mail1.internal.inlanefreight.htb. 604800 IN A   10.129.18.200
ns.internal.inlanefreight.htb. 604800 IN A      10.129.34.136
vpn.internal.inlanefreight.htb. 604800 IN A     10.129.1.6
ws1.internal.inlanefreight.htb. 604800 IN A     10.129.1.34
ws2.internal.inlanefreight.htb. 604800 IN A     10.129.1.35
wsus.internal.inlanefreight.htb. 604800 IN A    10.129.18.2
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800

;; XFR size: 15 records (messages 1, bytes 664)
```

**ข้อมูลภายในที่รั่วไหล:**
- **dc1** (Domain Controller 1) → 10.129.34.16
- **dc2** (Domain Controller 2) → 10.129.34.11
- **mail1** → 10.129.18.200
- **vpn** → 10.129.1.6
- **ws1** (Workstation 1) → 10.129.1.34
- **ws2** (Workstation 2) → 10.129.1.35
- **wsus** (Windows Server Update Services) → 10.129.18.2

🚨 **อันตราย!** ข้อมูลภายในเครือข่ายรั่วไหลทั้งหมด!

---

## ช่องโหว่ที่เกิดจากการตั้งค่าผิดพลาด

### สาเหตุของปัญหา:

❌ **การตั้งค่าที่อันตราย:**

```
allow-transfer { any; };
```

หรือ

```
allow-transfer { 10.129.0.0/16; };
```

**ผลที่ตามมา:**
- ใครก็ได้สามารถ query zone file ทั้งหมด
- เปิดเผยข้อมูล **Internal IP addresses**
- เปิดเผย **Hostnames** ภายในเครือข่าย
- ผู้โจมตีสามารถวางแผนโจมตีได้ง่ายขึ้น

### สถานการณ์ที่พบบ่อย:

**ผู้ดูแลระบบตั้งค่าแบบนี้เพราะ:**
- เพื่อทดสอบระบบ (testing purposes)
- แก้ปัญหาชั่วคราว (workaround solution)
- ไม่เข้าใจความเสี่ยงด้านความปลอดภัย

---

## 7. Brute-Force Attack - การเดาชื่อ Subdomain


## ใช้เครื่องมือ DNSenum

**DNSenum** เป็นเครื่องมือสำเร็จรูปที่ออกแบบมาสำหรับ DNS enumeration โดยเฉพาะ

### คำสั่ง DNSenum:

```bash
dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb
```

### อธิบายพารามิเตอร์:

| พารามิเตอร์ | คำอธิบาย |
|------------|---------|
| `--dnsserver 10.129.14.128` | ระบุ DNS server ที่จะ query |
| `--enum` | เปิดใช้งาน enumeration mode |
| `-p 0` | ไม่ทำ Google scraping (0 = ปิด) |
| `-s 0` | ไม่ทำ subdomain scraping (0 = ปิด) |
| `-o subdomains.txt` | บันทึกผลลัพธ์ลงไฟล์ |
| `-f /path/to/wordlist.txt` | ระบุไฟล์ wordlist สำหรับ brute-force |
| `inlanefreight.htb` | โดเมนเป้าหมาย |

---

### ผลลัพธ์จาก DNSenum:

```
dnsenum VERSION:1.2.6

-----   inlanefreight.htb   -----

Host's addresses:
__________________

Name Servers:
______________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136

Mail (MX) Servers:
___________________

Trying Zone Transfers and getting Bind Versions:
_________________________________________________

unresolvable name: ns.inlanefreight.htb at /usr/bin/dnsenum line 900 thread 1.

Trying Zone Transfer for inlanefreight.htb on ns.inlanefreight.htb ...
AXFR record query failed: no nameservers

Brute forcing with /home/cry0l1t3/Pentesting/SecLists/Discovery/DNS/subdomains-top1million-110000.txt:
_______________________________________________________________________________________________________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136
mail1.inlanefreight.htb.                 604800   IN    A        10.129.18.201
app.inlanefreight.htb.                   604800   IN    A        10.129.18.15
ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136

done.
```

---

### วิเคราะห์ผลลัพธ์:

#### **1. Host's addresses:**
- (ว่างเปล่า) - ไม่มี IP address หลักของโดเมน

#### **2. Name Servers:**
```
ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136
```
- พบ name server: **ns.inlanefreight.htb** → 10.129.34.136

#### **3. Mail (MX) Servers:**
- (ว่างเปล่า) - ไม่มี MX records

#### **4. Trying Zone Transfers:**
```
AXFR record query failed: no nameservers
```
- ❌ **Zone Transfer ล้มเหลว** - DNS server ไม่อนุญาตให้ transfer zone

#### **5. Brute Forcing Results:**
```
ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136
mail1.inlanefreight.htb.                 604800   IN    A        10.129.18.201
app.inlanefreight.htb.                   604800   IN    A        10.129.18.15
```
- ✅ พบ **3 subdomains** จากการ brute-force

---


---

## สรุปเทคนิค DNS Footprinting

### เครื่องมือหลัก: **dig**

**1. NS Query** - หา name servers อื่นๆ
```bash
dig ns domain.com @dns-server
```

**2. Version Query** - ตรวจสอบเวอร์ชัน DNS
```bash
dig CH TXT version.bind dns-server
```

**3. ANY Query** - ดูข้อมูลทั้งหมด
```bash
dig any domain.com @dns-server
```

**4. AXFR Zone Transfer** - ถ่ายโอน zone file
```bash
dig axfr domain.com @dns-server
```

**5. Brute-Force** - เดา subdomain
```bash
dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb


gobuster dns --do dev.inlanefreight.htb -w /usr/share/seclists/Discovery/DNS/fierce-hostlist.txt --resolver 10.129.244.143
```

---

