# Password Managers

## บทนำ
ในปัจจุบันทุกอย่างดูเหมือนต้องใช้รหัสผ่าน ไม่ว่าจะเป็น Wi-Fi บ้าน, โซเชียลมีเดีย, บัญชีธนาคาร, อีเมลธุรกิจ และแอปพลิเคชันต่างๆ ตามการศึกษาของ NordPass พบว่าคนทั่วไปมีรหัสผ่านประมาณ **100 รหัสผ่าน** ซึ่งเป็นเหตุผลหลักที่ทำให้ผู้คนมักใช้รหัสผ่านซ้ำหรือสร้างรหัสผ่านที่ง่ายเกินไป

เราจำเป็นต้องมีรหัสผ่านที่แข็งแรงและไม่ซ้ำกันสำหรับแต่ละบริการ แต่ไม่สมจริงที่จะคาดหวังให้ใครจดจำ credentials ที่ซับซ้อนหลายร้อยตัว นี่คือจุดที่ **Password Manager** มีความสำคัญ

## Password Manager คือ?
Password Manager คือแอปพลิเคชันที่จัดเก็บรหัสผ่านและข้อมูลที่ละเอียดอ่อนใน **encrypted database** อย่างปลอดภัย นอกจากการเก็บข้อมูลที่ปลอดภัยแล้ว ยังมีฟีเจอร์เพิ่มเติม:

- Password generation (สร้างรหัสผ่าน)
- Two-Factor Authentication (2FA) support
- Secure form filling (กรอกฟอร์มอัตโนมัติ)
- Browser integration (ผสานกับ browser)
- Multi-device synchronization (ซิงค์หลายอุปกรณ์)
- Security alerts (แจ้งเตือนความปลอดภัย)

## Password Manager ทำงานอย่างไร?

การทำงานของ password manager แต่ละผู้ให้บริการจะแตกต่างกัน แต่ส่วนใหญ่ใช้ **master password** เพื่อเข้ารหัส password database

การเข้ารหัสและการยืนยันตัวตนอาศัย:
- **Cryptographic hash functions**
- **Key derivation functions**

เพื่อป้องกันการเข้าถึง encrypted database และเนื้อหาภายในโดยไม่ได้รับอนุญาต

---

## Cloud Password Managers

### ข้อพิจารณาหลัก: ความสะดวก
คนทั่วไปมี 3-4 อุปกรณ์และใช้ล็อกอินเว็บไซต์และแอปต่างๆ Cloud-based password manager ช่วยให้ผู้ใช้ซิงค์ encrypted password database ข้างหลายอุปกรณ์

### ฟีเจอร์ที่มักมี:
- Mobile application
- Browser add-on
- ฟีเจอร์อื่นๆ ที่จะกล่าวถึงในหัวข้อถัดไป

### การทำงาน
แต่ละผู้ให้บริการมี technical document อธิบายระบบของตนเอง เช่น:
- Bitwarden
- 1Password
- LastPass

### Zero-Knowledge Encryption
การทำงานทั่วไปคือการสร้าง encryption keys จาก master password ซึ่งรองรับ **Zero-Knowledge Encryption** ที่รับประกันว่าไม่มีใคร แม้แต่ผู้ให้บริการ สามารถเข้าถึงข้อมูลของคุณได้

### ตัวอย่าง: Bitwarden Password Derivation

1. **Master key**: สร้างจาก master password โดยใช้ key derivation function
2. **Master password hash**: สร้างจาก master password (และ master key) เพื่อยืนยันตัวตนผู้ใช้กับ cloud service
3. **Decryption key**: สร้างจาก master key เพื่อทำ symmetric key สำหรับถอดรหัสข้อมูลใน vault

**กระบวนการ:**
- User login → PBKDF2-SHA256 algorithm → Master key derivation → AES-256 bit decryption สำหรับเข้าถึง vault

### Cloud Password Managers ยอดนิยม:
- 1Password
- Bitwarden
- Dashlane
- Keeper
- Lastpass
- NordPass
- RoboForm

---

## Local Password Managers

### แนวคิด
บางบริษัทและบุคคลต้องการจัดการความปลอดภัยด้วยตนเอง โดยไม่พึ่งพา third-party services Local password managers เก็บ password database ในเครื่องและให้ผู้ใช้รับผิดชอบในการปกป้องเนื้อหาและที่เก็บข้อมูล

### Cloud vs. Local
Dashlane เผยแพร่บทความ "Password Manager Storage: Cloud vs. Local" ที่สำรวจข้อดีข้อเสียของแต่ละวิธี ซึ่งระบุว่า **"ในตอนแรกอาจดูเหมือนว่า local storage ปลอดภัยกว่า cloud storage แต่ cybersecurity ไม่ใช่สาขาที่เรียบง่าย"**

### การทำงาน
Local password managers ใช้วิธีการเข้ารหัสคล้ายกับ cloud-based ความแตกต่างที่โดดเด่นคือ:
- **Data transmission และ authentication**
- เน้นการรักษาความปลอดภัย database ที่เก็บใน local system
- ใช้ cryptographic hash functions ต่างๆ
- ใช้ key derivation functions กับ random salt เพื่อป้องกัน precomputed keys และ dictionary/guessing attacks
- มีการป้องกันเพิ่มเติม เช่น memory protection และ keylogger resistance

### Local Password Managers ยอดนิยม:
- KeePass
- KWalletManager
- Pleasant Password Server
- Password Safe

---

## Features (ฟีเจอร์)

### กรณีศึกษา
สมมติเราใช้ Linux, Android และ Chrome OS เราเข้าถึงแอปและเว็บไซต์จากหลายอุปกรณ์และต้องการซิงค์รหัสผ่านและ secure notes ทั้งหมด เราต้องการการป้องกันเพิ่มเติมผ่าน 2FA และงบประมาณ $5 ต่อเดือน

### ฟีเจอร์ทั่วไป:
- **2FA support**
- **Multi-platform** (Android, iOS, Windows, Linux, Mac ฯลฯ)
- **Browser Extension**
- **Login Autocomplete**
- **Import and export capabilities**
- **Password generation**

Wikipedia มีรายการ password managers ทั้งแบบ online และ offline พร้อมความสามารถหลักของแต่ละตัว

---

## Alternatives (ทางเลือกอื่น)

รหัสผ่านเป็นวิธีการยืนยันตัวตนที่พบบ่อยที่สุด แต่ไม่ใช่วิธีเดียว ตลอดโมดูลนี้เราเห็นว่ารหัสผ่านสามารถถูกโจมตีได้หลายวิธี: cracking, guessing, shoulder surfing และอื่นๆ

### แต่ถ้าเราไม่ต้องใช้รหัสผ่านเลยล่ะ?

แม้ว่า OS และแอปส่วนใหญ่จะสร้างบนพื้นฐานของ password-based authentication แต่ administrators สามารถใช้ third-party identity providers หรือแอปพลิเคชันเพื่อเพิ่มการปกป้อง identity

### ทางเลือกทั่วไป:

1. **Multi-factor Authentication (MFA)**
2. **FIDO2** - มาตรฐานการยืนยันตัวตนแบบเปิดที่ใช้อุปกรณ์กายภาพเช่น YubiKey
3. **One-Time Passwords (OTP)**
4. **Time-Based One-Time Passwords (TOTP)**
5. **IP restrictions**
6. **Device compliance enforcement** - เช่น Microsoft Endpoint Manager หรือ Workspace ONE

---

## Going Passwordless (การไปสู่โลกไร้รหัสผ่าน)

### แนวคิด
หลายบริษัท เช่น Microsoft, Auth0, Okta และ Ping Identity กำลังสนับสนุนอนาคตที่ไร้รหัสผ่าน กลยุทธ์นี้มุ่งหมายที่จะลบรหัสผ่านออกจากวิธีการยืนยันตัวตนโดยสิ้นเชิง

### Passwordless Authentication คือ?
เกิดขึ้นเมื่อใช้ authentication factor อื่นที่ไม่ใช่รหัสผ่าน

**ปัญหาของรหัสผ่าน:**
- เป็น **knowledge factor** (สิ่งที่ผู้ใช้รู้)
- เสี่ยงต่อการถูกขโมย
- การแชร์
- การใช้ซ้ำ
- การใช้งานผิด

**Passwordless authentication อาศัย:**
- **Possession factor** (สิ่งที่ผู้ใช้มี) หรือ
- **Inherent factor** (สิ่งที่ผู้ใช้เป็น)

เพื่อยืนยันตัวตนผู้ใช้ด้วยความมั่นใจที่มากขึ้น

### แหล่งข้อมูลเพิ่มเติม:
- Microsoft Passwordless
- Auth0 Passwordless
- Okta Passwordless
- PingIdentity

---

## สรุป

มีตัวเลือกมากมายสำหรับการปกป้องรหัสผ่าน การเลือกวิธีที่เหมาะสมขึ้นอยู่กับความต้องการเฉพาะของบุคคลหรือองค์กร **ทั้งบุคคลและบริษัทมักใช้วิธีการปกป้องรหัสผ่านที่แตกต่างกันสำหรับวัตถุประสงค์ที่แตกต่างกัน**

### ข้อควรพิจารณา:
- **Cloud vs. Local** - ความสะดวกกับความควบคุม
- **Features** - ฟีเจอร์ที่จำเป็นต่อการใช้งาน
- **Security** - ระดับความปลอดภัยที่ต้องการ
- **Future** - การเตรียมพร้อมสำหรับ passwordless authentication

เทคโนโลジีและมาตรฐานใหม่กำลังพัฒนาขึ้น เราจำเป็นต้องศึกษาและเข้าใจรายละเอียดของการนำไปใช้เพื่อตัดสินใจว่าทางเลือกเหล่านั้นจะให้ความปลอดภัยที่เราต้องการสำหรับกระบวนการยืนยันตัวตนหรือไม่