#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void secret_function() {
    printf("You found the secret function!\n");
}

void dangerous_function(char *input) {
    char buf[64];
    strcpy(buf, input);
    system("ls");
}

int main() {
    printf("Hello, Bug Bounty World!\n");
    return 0;
}
