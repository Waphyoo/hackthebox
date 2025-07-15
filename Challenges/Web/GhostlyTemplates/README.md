

![alt text](image.png)

![alt text](image-1.png)

get html ออกมาเป็น string

defer response.Body.Close() เป็นการมั่นใจว่า HTTP connection จะถูกปิดเสมอ ไม่ว่า function จะจบด้วยวิธีไหน (success, error, panic) เพื่อป้องกัน resource leak

![alt text](image-4.png)



##  Template Injection
ปัญหาหลักคือการใช้ `template.New().Parse()` กับข้อมูลที่อาจมาจากผู้ใช้ (`tmplFile`) โดยไม่ได้ตรวจสอบ ทำให้เกิด **Server-Side Template Injection (SSTI)**

```go
// ช่องโหว่: ถ้า tmplFile มาจาก user input
tmpl, err := template.New("page").Parse(tmplFile)
- `template.New("page")` = สร้าง template object ใหม่ชื่อ "page"
- `.Parse(tmplFile)` = แปลง string ใน `tmplFile` เป็น template
- `tmplFile` คือ string ที่มี template syntax
```

ผู้โจมตีสามารถส่ง template code ที่เป็นอันตราย เช่น:
```go
{{.}} // อ่านข้อมูลทั้งหมดใน reqData
{{range $key, $value := .}} {{$key}}: {{$value}} {{end}} // เปิดเผยข้อมูล

```
![alt text](image-5.png)

![alt text](image-6.png)


```go
err = tmpl.Execute(w, reqData)
```

**สิ่งที่เกิดขึ้น:**
- `tmpl.Execute()` = รัน template และแทนที่ variables
- `w` = HTTP response writer (ส่งไปยัง browser)
- `reqData` = ข้อมูลที่จะใส่ใน template




https://snyk.io/articles/understanding-server-side-template-injection-in-golang/

![alt text](image-3.png)

ngrok http 80

python3 -m http.server 8000

![alt text](image-2.png)


![alt text](image-7.png)