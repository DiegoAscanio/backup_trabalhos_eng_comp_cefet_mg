
/* printmsg.c: print a message on the console */

/* printmsg.c: print a message on the console */
#include <stdio.h>
 
int main(int argc, char *argv[]) {
    char *message;
    if (argc != 2) {
        fprintf(stderr, "usage: %s <message>\n",
        argv[0]);
        exit(1);
    }
    message = argv[1];
    if (!printmessage(message)) {
        fprintf(stderr,"%s: couldn't print your message\n",argv[0]);
        exit(1);
    }
    printf("Message Delivered!\n");
    exit(0);
}

int printmessage(char *msg) {
    FILE *f;
    f = fopen("/dev/stdout", "w");
    if (f == (FILE *)NULL) {
        return 0;
    }
    fprintf(f, "%s\n", msg);
    fclose(f);
    return 1;
}
