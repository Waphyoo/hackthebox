![image](https://github.com/user-attachments/assets/65a31a5d-46d6-45d1-8cd5-471c9c51e2f4)
cat flag is in the open_door()

![image](https://github.com/user-attachments/assets/006bb54f-72c6-4058-87fd-11a35719c698)

access open_door() use Format string attack 
Description
The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.
![image](https://github.com/user-attachments/assets/12771037-f152-45bb-bda6-5732bf091ee6)

use %x to read stack
![image](https://github.com/user-attachments/assets/4d16c883-132f-40c2-b91e-b5b865ca36f0)
found deadbeef we want to access open_door()
todo change local_48 = 0xdeadbee----->local_48 = 0xdead1337
use %n to write integer


