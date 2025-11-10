

# Targets ใน Metasploit

## Targets คืออะไร?

**Targets** คือตัวระบุระบบปฏิบัติการที่เฉพาะเจาะจง ซึ่งนำมาจากเวอร์ชันต่างๆ ของ OS นั้นๆ โดย Targets จะช่วยปรับแต่ง exploit module ให้ทำงานได้กับเวอร์ชันเฉพาะของระบบปฏิบัติการนั้น

---

## การดู Targets

### คำสั่ง `show targets`:

```bash
# ถ้าไม่ได้เลือก exploit module
msf6 > show targets
[-] No exploit module selected.

# ถ้าอยู่ใน exploit module แล้ว
msf6 exploit(windows/smb/ms17_010_psexec) > show targets
```

---

## ตัวอย่าง: Target แบบทั่วไป

### MS17-010 PSExec Exploit:

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > options

Exploit target:
   Id  Name
   --  ----
   0   Automatic
```

**สังเกต:** Exploit นี้มี target เพียง 1 แบบคือ "Automatic" เนื่องจากใช้ได้กับ Windows หลายเวอร์ชัน

---

## ตัวอย่าง: Target แบบเฉพาะเจาะจง

### MS12-063 Internet Explorer execCommand Use-After-Free Vulnerability:

```bash
msf6 exploit(windows/browser/ie_execcommand_uaf) > info
```

### ข้อมูลของ Exploit:

**ชื่อ:** MS12-063 Microsoft Internet Explorer execCommand Use-After-Free Vulnerability  
**แพลตฟอร์ม:** Windows  
**Rank:** Good  
**เปิดเผย:** 2012-09-14

### รายละเอียดช่องโหว่:
- เกิดจากการใช้หน่วยความจำที่ถูกลบไปแล้วซ้ำอีกครั้ง (use-after-free)
- เกิดขึ้นใน CMshtmlEd object
- ช่องโหว่นี้ถูกใช้ในการโจมตีจริงตั้งแต่ 14 ก.ย. 2012

---

## การดูรายการ Targets

```bash
msf6 exploit(windows/browser/ie_execcommand_uaf) > show targets

Exploit targets:
   Id  Name
   --  ----
   0   Automatic
   1   IE 7 on Windows XP SP3
   2   IE 8 on Windows XP SP3
   3   IE 7 on Windows Vista
   4   IE 8 on Windows Vista
   5   IE 8 on Windows 7
   6   IE 9 on Windows 7
```

### สังเกต:
- มี targets หลายแบบตามเวอร์ชัน IE และ Windows
- แต่ละ target มี return address และพารามิเตอร์ที่แตกต่างกัน

---

## การเลือก Target

### **Option 1: Automatic (แนะนำถ้าไม่แน่ใจ)**
```bash
# ปล่อยให้เป็น Automatic
msf6 exploit(windows/browser/ie_execcommand_uaf) > options

Exploit target:
   Id  Name
   --  ----
   0   Automatic
```
- Metasploit จะทำ service detection บนเป้าหมายก่อนโจมตี
- เหมาะกับกรณีที่ไม่แน่ใจเวอร์ชันแน่นอน

### **Option 2: Manual (ถ้ารู้เวอร์ชันแน่นอน)**
```bash
msf6 exploit(windows/browser/ie_execcommand_uaf) > set target 6
target => 6
```
- เลือกเป้าหมายเฉพาะเจาะจงจาก index
- เหมาะกับกรณีที่รู้เวอร์ชัน OS และ browser แน่นอน

---

## ประเภทของ Targets

### Targets อาจแตกต่างกันตาม:

1. **Service Pack**
   - Windows XP SP2 vs SP3
   - ต่างกันที่ patch และ security update

2. **เวอร์ชัน OS**
   - Windows 7 vs Windows Vista vs Windows XP
   - Architecture (x86 vs x64)

3. **เวอร์ชันภาษา**
   - English vs Thai vs Japanese
   - Language pack เปลี่ยน memory addresses

4. **เวอร์ชันซอฟต์แวร์**
   - IE 7 vs IE 8 vs IE 9
   - แต่ละเวอร์ชันมี memory layout ต่างกัน

---

## Return Address คืออะไร?

**Return Address** คือที่อยู่ในหน่วยความจำที่ exploit ต้องการเพื่อควบคุมการทำงานของโปรแกรม

### Return Address อาจแตกต่างกันเพราะ:

✅ **Language Pack** - เปลี่ยน memory addresses  
✅ **Software Version** - เวอร์ชันต่างกัน addresses ต่างกัน  
✅ **Hooks** - การติดตั้ง security software เปลี่ยน addresses  

### ประเภท Return Address:

| ประเภท | คำอธิบาย |
|--------|----------|
| **jmp esp** | กระโดดไปที่ ESP register |
| **pop/pop/ret** | ลำดับคำสั่งเฉพาะเพื่อควบคุม execution flow |
| **Register Jump** | กระโดดไปที่ register เฉพาะ |

---

## การระบุ Target ที่ถูกต้อง

### ขั้นตอนการระบุ Target:

#### **1. รับสำเนาของ Target Binaries**
```bash
# ต้องมีไฟล์ .exe หรือ .dll จากระบบเป้าหมาย
# เพื่อวิเคราะห์หา return address
```

#### **2. ใช้ msfpescan หา Return Address**
```bash
# เครื่องมือใน Metasploit สำหรับค้นหา return address
msfpescan -p <binary_file>
```

#### **3. ศึกษา Exploit Module Code**
```bash
# อ่าน comments ใน source code
# เพื่อเข้าใจว่า target ถูกกำหนดด้วยอะไร
```