
![alt text](image-4.png)

/home จะมี flag ซึ่งจะแสดงเมื่อมี role ใน jwt เป็น admin


![alt text](image-3.png)

![alt text](image-5.png)

![alt text](image-2.png)

จะสารถ addAdmin ได้แต่จะต้องอยู่ใน localhost !!!!!!! ก่อน

![alt text](image-6.png)

parameter manualUrl ซึ่งรับจาก user intput 

![alt text](image-1.png)

![alt text](image.png)


parameter manualUrl จะมาถูก get request

![alt text](image-7.png)

ที่อยู่ 127.0.0.1 ที่หมายถึง localhost สามารถเขียนได้หลายแบบ:

**รูปแบบ IP Address:**
- 127.0.0.1 (แบบมาตรฐาน)
- 127.1 (ย่อรูป)
- 127.0.1 (ย่อรูป)
- 0.0.0.0 (ในบางกรณี สำหรับ bind ทุก interface)
- 0 (ย่อสุดๆ แต่อาจใช้ไม่ได้ในทุกระบบ)

port นำมาจาก docker

![alt text](image-8.png)

login อีกครั้งเพื่อรับ jwt ใหม่ที่มี role admin