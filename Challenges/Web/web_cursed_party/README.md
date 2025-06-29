![alt text](image-4.png)

bot เก็บ flag ใน cookie

![alt text](image-5.png)

จะแสดงหน้า admin.html

![alt text](image-3.png)

halloween_name ใช้ filter | safe ทำให้เกิด XSS

![alt text](image.png)

https://jinja.palletsprojects.com/en/stable/templates/#working-with-automatic-escaping

Auto Escape {{ request.halloween_name }}

![alt text](image-13.png)

{{ request.halloween_name | safe }} จะทำ XSS ได้

Nunjucks และ Jinja2 เป็น template engines ที่มีความคล้ายคลึงกันมาก เนื่องจาก Nunjucks ได้รับแรงบันดาลใจมาจาก Jinja2 

Jinja2 (Python),Nunjucks (JavaScript/Node.js)

![alt text](image-1.png)

มีการใช้ CSP (Content Security Policy) เป็นกลไกความปลอดภัยที่ช่วยป้องกันการโจมตีแบบ XSS (Cross-Site Scripting) และการโจมตีอื่นๆ โดยการควบคุมว่าเว็บไซต์สามารถโหลดทรัพยากรจากแหล่งใดได้บ้าง

https://csp-evaluator.withgoogle.com/

![alt text](image-2.png)

![alt text](image-12.png)

JSDeliver เป็น CDN ฟรีที่ออกแบบมาเพื่อการส่งมอบไฟล์ JavaScript, CSS และไฟล์อื่นๆ โดยเฉพาะสำหรับ open source projects

![alt text](image-6.png)

https://cdn.jsdelivr.net/gh/user/repo@version/file

ใช้ทำ webhook cookie โดยสร้าง JavaScript บน github

![alt text](image-8.png)

![alt text](image-7.png)

![alt text](image-9.png)

![alt text](image-10.png)

![alt text](image-11.png)





