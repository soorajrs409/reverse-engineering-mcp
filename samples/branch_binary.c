#include <stdio.h>
#include <unistd.h>

int check(char *s) {
    if (s[0] == 'c' && s[1] == 'a' && s[2] == 't') {
        return 1;
    }
    return 0;
}

int main() {
    char buf[16];
    if (read(0, buf, 16) > 0) {
        if (check(buf)) {
            printf("Success\n");
        } else {
            printf("Fail\n");
        }
    }
    return 0;
}
