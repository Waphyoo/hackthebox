# Plugins ใน Metasploit

## Plugins คืออะไร?

**Plugins** คือซอฟต์แวร์สำเร็จรูปที่พัฒนาโดยบุคคลที่สาม และได้รับอนุญาตให้รวมเข้ากับ Metasploit Framework โดยมี 2 ประเภท:

1. **ผลิตภัณฑ์เชิงพาณิชย์** - มี Community Edition ให้ใช้ฟรี แต่ฟังก์ชันจำกัด
2. **โปรเจคส่วนบุคคล** - พัฒนาโดยนักพัฒนาอิสระ

---

## ทำไมต้องใช้ Plugins?

### ข้อดีหลัก:

✅ **ทำให้ชีวิต Pentester ง่ายขึ้น** - นำฟังก์ชันของซอฟต์แวร์ที่รู้จักกันดีเข้ามาใน msfconsole  
✅ **ไม่ต้องสลับโปรแกรม** - ไม่ต้อง import/export ข้อมูลไปมา  
✅ **บันทึกอัตโนมัติ** - ทุกอย่างถูกบันทึกใน database โดยอัตโนมัติ  
✅ **ดูข้อมูลได้ทันที** - hosts, services, vulnerabilities แสดงผลพร้อมใช้  
✅ **ทำงานกับ API โดยตรง** - สามารถควบคุม framework ทั้งหมดได้  

### ประโยชน์เพิ่มเติม:

- **Automate งานซ้ำๆ** - ลดเวลาทำงานที่น่าเบื่อ
- **เพิ่มคำสั่งใหม่** - ขยาย msfconsole ให้ทรงพลังขึ้น
- **Extend Framework** - เสริมความสามารถที่มีอยู่แล้ว

---

## การใช้งาน Plugins

### 1. ตรวจสอบ Plugins ที่มีอยู่

**ตำแหน่งเริ่มต้นของ Plugins:**
```bash
ls /usr/share/metasploit-framework/plugins
```

**รายการ Plugins ที่มาพร้อมติดตั้ง:**
```
aggregator.rb       komand.rb          request.rb           sounds.rb
alias.rb            lab.rb             rssfeed.rb           sqlmap.rb
auto_add_route.rb   libnotify.rb       sample.rb            thread.rb
beholder.rb         msfd.rb            session_notifier.rb  token_adduser.rb
db_credcollect.rb   msgrpc.rb          session_tagger.rb    token_hunter.rb
db_tracker.rb       nessus.rb          socket_logger.rb     wiki.rb
event_tester.rb     nexpose.rb         
ffautoregen.rb      openvas.rb
ips_filter.rb       pcap_log.rb
```

### 2. โหลด Plugin

**ตัวอย่าง: โหลด Nessus Plugin**

```
msf6 > load nessus

[*] Nessus Bridge for Metasploit
[*] Type nessus_help for a command listing
[*] Successfully loaded Plugin: Nessus
```

**ดูคำสั่งที่ใช้ได้:**

```
msf6 > nessus_help

Command                     Help Text
-------                     ---------
Generic Commands            
-----------------           
nessus_connect              Connect to a Nessus server
nessus_logout               Logout from the Nessus server
nessus_login                Login into the connected Nessus server
nessus_user_add             Create a new Nessus User
nessus_user_del             Delete a Nessus User
nessus_user_passwd          Change Nessus Users Password

Policy Commands             
-----------------           
nessus_policy_list          List all policies
nessus_policy_del           Delete a policy
```

### 3. กรณี Plugin ไม่พบ

```
msf6 > load Plugin_That_Does_Not_Exist

[-] Failed to load plugin from /usr/share/metasploit-framework/plugins/Plugin_That_Does_Not_Exist.rb: 
cannot load such file
```

**สาเหตุ:** Plugin ไม่ได้ติดตั้งในโฟลเดอร์ที่ถูกต้อง

---

## การติดตั้ง Plugins ใหม่

### วิธีการติดตั้ง:

1. **Plugins ใหม่จาก Parrot OS** - อัพเดทอัตโนมัติตาม distro updates
2. **Custom Plugins** - ดาวน์โหลดไฟล์ `.rb` แล้ววางในโฟลเดอร์ที่เหมาะสม

### ตัวอย่าง: ติดตั้ง DarkOperator's Metasploit-Plugins

**ขั้นตอนที่ 1: Clone Repository**

```bash
git clone https://github.com/darkoperator/Metasploit-Plugins
```

**ขั้นตอนที่ 2: ตรวจสอบไฟล์ที่ดาวน์โหลด**

```bash
ls Metasploit-Plugins

aggregator.rb       ips_filter.rb       pcap_log.rb          sqlmap.rb
alias.rb            komand.rb           pentest.rb           thread.rb
auto_add_route.rb   lab.rb              request.rb           token_adduser.rb
beholder.rb         libnotify.rb        rssfeed.rb           token_hunter.rb
db_credcollect.rb   msfd.rb             sample.rb            twitt.rb
db_tracker.rb       msgrpc.rb           session_notifier.rb  wiki.rb
event_tester.rb     nessus.rb           session_tagger.rb    wmap.rb
ffautoregen.rb      nexpose.rb          socket_logger.rb
growl.rb            openvas.rb          sounds.rb
```

**ขั้นตอนที่ 3: Copy Plugin ไปยังโฟลเดอร์ MSF**

```bash
sudo cp ./Metasploit-Plugins/pentest.rb /usr/share/metasploit-framework/plugins/pentest.rb
```

**ขั้นตอนที่ 4: เริ่ม msfconsole และโหลด Plugin**

```bash
msfconsole -q
```

```
msf6 > load pentest

       ___         _          _     ___ _           _
      | _ \___ _ _| |_ ___ __| |_  | _ \ |_  _ __ _(_)_ _
      |  _/ -_) ' \  _/ -_|_-<  _| |  _/ | || / _` | | ' \ 
      |_| \___|_||_\__\___/__/\__| |_| |_|\_,_\__, |_|_||_|
                                              |___/
      
Version 1.6
Pentest Plugin loaded.
by Carlos Perez (carlos_perez[at]darkoperator.com)
[*] Successfully loaded plugin: pentest
```

**ขั้นตอนที่ 5: ดูคำสั่งใหม่ที่เพิ่มเข้ามา**

```
msf6 > help
```

---

## คำสั่งใหม่จาก Pentest Plugin

### 1. **Tradecraft Commands**
```
check_footprint      Checks the possible footprint of a post module on a target system
```

### 2. **auto_exploit Commands**
```
show_client_side     Show matched client side exploits from data imported from vuln scanners
vuln_exploit         Runs exploits based on data imported from vuln scanners
```

### 3. **Discovery Commands**
```
discover_db                 Run discovery modules against current hosts in the database
network_discover            Performs a port-scan and enumeration of services found
pivot_network_discover      Performs enumeration of networks available to a Meterpreter session
show_session_networks       Enumerate the networks one could pivot thru Meterpreter
```

### 4. **Project Commands**
```
project              Command for managing projects
```

### 5. **Postauto Commands**
```
app_creds            Run application password collection modules against sessions
get_lhost            List local IP addresses that can be used for LHOST
multi_cmd            Run shell command against several sessions
multi_meter_cmd      Run a Meterpreter Console Command against specified sessions
multi_meter_cmd_rc   Run resource file with Meterpreter Console Commands
multi_post           Run a post module against specified sessions
multi_post_rc        Run resource file with post modules and options
sys_creds            Run system password collection modules against sessions
```

---

## รายการ Plugins ยอดนิยม

### ติดตั้งมาพร้อม (Pre-installed):

| Plugin | คำอธิบาย |
|--------|----------|
| **nMap** | Integration กับ Nmap scanner |
| **NexPose** | Vulnerability scanner integration |
| **Nessus** | Vulnerability scanner integration |
| **Mimikatz (V.1)** | Credential extraction tool |
| **Stdapi** | Standard API functions |
| **Incognito** | Token manipulation |

### ติดตั้งเพิ่มเติมได้:

| Plugin | คำอธิบาย |
|--------|----------|
| **Railgun** | Windows API access |
| **Priv** | Privilege escalation |
| **Darkoperator's** | Collection of useful plugins |

---

## Mixins - ความรู้ขั้นสูง

### Mixins คืออะไร?

**Mixins** เป็น feature ของภาษา Ruby ที่ทำให้ Metasploit ยืดหยุ่นมาก:

- เป็น **classes ที่ทำหน้าที่เป็น methods** สำหรับ classes อื่น
- **ไม่ใช่การสืบทอด (inheritance)** แต่เป็นการ **รวมเข้า (inclusion)**
- ใช้คำสั่ง `include` เพื่อเรียกใช้ module

### ใช้ Mixins เมื่อไหร่?

1. **ต้องการ optional features มากมาย** สำหรับ class
2. **ต้องการใช้ feature เดียวกัน** กับหลาย classes

### โครงสร้างการทำงาน:

```ruby
# ตัวอย่างการใช้ Mixin
include ModuleName  # รวม Module เข้ากับ class
```

### หมายเหตุสำหรับผู้เริ่มต้น:

⚠️ **ไม่ต้องกังวล** - ถ้าเพิ่งเริ่มใช้ Metasploit ไม่จำเป็นต้องเข้าใจ Mixins ลึกซึ้งทันที  
💡 **ใช้งานก่อน** - เริ่มจากการใช้ Plugins ที่มีอยู่แล้ว  
📚 **เรียนรู้ภายหลัง** - เมื่อต้องการ customize หรือสร้าง plugins เอง

---

