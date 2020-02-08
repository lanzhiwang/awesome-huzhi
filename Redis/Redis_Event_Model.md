## Redis 事件模型

Redis 以其高性能而闻名，它最大限度地利用了`单线程`、`非阻塞`、`多路复用I/O`模型来快速处理请求。



Redis 事件模型示例：



1. 调用 aeCreateEventLoop() 创建事件循环

2. 调用 anetTcpServer() 创建 TCP 服务器
3. 调用 anetNonBlock() 将套接字 fd 设置为非阻塞I/O模型
4. 将套接字 fd 的客户端连接事件的回调函数设置为 acceptProc，当事件循环 el 检测到套接字 fd 的内容发生变化时，也就是有TCP连接时，事件循环将会调用回调函数 acceptProc
5. 在 acceptProc 中接收连接请求
6. 在 acceptProc 中将套接字 fd 有数据可供读取事件的回调函数注册为 readProc，当客户端向服务端传入数据时将会调用回调函数 readProc
7. 在 readProc 中读取客户端发往服务器的数据
8. 在 readProc 中将套接字 fd 有数据可供写入事件的回调函数注册为 writeProc，当服务器准备好发往客户端的数据后，writeProc 将会被调用
9. 在 writeProc 中向客户端发送数据

```c
// echo-server.c
//
#include <stdio.h>
#include <assert.h>
#include <errno.h>
#include "../src/ae.h"
#include "../src/anet.h"

char myerr[ANET_ERR_LEN] = {0};
void acceptProc(struct aeEventLoop *eventLoop, int fd, void *clientdata, int mask);

int main() {/ aeCreateEventLoop
    // 1. 调用 aeCreateEventLoop() 创建事件循环
    aeEventLoop *el = aeCreateEventLoop(1024);
    if(!el){
        return 1;
    }
    // 2. 调用 anetTcpServer() 创建 TCP 服务器
    int fd = anetTcpServer(myerr, 8000, "0.0.0.0", 511);

    if (fd != ANET_ERR) {
        // 3. 调用 anetNonBlock() 将套接字 fd 设置为非阻塞I/O模型
        anetNonBlock(NULL, fd);
        // 4. 将套接字 fd 的客户端连接事件的回调函数设置为 acceptProc
        // 当事件循环 el 检测到套接字 fd 的内容发生变化时，也就是有TCP连接时，
        // 事件循环将会调用回调函数 acceptProc
        if (aeCreateFileEvent(el, fd, AE_READABLE, acceptProc, NULL)) {
            printf("Unrecoverable errror createing server file event");
        }
    } else if (errno == EAFNOSUPPORT) {
        printf("Not listening to IPv4: unsupported");
    }

    printf("Server started at 0.0.0.0:8000! \n");
    aeMain(el);
    aeDeleteEventLoop(el);
    return 0;
}

```



```c
// echo.c
//

#include <string.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <zconf.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include "../src/ae.h"
#include "../src/anet.h"


void unlinkFileEvent(aeEventLoop *loop, int fd) {

    if (fd != -1) {
        aeDeleteFileEvent(loop, fd, AE_READABLE);
        aeDeleteFileEvent(loop, fd, AE_WRITABLE);
        close(fd);
        fd = -1;
    }
}

void writeProc(aeEventLoop *loop, int fd, void *clientdata, int mask)
{

    struct sockaddr_in guest;
    char guest_ip[20];
    int guest_len = sizeof(guest);
    getpeername(fd,(struct sockaddr*)&guest,&guest_len);
    inet_ntop(AF_INET,(void *)&guest.sin_addr, guest_ip,sizeof(guest_ip));
    printf("Sending Client data to %s:%d!\n", guest_ip, guest.sin_port);
    char *buffer = clientdata;

    // 9. 在 writeProc 中向客户端发送数据
    int n_read = anetWrite(fd, buffer, strlen(buffer));
    printf("Size of Sent Data:%d, and the Data is: %s \n", n_read, buffer);

    free(buffer);
    aeDeleteFileEvent(loop, fd, mask);
}


void readProc(struct aeEventLoop *eventLoop, int fd, void *clientdata, int mask) {
    struct sockaddr_in guest;
    char guest_ip[20];
    int guest_len = sizeof(guest);
    getpeername(fd,(struct sockaddr*)&guest,&guest_len);
    inet_ntop(AF_INET,(void *)&guest.sin_addr, guest_ip,sizeof(guest_ip));
    printf("Reading Client data from %s:%d!\n", guest_ip, guest.sin_port);

    int buffer_size = 1024;
    char *buffer = malloc(sizeof(char) * buffer_size);
    bzero(buffer, buffer_size);
    int n_read = 0;
    
    // 7. 在 readProc 中读取客户端发往服务器的数据
    n_read = read(fd, buffer, 1024);


    if (n_read == 0) {
        printf("Server close socket -- \n");
        unlinkFileEvent(eventLoop,fd);
    }

    if (n_read == -1) {
        printf("Socket read error \n");
        if(errno == EAGAIN){
            return;
        } else {
            unlinkFileEvent(eventLoop,fd);
            return;
        }
    }

    printf("Size of Data to be writen:%d, and the Data is: %s \n", n_read, buffer);
    
    // 8. 在 readProc 中将套接字 fd 有数据可供写入事件的回调函数注册为 writeProc
    // 当服务器准备好发往客户端的数据后，writeProc 将会被调用
    aeCreateFileEvent(eventLoop, fd, AE_WRITABLE, writeProc, buffer);
//    write(fd,writebuff,n_read);
}

void acceptProc(struct aeEventLoop *eventLoop, int fd, void *clientdata, int mask) {
    char myerr[ANET_ERR_LEN] = {0};
    printf("Accept new connection in acceptProc.\n");
    char ip[20] = {0};
    int port = 0;
    // 5. 在 acceptProc 中接收连接请求
    int clientfd = anetTcpAccept(myerr, fd, ip, sizeof(ip), &port);

    if (clientfd == AE_ERR) {
        printf("acceptProc error occured!! \n");
        return;
    }

    printf("Client info - ip %s port %d \n", ip, port);


    int ret = anetNonBlock(myerr, clientfd);
    if (ret == ANET_OK) {
        printf("AnetNonBlock running successfully\n\n");
    }
    anetEnableTcpNoDelay(myerr, clientfd);
    // 6. 在 acceptProc 中将套接字 fd 有数据可供读取事件的回调函数注册为 readProc
    // 当客户端向服务端传入数据时将会调用回调函数 readProc
    if(aeCreateFileEvent(eventLoop, clientfd, AE_READABLE, readProc, NULL)==AE_ERR){
        close(fd);
        return;
    }
    write(clientfd,"Hello Client!\n",14);
}

```



总结：

1. Redis 包含一个简单但功能强大的异步事件库 `ae`，该库封装了不同的操作系统的 polling 机制（非阻塞I/O机制）。
2. Linux 操作系统常见的 polling 机制有 select、poll、epoll、kqueue。
3. 以 epoll 机制为例说明。调用 epoll_create() 通知操作系统内核我们要创建 epoll，然后调用 epoll_ctl() 将文件描述符 fd 和所关注的事件类型传递给内核，之后调用 epoll_wait() 等待文件描述符上的事件的发生。当文件描述符被更新时，内核会向应用程序发送通知。应用程序需要做的事情就是为事件创建回调函数。
4. 在 polling 的过程中没有线程和子进程的创建和交互，因此，该模型的关键有点就在于它是一个轻量级的上下文切换的I/O模型，在上下文切换上花费不大。
5. polling 模型最常见的问题就是`延时问题`。在 polling 模型的一个连接中，在一条命令被处理完成前，Redis 不能处理其他的命令。
