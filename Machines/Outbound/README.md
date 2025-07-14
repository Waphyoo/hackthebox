

![alt text](image.png)


![alt text](image-1.png)


https://github.com/hakaioffsec/CVE-2025-49113-exploit

![alt text](image-2.png)

![alt text](image-3.png)




mysql -u roundcube -p'RCDBPass2025' -h localhost roundcube


![alt text](image-4.png)

www-data@mail:/$ su tyler
รหัสผ่าน: LhKL1o9Nm3X2

![alt text](image-5.png)

![alt text](image-6.png)

![alt text](image-8.png)


tyler@mail:/var/www/html/roundcube/config$ cat config.inc.php.sample 

// This key is used to encrypt the users imap password which is stored

// in the session record. For the default cipher method it must be

// exactly 24 characters long.

// YOUR KEY MUST BE DIFFERENT THAN THE SAMPLE VALUE FOR SECURITY REASONS

$config['des_key'] = 'rcmail-!24ByteDESkey*Str';

![alt text](image-10.png)



https://github.com/roundcube/roundcubemail/blob/master/config/defaults.inc.php



![alt text](image-9.png)

tyler@mail:su jacob

Password: 595mO8DmwGeD


![alt text](image-11.png)

![alt text](image-12.png)

ssh jacob@10.10.11.77

password : : gY4Wr3a1evp4

run linpea as jacob

![alt text](image-17.png)

https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html#writable-files

![alt text](image-19.png)

![alt text](image-18.png)

ใช้ symbolic link อาจจะเท่กว่า ?

![alt text](image-16.png)

