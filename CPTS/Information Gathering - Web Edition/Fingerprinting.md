# Fingerprinting (การระบุลายนิ้วมือดิจิทัล)

## Fingerprinting คืออะไร?

**Fingerprinting** เน้นที่การดึงรายละเอียดทางเทคนิคเกี่ยวกับเทคโนโลยีที่ขับเคลื่อนเว็บไซต์หรือเว็บแอปพลิเคชัน เหมือนกับที่ลายนิ้วมือระบุบุคคลได้อย่างเฉพาะเจาะจง ลายเซ็นดิจิทัลของเว็บเซิร์ฟเวอร์, ระบบปฏิบัติการ และส่วนประกอบซอฟต์แวร์ สามารถเปิดเผยข้อมูลสำคัญเกี่ยวกับโครงสร้างพื้นฐานของเป้าหมายและจุดอ่อนด้านความปลอดภัยที่อาจเกิดขึ้น

## ทำไม Fingerprinting จึงสำคัญ?

Fingerprinting เป็นรากฐานสำคัญของการสอดแนมเว็บด้วยเหตุผลหลายประการ:

| เหตุผล | คำอธิบาย | ประโยชน์ |
|--------|----------|----------|
| **การโจมตีแบบเฉพาะเจาะจง** (Targeted Attacks) | เมื่อทราบเทคโนโลยีเฉพาะที่ใช้งาน ผู้โจมตีสามารถมุ่งเน้นความพยายามไปที่ช่องโหว่ที่รู้จักว่ามีผลกับระบบเหล่านั้น | เพิ่มโอกาสความสำเร็จในการบุกรุกอย่างมีนัยสำคัญ |
| **ระบุการตั้งค่าที่ผิดพลาด** (Identifying Misconfigurations) | สามารถเปิดเผยซอฟต์แวร์ที่ตั้งค่าผิดหรือล้าสมัย การตั้งค่าเริ่มต้น หรือจุดอ่อนอื่นๆ | พบช่องโหว่ที่อาจไม่เห็นได้ชัดจากวิธีการสอดแนมอื่น |
| **จัดลำดับความสำคัญเป้าหมาย** (Prioritising Targets) | เมื่อเผชิญกับเป้าหมายที่เป็นไปได้หลายรายการ | ช่วยระบุระบบที่มีแนวโน้มจะมีช่องโหว่หรือมีข้อมูลที่มีค่า |
| **สร้างโปรไฟล์ที่ครอบคลุม** (Building Comprehensive Profile) | รวมข้อมูล fingerprint กับผลการสอดแนมอื่นๆ | สร้างภาพรวมแบบองค์รวมของโครงสร้างพื้นฐานของเป้าหมาย ช่วยเข้าใจท่าทีด้านความปลอดภัยโดยรวม |

## เทคนิคการทำ Fingerprinting

### เทคนิคหลัก

| เทคนิค | คำอธิบาย | วิธีการ |
|--------|----------|---------|
| **Banner Grabbing** | วิเคราะห์ banner ที่แสดงโดยเว็บเซิร์ฟเวอร์และบริการอื่นๆ | Banner มักเปิดเผยซอฟต์แวร์เซิร์ฟเวอร์ หมายเลขเวอร์ชัน และรายละเอียดอื่นๆ |
| **Analysing HTTP Headers** | วิเคราะห์ HTTP headers ที่ส่งพร้อมกับทุกคำขอและการตอบกลับหน้าเว็บ | `Server` header เปิดเผยซอฟต์แวร์เว็บเซิร์ฟเวอร์<br>`X-Powered-By` header อาจเปิดเผยเทคโนโลยีเพิ่มเติม |
| **Probing for Specific Responses** | ส่งคำขอที่สร้างขึ้นเป็นพิเศษไปยังเป้าหมาย | ได้รับการตอบกลับที่เป็นเอกลักษณ์ซึ่งเปิดเผยเทคโนโลยีหรือเวอร์ชันเฉพาะ |
| **Analysing Page Content** | วิเคราะห์เนื้อหาของหน้าเว็บ | โครงสร้าง, สคริปต์ และองค์ประกอบอื่นๆ อาจให้เบาะแสเกี่ยวกับเทคโนโลยีพื้นฐาน |

## เครื่องมือสำหรับ Fingerprinting

| เครื่องมือ | คำอธิบาย | ฟีเจอร์หลัก |
|-----------|----------|-------------|
| **Wappalyzer** | Browser extension และ online service สำหรับการทำโปรไฟล์เทคโนโลยีเว็บไซต์ | ระบุเทคโนโลยีเว็บที่หลากหลาย รวมถึง CMSs, frameworks, analytics tools และอื่นๆ |
| **BuiltWith** | Web technology profiler ที่ให้รายงานโดยละเอียดเกี่ยวกับ technology stack ของเว็บไซต์ | มีทั้งแผนฟรีและแผนแบบเสียเงินที่มีระดับรายละเอียดแตกต่างกัน |
| **WhatWeb** | เครื่องมือ command-line สำหรับ website fingerprinting | ใช้ฐานข้อมูล signatures ขนาดใหญ่เพื่อระบุเทคโนโลยีเว็บต่างๆ |
| **Nmap** | Network scanner อเนกประสงค์สำหรับงาน reconnaissance ต่างๆ | สามารถใช้กับสคริปต์ (NSE) เพื่อทำ fingerprinting เฉพาะทางมากขึ้น |
| **Netcraft** | ให้บริการด้านความปลอดภัยเว็บหลากหลาย | รายงานโดยละเอียดเกี่ยวกับเทคโนโลยี, hosting provider และท่าทีด้านความปลอดภัย |
| **wafw00f** | เครื่องมือ command-line ออกแบบเฉพาะสำหรับระบุ Web Application Firewalls (WAFs) | ช่วยกำหนดว่ามี WAF หรือไม่ และถ้ามี ประเภทและการตั้งค่าคืออะไร |

## กรณีศึกษา: Fingerprinting inlanefreight.com

### 1. Banner Grabbing

ใช้คำสั่ง `curl` พร้อม flag `-I` เพื่อดึงเฉพาะ HTTP headers:

```bash
curl -I inlanefreight.com
```

**ผลลัพธ์:**
```
HTTP/1.1 301 Moved Permanently
Date: Fri, 31 May 2024 12:07:44 GMT
Server: Apache/2.4.41 (Ubuntu)
Location: https://inlanefreight.com/
Content-Type: text/html; charset=iso-8859-1
```

**การวิเคราะห์:** 
- เว็บไซต์ใช้ `Apache/2.4.41 (Ubuntu)`
- มีการ redirect ไปยัง HTTPS

**ตรวจสอบ HTTPS:**
```bash
curl -I https://inlanefreight.com
```

**ผลลัพธ์:**
```
HTTP/1.1 301 Moved Permanently
Date: Fri, 31 May 2024 12:12:12 GMT
Server: Apache/2.4.41 (Ubuntu)
X-Redirect-By: WordPress
Location: https://www.inlanefreight.com/
Content-Type: text/html; charset=UTF-8
```

**การวิเคราะห์:** 
- พบ header `X-Redirect-By: WordPress` - เว็บไซต์ใช้ **WordPress**!

**ตรวจสอบ URL สุดท้าย:**
```bash
curl -I https://www.inlanefreight.com
```

**ผลลัพธ์:**
```
HTTP/1.1 200 OK
Date: Fri, 31 May 2024 12:12:26 GMT
Server: Apache/2.4.41 (Ubuntu)
Link: <https://www.inlanefreight.com/index.php/wp-json/>; rel="https://api.w.org/"
Link: <https://www.inlanefreight.com/index.php/wp-json/wp/v2/pages/7>; rel="alternate"; type="application/json"
Link: <https://www.inlanefreight.com/>; rel=shortlink
Content-Type: text/html; charset=UTF-8
```

**การวิเคราะห์:**
- พบ path ที่มี `wp-json` - ยืนยัน WordPress
- `wp-` prefix เป็นเอกลักษณ์ของ WordPress

### 2. การตรวจจับ WAF ด้วย Wafw00f

**การติดตั้ง:**
```bash
pip3 install git+https://github.com/EnableSecurity/wafw00f
```

**การใช้งาน:**
```bash
wafw00f inlanefreight.com
```

**ผลลัพธ์:**
```
[*] Checking https://inlanefreight.com
[+] The site https://inlanefreight.com is behind Wordfence (Defiant) WAF.
[~] Number of requests: 2
```

**การวิเคราะห์:**
- เว็บไซต์ได้รับการปกป้องโดย **Wordfence WAF** (พัฒนาโดย Defiant)
- มีชั้นความปลอดภัยเพิ่มเติมที่อาจบล็อกหรือกรองความพยายามในการสอดแนม
- ต้องปรับเทคนิคเพื่อหลบเลี่ยงหรือหลีกเลี่ยงกลไกการตรวจจับของ WAF

### 3. การสแกนด้วย Nikto
Nikto เป็น web server scanner แบบ open-source ที่ทรงพลัง นอกจากจะเป็นเครื่องมือประเมินช่องโหว่หลักแล้ว ความสามารถด้าน fingerprinting ของ Nikto ยังให้ข้อมูลเชิงลึกเกี่ยวกับ technology stack ของเว็บไซต์อีกด้วย

**การติดตั้ง (ถ้าจำเป็น):**
```bash
sudo apt update && sudo apt install -y perl
git clone https://github.com/sullo/nikto
cd nikto/program
chmod +x ./nikto.pl
```

**การใช้งาน:**
```bash
nikto -h inlanefreight.com -Tuning b
```

- `-h`: ระบุ target host
- `-Tuning b`: รันเฉพาะ Software Identification modules

**ผลลัพธ์สำคัญ:**

```
+ Multiple IPs found: 134.209.24.248, 2a03:b0c0:1:e0::32c:b001
+ Target Hostname:    www.inlanefreight.com
+ Server: Apache/2.4.41 (Ubuntu)
+ /index.php?: Uncommon header 'x-redirect-by' found, with contents: WordPress.
+ Apache/2.4.41 appears to be outdated (current is at least 2.4.59)
+ /license.txt: License file found may identify site software.
+ /: A Wordpress installation was found.
+ /wp-login.php: Wordpress login found.
```

## สรุปผลการสอดแนม inlanefreight.com

| หมวดหมู่ | รายละเอียด | ความสำคัญ |
|---------|-----------|-----------|
| **IP Addresses** | IPv4: 134.209.24.248<br>IPv6: 2a03:b0c0:1:e0::32c:b001 | รองรับทั้ง IPv4 และ IPv6 |
| **Server Technology** | Apache/2.4.41 (Ubuntu) | ⚠️ Apache ล้าสมัย (ปัจจุบันอย่างน้อย 2.4.59) |
| **CMS** | WordPress | เป้าหมายที่เป็นไปได้สำหรับช่องโหว่ที่เกี่ยวข้องกับ WordPress |
| **WAF** | Wordfence (Defiant) | มีการป้องกันเพิ่มเติม |
| **WordPress Login** | /wp-login.php | พบหน้าเข้าสู่ระบบ |
| **Information Disclosure** | /license.txt | อาจเปิดเผยรายละเอียดเกี่ยวกับส่วนประกอบซอฟต์แวร์ |
| **Security Headers** | ❌ Missing Strict-Transport-Security<br>❌ X-Content-Type-Options ไม่ได้ตั้งค่า<br>⚠️ x-redirect-by header ที่อาจไม่ปลอดภัย | จุดอ่อนด้านความปลอดภัยหลายจุด |
| **Cookie Security** | ⚠️ wordpress_test_cookie สร้างโดยไม่มี httponly flag | อาจเสี่ยงต่อการโจมตี XSS |

