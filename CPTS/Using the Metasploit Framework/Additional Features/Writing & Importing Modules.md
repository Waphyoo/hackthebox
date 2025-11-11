# Writing and Importing Modules ใน Metasploit

## การติดตั้ง Module ใหม่

### วิธีที่ 1: อัปเดตทั้งระบบ
```bash
# อัปเดต msfconsole จาก terminal
# จะได้ exploits, auxiliaries และ features ใหม่ล่าสุดทั้งหมด
```

**ข้อดี:** ได้ modules ใหม่ทั้งหมดที่ถูก push เข้า GitHub branch หลัก

**ข้อเสีย:** ต้องอัปเดตทั้งระบบ อาจใช้เวลานาน

---

### วิธีที่ 2: ติดตั้ง Module เฉพาะที่ต้องการ (Manual Installation)

#### ขั้นตอนการค้นหาและติดตั้ง:

## 🔍 การค้นหา Module จาก ExploitDB

**ExploitDB** เป็นแหล่งที่ดีในการหา custom exploit โดยสามารถใช้:
- **Web Interface:** https://www.exploit-db.com/?tag=3
- **CLI Tool:** `searchsploit`

### ตัวอย่างการค้นหา:

#### 1. ค้นหาด้วย `searchsploit`
```bash
searchsploit nagios3
```

**ผลลัพธ์:**
```
Nagios3 - 'history.cgi' Host Command Execution (Metasploit) | linux/remote/24159.rb
Nagios3 - 'history.cgi' Remote Command Execution | multiple/remote/24084.py
Nagios3 - 'statuswml.cgi' 'Ping' Command Execution (Metasploit) | cgi/webapps/16908.rb
Nagios3 - 'statuswml.cgi' Command Injection (Metasploit) | unix/webapps/9861.rb
```

#### 2. กรองเฉพาะไฟล์ `.rb` (Ruby)
```bash
searchsploit -t Nagios3 --exclude=".py"
```

**หมายเหตุ:** ไฟล์ที่ลงท้ายด้วย `.rb` มักเป็น Ruby scripts ที่ออกแบบมาสำหรับ msfconsole

---

## 📂 โครงสร้างไดเรกทอรี Metasploit

### ตำแหน่งไฟล์หลัก:

**1. ไดเรกทอรีหลัก:**
```bash
/usr/share/metasploit-framework/
```

**โครงสร้างภายใน:**
```bash
ls /usr/share/metasploit-framework/

app     db        Gemfile.lock   modules     msfdb      msfrpcd    plugins
config  documentation  lib     msfconsole  msfrpc     msfupdate  scripts
data    Gemfile   metasploit-framework.gemspec  msfd  tools
```

**2. โฟลเดอร์ใน Home Directory:**
```bash
~/.msf4/
```

**โครงสร้าง:**
```bash
ls .msf4/

history  local  logos  logs  loot  modules  plugins  store
```

---

## 📥 การติดตั้ง Module แบบ Manual

### ขั้นตอนการติดตั้ง:

#### 1. **ดาวน์โหลดไฟล์ `.rb`**
```bash
# ตัวอย่าง: ดาวน์โหลด exploit สำหรับ Nagios3
# ไฟล์: 9861.rb
```

#### 2. **คัดลอกไฟล์ไปยังไดเรกทอรีที่เหมาะสม**
```bash
cp ~/Downloads/9861.rb /usr/share/metasploit-framework/modules/exploits/unix/webapp/nagios3_command_injection.rb
```

#### 3. **โหลด Module ใน msfconsole**

**วิธีที่ 1: โหลดตอน start msfconsole**
```bash
msfconsole -m /usr/share/metasploit-framework/modules/
```

**วิธีที่ 2: ใช้คำสั่ง `loadpath`**
```bash
msf6> loadpath /usr/share/metasploit-framework/modules/
```

**วิธีที่ 3: ใช้คำสั่ง `reload_all`**
```bash
msf6> reload_all
```

#### 4. **ใช้งาน Module**
```bash
msf6> use exploit/unix/webapp/nagios3_command_injection
msf6 exploit(unix/webapp/nagios3_command_injection)> show options
```

---

## ⚠️ กฎการตั้งชื่อ Module (Naming Conventions)

**CRITICAL:** ต้องใช้ naming convention ที่ถูกต้อง มิฉะนั้นจะเกิด error

### ✅ รูปแบบที่ถูกต้อง:
- ใช้ **snake_case** (ขีดล่างคั่น)
- ใช้ตัวอักษร **alphanumeric** เท่านั้น
- ใช้ **underscores** (`_`) ไม่ใช่ **dashes** (`-`)

**ตัวอย่างที่ถูกต้อง:**
```
nagios3_command_injection.rb
our_module_here.rb
bludit_auth_bruteforce_mitigation_bypass.rb
```

**ตัวอย่างที่ผิด:**
```
nagios3-command-injection.rb  ❌
Nagios3CommandInjection.rb     ❌
nagios3 command injection.rb   ❌
```

---

## 🔧 การ Port Script เป็น Metasploit Module

### ขั้นตอนการ Port:

#### 1. **เลือก Script ที่จะ Port**
ตัวอย่าง: **Bludit 3.9.2 - Authentication Bruteforce Mitigation Bypass**
- ไฟล์: `48746.rb`

#### 2. **หา Boilerplate Code**
```bash
# ค้นหา module ที่มีอยู่แล้วในหมวดเดียวกัน
ls /usr/share/metasploit-framework/modules/exploits/linux/http/ | grep bludit

# ผลลัพธ์:
bludit_upload_images_exec.rb
```

#### 3. **คัดลอกและเตรียมไฟล์**
```bash
cp ~/Downloads/48746.rb /usr/share/metasploit-framework/modules/exploits/linux/http/bludit_auth_bruteforce_mitigation_bypass.rb
```

---

## 📝 โครงสร้าง Metasploit Module

### ส่วนประกอบหลัก:

#### 1. **Include Statements (Mixins)**
```ruby
class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking

  include Msf::Exploit::Remote::HttpClient
  include Msf::Exploit::PhpEXE
  include Msf::Exploit::FileDropper
  include Msf::Auxiliary::Report
```

**คำอธิบาย Mixins:**

| Function | คำอธิบาย |
|----------|----------|
| `Msf::Exploit::Remote::HttpClient` | มี methods สำหรับทำงานเป็น HTTP client เมื่อ exploit HTTP server |
| `Msf::Exploit::PhpEXE` | สร้าง first-stage PHP payload |
| `Msf::Exploit::FileDropper` | จัดการการถ่ายโอนไฟล์และทำความสะอาดหลังสร้าง session |
| `Msf::Auxiliary::Report` | มี methods สำหรับรายงานข้อมูลไปยัง MSF Database |

---

#### 2. **Module Information**
```ruby
def initialize(info={})
  super(update_info(info,
    'Name'           => "Bludit 3.9.2 - Authentication Bruteforce Mitigation Bypass",
    'Description'    => %q{
      คำอธิบายช่องโหว่และวิธีการ exploit
    },
    'License'        => MSF_LICENSE,
    'Author'         =>
      [
        'rastating',  # ผู้ค้นพบ
        '0ne-nine9'   # ผู้เขียน Metasploit module
      ],
    'References'     =>
      [
        ['CVE', '2019-17240'],
        ['URL', 'https://...'],
        ['PATCH', 'https://github.com/...']
      ],
    'Platform'       => 'php',
    'Arch'           => ARCH_PHP,
    'Notes'          =>
      {
        'SideEffects' => [ IOC_IN_LOGS ],
        'Reliability' => [ REPEATABLE_SESSION ],
        'Stability'   => [ CRASH_SAFE ]
      },
    'Targets'        =>
      [
        [ 'Bludit v3.9.2', {} ]
      ],
    'Privileged'     => false,
    'DisclosureDate' => "2019-10-05",
    'DefaultTarget'  => 0))
```

---

#### 3. **Module Options**
```ruby
register_options(
  [
    OptString.new('TARGETURI', [true, 'The base path for Bludit', '/']),
    OptString.new('BLUDITUSER', [true, 'The username for Bludit']),
    OptPath.new('PASSWORDS', [ true, 'The list of passwords',
      File.join(Msf::Config.data_directory, "wordlists", "passwords.txt") ])
  ])
end
```

**ประเภท Options ที่ใช้บ่อย:**
- `OptString.new()` - รับค่า string
- `OptPath.new()` - รับค่า file path
- `OptInt.new()` - รับค่าตัวเลข
- `OptBool.new()` - รับค่า true/false

---

#### 4. **Exploit Code**
```ruby
# โค้ดสำหรับการ exploit จริง
# ใส่ฟังก์ชันและ logic การโจมตีที่นี่
```

---

## 📚 แหล่งข้อมูลสำหรับการเขียน Module

### เอกสารและแหล่งเรียนรู้:

1. **Metasploit Documentation**
   - https://docs.metasploit.com
   - ค้นหา mixins, classes, และ methods ที่ต้องการ

2. **GitHub Repository**
   - https://github.com/rapid7/metasploit-framework
   - ดูตัวอย่าง modules ที่มีอยู่แล้ว

3. **หนังสือแนะนำ**
   - "Metasploit: A Penetration Tester's Guide" (No Starch Press)
   - มีเนื้อหาเชิงลึกเกี่ยวกับการ port scripts

4. **Rapid7 Blog Posts**
   - https://blog.rapid7.com
   - บทความเกี่ยวกับการพัฒนา modules

---

