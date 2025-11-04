# Automating Recon (การทำให้การสอดแนมเป็นอัตโนมัติ)

## บทนำ

แม้ว่าการสอดแนมด้วยตนเองจะมีประสิทธิภาพ แต่ก็อาจใช้เวลานานและเสี่ยงต่อข้อผิดพลาดจากมนุษย์ **การทำให้งานสอดแนมเว็บเป็นอัตโนมัติ** สามารถเพิ่มประสิทธิภาพและความแม่นยำอย่างมาก ช่วยให้คุณรวบรวมข้อมูลในระดับใหญ่และระบุช่องโหว่ที่อาจเกิดขึ้นได้เร็วขึ้น

## ทำไมต้องทำให้การสอดแนมเป็นอัตโนมัติ?

### ข้อดีหลักของ Automation:

| ข้อดี | คำอธิบาย | ประโยชน์ |
|------|----------|---------|
| **Efficiency (ประสิทธิภาพ)** | เครื่องมืออัตโนมัติสามารถทำงานซ้ำๆ ได้เร็วกว่ามนุษย์มาก | ประหยัดเวลาอันมีค่าสำหรับการวิเคราะห์และการตัดสินใจ |
| **Scalability (ความสามารถในการขยาย)** | ช่วยให้คุณขยายความพยายามในการสอดแนมไปยังเป้าหมายหรือโดเมนจำนวนมาก | เปิดเผยข้อมูลในขอบเขตที่กว้างขึ้น |
| **Consistency (ความสม่ำเสมอ)** | เครื่องมืออัตโนมัติปฏิบัติตามกฎและขั้นตอนที่กำหนดไว้ล่วงหน้า | ให้ผลลัพธ์ที่สอดคล้องและทำซ้ำได้ ลดความเสี่ยงจากข้อผิดพลาดของมนุษย์ |
| **Comprehensive Coverage (ความครอบคลุม)** | สามารถตั้งโปรแกรมให้ทำงานสอดแนมหลากหลาย | ครอบคลุม DNS enumeration, subdomain discovery, web crawling, port scanning และอื่นๆ |
| **Integration (การบูรณาการ)** | เฟรมเวิร์กหลายตัวรองรับการบูรณาการกับเครื่องมืออื่น | สร้าง workflow ที่ราบรื่นตั้งแต่การสอดแนมไปจนถึงการประเมินช่องโหว่และการใช้ประโยชน์ |

## Reconnaissance Frameworks (เฟรมเวิร์กสำหรับการสอดแนม)

เฟรมเวิร์กเหล่านี้มีจุดมุ่งหมายเพื่อให้ชุดเครื่องมือที่สมบูรณ์สำหรับการสอดแนมเว็บ:

| Framework | คำอธิบาย | ภาษา | คุณสมบัติเด่น |
|-----------|----------|------|---------------|
| **FinalRecon** | เครื่องมือสอดแนมที่ใช้ Python นำเสนอโมดูลต่างๆ สำหรับงานที่แตกต่างกัน | Python | โครงสร้างแบบโมดูลที่ปรับแต่งได้ง่าย, ตรวจสอบ SSL certificate, รวบรวมข้อมูล Whois, วิเคราะห์ header, crawling |
| **Recon-ng** | เฟรมเวิร์กที่ทรงพลังพร้อมโครงสร้างแบบโมดูล | Python | DNS enumeration, subdomain discovery, port scanning, web crawling, exploit ช่องโหว่ที่ทราบ |
| **theHarvester** | ออกแบบมาเพื่อรวบรวมข้อมูลจากแหล่งสาธารณะ | Python | รวบรวม email addresses, subdomains, hosts, ชื่อพนักงาน, open ports, banners จาก search engines, PGP key servers, SHODAN |
| **SpiderFoot** | เครื่องมือ OSINT อัตโนมัติ | Python | บูรณาการกับแหล่งข้อมูลต่างๆ, รวบรวม IP addresses, domain names, email addresses, social media profiles |
| **OSINT Framework** | คอลเลกชันของเครื่องมือและทรัพยากร | Mixed | ครอบคลุมแหล่งข้อมูลหลากหลาย: social media, search engines, public records |

## FinalRecon - รายละเอียดและการใช้งาน

### คุณสมบัติของ FinalRecon:

| โมดูล | คำอธิบาย | ข้อมูลที่ได้รับ |
|-------|----------|----------------|
| **Header Information** | เปิดเผยรายละเอียดเซิร์ฟเวอร์ | เทคโนโลยีที่ใช้, การตั้งค่าความปลอดภัยที่ผิดพลาดที่อาจเกิดขึ้น |
| **Whois Lookup** | เปิดเผยรายละเอียดการจดทะเบียนโดเมน | ข้อมูลผู้จดทะเบียนและรายละเอียดการติดต่อ |
| **SSL Certificate Information** | ตรวจสอบ SSL/TLS certificate | ความถูกต้อง, ผู้ออก และรายละเอียดที่เกี่ยวข้อง |
| **Crawler** | สกัดข้อมูลจาก HTML, CSS, JavaScript | ลิงก์, ทรัพยากร, ช่องโหว่ที่อาจเกิดขึ้น |
| | วิเคราะห์ลิงก์ภายใน/ภายนอก | โครงสร้างเว็บไซต์, การเชื่อมต่อกับโดเมนอื่น |
| | รวบรวมรูปภาพ, robots.txt, sitemap.xml | เส้นทาง crawling ที่อนุญาต/ไม่อนุญาต, โครงสร้างเว็บไซต์ |
| | ค้นหาลิงก์ใน JavaScript, Wayback Machine | ลิงก์ที่ซ่อนอยู่และข้อมูลเว็บไซต์ในอดีต |
| **DNS Enumeration** | สอบถาม DNS record มากกว่า 40 ประเภท | รวมถึง DMARC records สำหรับการประเมินความปลอดภัยอีเมล |
| **Subdomain Enumeration** | ใช้แหล่งข้อมูลหลายแหล่ง | crt.sh, AnubisDB, ThreatMiner, CertSpotter, Facebook API, VirusTotal API, Shodan API, BeVigil API |
| **Directory Enumeration** | รองรับ wordlists และนามสกุลไฟล์ที่กำหนดเอง | ไดเรกทอรีและไฟล์ที่ซ่อนอยู่ |
| **Wayback Machine** | ดึง URLs จากห้าปีที่ผ่านมา | วิเคราะห์การเปลี่ยนแปลงของเว็บไซต์และช่องโหว่ที่อาจเกิดขึ้น |

### การติดตั้ง FinalRecon:

```bash
# 1. Clone repository จาก GitHub
git clone https://github.com/thewhiteh4t/FinalRecon.git

# 2. เข้าไปในไดเรกทอรี
cd FinalRecon

# 3. ติดตั้ง dependencies
pip3 install -r requirements.txt

# 4. เปลี่ยนสิทธิ์ไฟล์ให้ execute ได้
chmod +x ./finalrecon.py

# 5. ตรวจสอบการติดตั้งและดูตัวเลือก
./finalrecon.py --help
```

### ตัวเลือกการใช้งาน FinalRecon:

#### ตัวเลือกหลัก:

| Option | Argument | คำอธิบาย |
|--------|----------|----------|
| `-h, --help` | - | แสดงข้อความช่วยเหลือและออก |
| `--url` | URL | ระบุ URL เป้าหมาย |
| `--headers` | - | ดึงข้อมูล header สำหรับ URL เป้าหมาย |
| `--sslinfo` | - | รับข้อมูล SSL certificate สำหรับ URL เป้าหมาย |
| `--whois` | - | ทำ Whois lookup สำหรับโดเมนเป้าหมาย |
| `--crawl` | - | คลานเว็บไซต์เป้าหมาย |
| `--dns` | - | ทำ DNS enumeration บนโดเมนเป้าหมาย |
| `--sub` | - | แจงนับ subdomains สำหรับโดเมนเป้าหมาย |
| `--dir` | - | ค้นหาไดเรกทอรีบนเว็บไซต์เป้าหมาย |
| `--wayback` | - | ดึง Wayback URLs สำหรับเป้าหมาย |
| `--ps` | - | ทำ port scan แบบเร็วบนเป้าหมาย |
| `--full` | - | ทำการสอดแนมแบบเต็มรูปแบบบนเป้าหมาย |

#### ตัวเลือกเพิ่มเติม:

| Option | Argument | คำอธิบาย | ค่าเริ่มต้น |
|--------|----------|----------|------------|
| `-nb` | - | ซ่อน Banner | - |
| `-dt` | DT | จำนวน threads สำหรับ directory enum | 30 |
| `-pt` | PT | จำนวน threads สำหรับ port scan | 50 |
| `-T` | T | Request Timeout | 30.0 |
| `-w` | W | เส้นทางไปยัง Wordlist | wordlists/dirb_common.txt |
| `-r` | - | อนุญาต Redirect | False |
| `-s` | - | สลับ SSL Verification | True |
| `-sp` | SP | ระบุ SSL Port | 443 |
| `-d` | D | Custom DNS Servers | 1.1.1.1 |
| `-e` | E | File Extensions | txt, xml, php |
| `-o` | O | รูปแบบการ Export | txt |
| `-cd` | CD | เปลี่ยนไดเรกทอรี export | ~/.local/share/finalrecon |
| `-k` | K | เพิ่ม API key | shodan@key |

### ตัวอย่างการใช้งาน:

**คำสั่ง:** รวบรวมข้อมูล header และทำ Whois lookup สำหรับ inlanefreight.com

```bash
./finalrecon.py --headers --whois --url http://inlanefreight.com
```

**ผลลัพธ์:**

```
 ______  __   __   __   ______   __
/\  ___\/\ \ /\ "-.\ \ /\  __ \ /\ \
\ \  __\\ \ \\ \ \-.  \\ \  __ \\ \ \____
 \ \_\   \ \_\\ \_\\"\_\\ \_\ \_\\ \_____\
  \/_/    \/_/ \/_/ \/_/ \/_/\/_/ \/_____/
 ______   ______   ______   ______   __   __
/\  == \ /\  ___\ /\  ___\ /\  __ \ /\ "-.\ \
\ \  __< \ \  __\ \ \ \____\ \ \/\ \\ \ \-.  \
 \ \_\ \_\\ \_____\\ \_____\\ \_____\\ \_\\"\_\
  \/_/ /_/ \/_____/ \/_____/ \/_____/ \/_/ \/_/

[>] Created By   : thewhiteh4t
[>] Version      : 1.1.6

[+] Target : http://inlanefreight.com
[+] IP Address : 134.209.24.248

[!] Headers :
Date : Tue, 11 Jun 2024 10:08:00 GMT
Server : Apache/2.4.41 (Ubuntu)
Link : <https://www.inlanefreight.com/index.php/wp-json/>...
Vary : Accept-Encoding
Content-Encoding : gzip
Content-Length : 5483
Keep-Alive : timeout=5, max=100
Connection : Keep-Alive
Content-Type : text/html; charset=UTF-8

[!] Whois Lookup : 
   Domain Name: INLANEFREIGHT.COM
   Registry Domain ID: 2420436757_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.registrar.amazon.com
   Creation Date: 2019-08-05T22:43:09Z
   Registry Expiry Date: 2024-08-05T22:43:09Z
   Registrar: Amazon Registrar, Inc.
   Domain Status: clientDeleteProhibited
   Domain Status: clientTransferProhibited
   Domain Status: clientUpdateProhibited
   Name Server: NS-1303.AWSDNS-34.ORG
   Name Server: NS-1580.AWSDNS-05.CO.UK
   Name Server: NS-161.AWSDNS-20.COM
   Name Server: NS-671.AWSDNS-19.NET

[+] Completed in 0:00:00.257780
[+] Exported : /home/htb-ac-643601/.local/share/finalrecon/dumps/fr_inlanefreight.com_11-06-2024_11:07:59
```

### การวิเคราะห์ผลลัพธ์:

| ข้อมูลที่ได้ | ความสำคัญ | การนำไปใช้ |
|-------------|----------|------------|
| **IP Address** | 134.209.24.248 | ระบุที่อยู่ IP ของเป้าหมาย |
| **Server** | Apache/2.4.41 (Ubuntu) | เทคโนโลยีและ OS ที่ใช้ - อาจมีช่องโหว่ที่ทราบ |
| **Content-Type** | text/html; charset=UTF-8 | ประเภทของเนื้อหา |
| **Registrar** | Amazon Registrar, Inc. | ผู้ให้บริการจดทะเบียน |
| **Name Servers** | AWS DNS servers | ใช้ AWS infrastructure |
| **Domain Status** | Protected statuses | โดเมนได้รับการป้องกันดี |

