#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>

volatile sig_atomic_t has_talking_stick;
char prepend_pid[80];

void handler_sigusr1(int sig) {
    printf("%sSomeone gave me the talking stick!\n", prepend_pid);

    has_talking_stick = 1;
}

int pass_talking_stick(int pid) {
    if (pid < 1) {
        perror("pass_talking_stick: Invalid PID\n");
        return -1;
    }

    int ret;
    ret = kill(pid, SIGUSR1);
    printf("%sPassed the stick to PID: %d\n", prepend_pid, pid);

    has_talking_stick = 0;
}

int get_pid() {
    printf("%sEnter PID to pass the talking stick to: ", prepend_pid);

    char *input = NULL;
    size_t len;

    getline(&input, &len, stdin);

    int pid = -1;
    if(len > 0) {
	pid = atoi(input);
     } 

    return pid;
}

int main(int argc, char **argv) {
    sprintf(prepend_pid, "\033[34mPID: %d \033[33m|\033[0m ", getpid());

    if (argc > 1) {
        has_talking_stick = 1;
    } else {
        has_talking_stick = 0;
    }

    struct sigaction handler;

    handler.sa_handler = handler_sigusr1;
    handler.sa_flags = 0;
    sigemptyset(&handler.sa_mask);

    if (sigaction(SIGUSR1, &handler, NULL) == -1) {
        perror("sigaction");
        exit(EXIT_SUCCESS);
    }

    for (;;) {
	if (has_talking_stick) {
            int pid = get_pid();
            printf("%sPassing the talking stick to PID %d\n", prepend_pid, pid);
            pass_talking_stick(pid);
        }
        else {
            printf("%sI don't have the stick, waiting.\n", prepend_pid);
            pause();
    	}
    	sleep(3);
    }
    return 0;
}
