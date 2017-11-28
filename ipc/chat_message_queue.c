#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

volatile sig_atomic_t has_talking_stick;
char prepend_pid[80];

struct my_msgbuf {
    long mtype;
    char mtext[200];
};

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
    int msqid, ret;
    int pid = getpid();
    key_t key;

    if ((key = ftok("chat_message_queue.c", 'B')) == -1) {
        perror("ftok");
        exit(1);
    }

    if ((msqid = msgget(key, 0644 | IPC_CREAT)) == -1) {
        perror("msgget");
        exit(1);
    }

    printf("msqid: %d\n", msqid);

    // Because messages get stuck in this queue, delete queue then
    // re-make it

    //if ((msqid = msgget(key, 0644 | IPC_CREAT)) == -1) {
        //perror("msgget");
        //exit(1);
    //}

            
    for (;;) {
        printf("pid: %d | \033[1;4mq\033[0muit, \033[1;4mr\033[0mecieve or \033[1;4ms\033[0mend: ", pid);
        char input[20] = "";
        if (fgets(input, sizeof input, stdin) != NULL) {
            // receive
            if (strncmp(input, "r", 1) == 0) {
                do {
                    struct my_msgbuf recv_buf;
                    ret = msgrcv(msqid, 
                                 &recv_buf,
                                 sizeof recv_buf.mtext, 
                                 pid, 
                                 IPC_NOWAIT | MSG_EXCEPT );
                    if (ret == -1 && errno != ENOMSG) {
                        perror("msgrcv");
                        exit(1);
                    } else if (ret == -1 && errno == ENOMSG) {
                        printf("no more messages for us\n");
                    } else {
                        printf("%ld said: %s\n", recv_buf.mtype, recv_buf.mtext);
                    }
                } while (ret != -1);
            // send
            } else if (strncmp(input, "s", 1) == 0) {
                struct my_msgbuf send_buf;
                send_buf.mtype = pid;
                printf("enter message: ");

                if (fgets(send_buf.mtext, sizeof send_buf.mtext, stdin) != NULL) {
                    int len = strlen(send_buf.mtext);

                    if (send_buf.mtext[len-1] == '\n') send_buf.mtext[len-1] = '\0';

                    if (msgsnd(msqid, &send_buf, len+1, 0) == -1)
                        perror("msgsnd");
                }
            } else if (strncmp(input, "d", 1) == 0) {
                printf("deleting the queue and recreating it\n");
                if (msgctl(msqid, IPC_RMID, NULL) == -1) {
                    perror("msgctl");
                    exit(1);
                }
                if ((msqid = msgget(key, 0644 | IPC_CREAT)) == -1) {
                    perror("msgget");
                    exit(1);
                }
             } else if (strncmp(input, "q", 1) == 0) {
                printf("deleting the queue and quiting\n");
                if (msgctl(msqid, IPC_RMID, NULL) == -1) {
                    perror("msgctl");
                    exit(1);
                }
            } else {
                printf("invalid command\n");
            }
        }
    }



    return 0;
}
