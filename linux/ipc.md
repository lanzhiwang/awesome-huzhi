## 进程间通信（IPC）

进程间通信（IPC，InterProcess Communication）是指在不同进程之间传播或交换信息。IPC的方式通常有`管道（包括无名管道和命名管道）`、`消息队列`、`信号量`、`共享内存`、`Socket`、`Streams`等。其中 Socket 和 Streams 支持不同主机上的两个进程IPC。

### 管道

管道，通常指无名管道，是 UNIX 系统IPC最古老的形式。

#### 特点

* 它是半双工的（即数据只能在一个方向上流动），具有固定的读端和写端。

* 它只能用于具有亲缘关系的进程之间的通信（也是父子进程或者兄弟进程之间）。

* 它可以看成是一种特殊的文件，对于它的读写也可以使用普通的read、write 等函数。但是它不是普通的文件，并不属于其他任何文件系统，并且只存在于内存中。

#### 原型

```c
#include <unistd.h>
int pipe(int fd[2]);  // 返回值：若成功返回0，失败返回-1
```

当一个管道建立时，它会创建两个文件描述符：fd[0]为读而打开，fd[1]为写而打开。

要关闭管道只需将这两个文件描述符关闭即可。

#### 例子

单个进程中的管道几乎没有任何用处。所以，通常调用 pipe 的进程接着调用 fork，这样就创建了父进程与子进程之间的 IPC 通道。

若要数据流从父进程流向子进程，则关闭父进程的读端（fd[0]）与子进程的写端（fd[1]）；反之，则可以使数据流从子进程流向父进程。

```c
#include<stdio.h>
#include<unistd.h>
int main()
{
  int fd[2];  // 两个文件描述符
  pid_t pid;
  char buff[20];
  
  if(pipe(fd) < 0) // 创建管道
  {
    printf("Create Pipe Error!\n");
  }
  
  if((pid = fork()) < 0)  // 创建子进程
  {
    printf("Fork Error!\n");
  }
  else if(pid > 0)  // 父进程
  {
    close(fd[0]); // 关闭读端
    write(fd[1], "hello world\n", 12);
  }
  else
  {
    close(fd[1]); // 关闭写端
    read(fd[0], buff, 20);
    printf("%s", buff);
  }
  return 0;
}

```

### FIFO

FIFO，也称为命名管道，它是一种文件类型。

#### 特点

* FIFO可以在无关的进程之间交换数据，与无名管道不同。

* FIFO有路径名与之相关联，它以一种特殊设备文件形式存在于文件系统中。

#### 原型

```c
#include <sys/stat.h>
int mkfifo(const char *pathname, mode_t mode); // 返回值：成功返回0，出错返回-1
```

其中的 mode 参数与open函数中的 mode 相同。一旦创建了一个 FIFO，就可以用一般的文件I/O函数操作它。

当 open 一个FIFO时，是否设置非阻塞标志（O_NONBLOCK）的区别：

* 若没有指定O_NONBLOCK（默认），只读 open 要阻塞到某个其他进程为写而打开此 FIFO。类似的，只写 open 要阻塞到某个其他进程为读而打开它。

* 若指定了O_NONBLOCK，则只读 open 立即返回。而只写 open 将出错返回 -1 如果没有进程已经为读而打开该 FIFO，其errno置ENXIO。

#### 例子

FIFO的通信方式类似于在进程中使用文件来传输数据，只不过FIFO类型文件同时具有管道的特性。在数据读出时，FIFO管道中同时清除数据，并且“先进先出”。

**write_fifo.c**

```c
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<time.h>

int main()
{
  int fd;
  int n, i;
  char buf[1024];
  time_t tp;
  
  printf("I am %d process.\n", getpid());  // 说明进程ID
  
  if((fd = open("fifo1", O_WRONLY)) < 0)  // 以写模式打开一个FIFO
  {
    perror("Open FIFO Failed");
    exit(1);
  }
  
  for(i=0; i<10; ++i)
  {
    time(&tp);  // 获取系统当前时间
    n=sprintf(buf,"Process %d's time is %s", getpid(), ctime(&tp));
    printf("Send message: %s", buf);  // 打印
    if(write(fd, buf, n+1) < 0)  // 写入到FIFO中
    {
      perror("Write FIFO Failed");
      close(fd);
      exit(1);
    }
    sleep(1);  // 休眠1秒
  }
  
  close(fd);  // 关闭FIFO文件
  return 0;
}
```

**read_fifo.c**

```c
#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<fcntl.h>
#include<sys/stat.h>

int main()
{
  int fd;
  int len;
  char buf[1024];
  
  if(mkfifo("fifo1", 0666) < 0 && errno!=EEXIST)  // 创建FIFO管道
  {
    perror("Create FIFO Failed");
  }
  
  if((fd = open("fifo1", O_RDONLY)) < 0)  // 以读模式打开FIFO
  {
    perror("Open FIFO Failed");
    exit(1);
  }
  
  while((len = read(fd, buf, 1024)) > 0)  // 读取FIFO管道
  {
    printf("Read message: %s", buf);
  }
  
  close(fd);  // 关闭FIFO文件
  return 0;
}
```

在两个终端里用 gcc 分别编译运行上面两个文件，可以看到输出结果如下：

```bash
$ ./write_fifo
I am 5954 process.
Send message: Process 5954's time is Mon Apr 20 12:37:28 2015
Send message: Process 5954's time is Mon Apr 20 12:37:29 2015
Send message: Process 5954's time is Mon Apr 20 12:37:30 2015
Send message: Process 5954's time is Mon Apr 20 12:37:31 2015
Send message: Process 5954's time is Mon Apr 20 12:37:32 2015
Send message: Process 5954's time is Mon Apr 20 12:37:33 2015
Send message: Process 5954's time is Mon Apr 20 12:37:34 2015
Send message: Process 5954's time is Mon Apr 20 12:37:35 2015
Send message: Process 5954's time is Mon Apr 20 12:37:36 2015
Send message: Process 5954's time is Mon Apr 20 12:37:37 2015
```

```bash
$ ./read_fifo
Read message: Process 5954's time is Mon Apr 20 12:37:28 2015
Read message: Process 5954's time is Mon Apr 20 12:37:29 2015
Read message: Process 5954's time is Mon Apr 20 12:37:30 2015
Read message: Process 5954's time is Mon Apr 20 12:37:31 2015
Read message: Process 5954's time is Mon Apr 20 12:37:32 2015
Read message: Process 5954's time is Mon Apr 20 12:37:33 2015
Read message: Process 5954's time is Mon Apr 20 12:37:34 2015
Read message: Process 5954's time is Mon Apr 20 12:37:35 2015
Read message: Process 5954's time is Mon Apr 20 12:37:36 2015
Read message: Process 5954's time is Mon Apr 20 12:37:37 2015
```

上述例子可以扩展成 客户进程—服务器进程 通信的实例，write_fifo的作用类似于客户端，可以打开多个客户端向一个服务器发送请求信息，read_fifo类似于服务器，它适时监控着FIFO的读端，当有数据时，读出并进行处理，但是有一个关键的问题是，每一个客户端必须预先知道服务器提供的FIFO接口。


### 消息队列

消息队列，是消息的链接表，存放在内核中。一个消息队列由一个标识符（即队列ID）来标识。

#### 特点
* 消息队列是面向记录的，其中的消息具有特定的格式以及特定的优先级。

* 消息队列独立于发送与接收进程。进程终止时，消息队列及其内容并不会被删除。

* 消息队列可以实现消息的随机查询,消息不一定要以先进先出的次序读取,也可以按消息的类型读取。

#### 原型

```c
#include <sys/msg.h>

// 创建或打开消息队列：成功返回队列ID，失败返回-1
int msgget(key_t key, int flag);

// 添加消息：成功返回0，失败返回-1
int msgsnd(int msqid, const void *ptr, size_t size, int flag);

// 读取消息：成功返回消息数据的长度，失败返回-1
int msgrcv(int msqid, void *ptr, size_t size, long type, int flag);

// 控制消息队列：成功返回0，失败返回-1
int msgctl(int msqid, int cmd, struct msqid_ds *buf);
```

在以下两种情况下，msgget 将创建一个新的消息队列：

* 如果没有与键值key相对应的消息队列，并且flag中包含了IPC_CREAT标志位。

* key参数为IPC_PRIVATE。

函数 msgrcv 在读取消息队列时，type参数有下面几种情况：

* type == 0，返回队列中的第一个消息；
* 
* type > 0，返回队列中消息类型为 type 的第一个消息；
* 
* type < 0，返回队列中消息类型值小于或等于 type 绝对值的消息，如果有多个，则取类型值最小的消息。
* 
可以看出，type值非 0 时用于以非先进先出次序读消息。也可以把 type 看做优先级的权值。

#### 例子
下面写了一个简单的使用消息队列进行IPC的例子，服务端程序一直在等待特定类型的消息，当收到该类型的消息以后，发送另一种特定类型的消息作为反馈，客户端读取该反馈并打印出来。

**msg_server.c**

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/msg.h>

// 用于创建一个唯一的key
#define MSG_FILE "/etc/passwd"

// 消息结构
struct msg_form {
  long mtype;
  char mtext[256];
};

int main()
{
  int msqid;
  key_t key;
  struct msg_form msg;

  // 获取key值
  if((key = ftok(MSG_FILE,'z')) < 0)
  {
    perror("ftok error");
    exit(1);
  }
  // 打印key值
  printf("Message Queue - Server key is: %d.\n", key);
  
  // 创建消息队列
  if ((msqid = msgget(key, IPC_CREAT|0777)) == -1)
  {
    perror("msgget error");
    exit(1);
  }
  // 打印消息队列ID及进程ID
  printf("My msqid is: %d.\n", msqid);
  printf("My pid is: %d.\n", getpid());
  
  // 循环读取消息
  for(;;)
  {
    // int msgrcv(int msqid, void *ptr, size_t size, long type, int flag);
    // 返回类型为888的第一个消息
    msgrcv(msqid, &msg, 256, 888, 0);
    printf("Server: receive msg.mtext is: %s.\n", msg.mtext);
    printf("Server: receive msg.mtype is: %d.\n", msg.mtype);
    
    // int msgsnd(int msqid, const void *ptr, size_t size, int flag);
    msg.mtype = 999; // 客户端接收的消息类型
    sprintf(msg.mtext, "hello, I'm server %d", getpid());
    msgsnd(msqid, &msg, sizeof(msg.mtext), 0);
  }
  return 0;
}
```

**msg_client.c**

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/msg.h>

// 用于创建一个唯一的key
#define MSG_FILE "/etc/passwd"

// 消息结构
struct msg_form {
  long mtype;
  char mtext[256];
};

int main()
{
  int msqid;
  key_t key;
  struct msg_form msg;
  
  // 获取key值
  if ((key = ftok(MSG_FILE, 'z')) < 0)
  {
    perror("ftok error");
    exit(1);
  }
  // 打印key值
  printf("Message Queue - Client key is: %d.\n", key);
  
  // 打开消息队列
  if ((msqid = msgget(key, IPC_CREAT|0777)) == -1)
  {
    perror("msgget error");
    exit(1);
  }
  // 打印消息队列ID及进程ID
  printf("My msqid is: %d.\n", msqid);
  printf("My pid is: %d.\n", getpid());
  
  // int msgsnd(int msqid, const void *ptr, size_t size, int flag);
  // 添加消息，类型为888
  msg.mtype = 888;
  sprintf(msg.mtext, "hello, I'm client %d", getpid());
  msgsnd(msqid, &msg, sizeof(msg.mtext), 0);
  
  // int msgrcv(int msqid, void *ptr, size_t size, long type, int flag);
  // 读取类型为999的消息
  msgrcv(msqid, &msg, 256, 999, 0);
  printf("Client: receive msg.mtext is: %s.\n", msg.mtext);
  printf("Client: receive msg.mtype is: %d.\n", msg.mtype);
  
  return 0;
}
```

### 信号量

信号量（semaphore）与已经介绍过的 IPC 结构不同，它是一个计数器。信号量用于实现进程间的`互斥`与`同步`，而不是用于存储进程间通信数据。

#### 特点

* 信号量用于进程间同步，若要在进程间传递数据需要结合共享内存。

* 信号量基于操作系统的 PV 操作，程序对信号量的操作都是原子操作。

* 每次对信号量的 PV 操作不仅限于对信号量值加 1 或减 1，而且可以加减任意正整数。
支持信号量组。

#### 原型

最简单的信号量是只能取 0 和 1 的变量，这也是信号量最常见的一种形式，叫做`二值信号量`（Binary Semaphore）。而可以取多个正整数的信号量被称为`通用信号量`。

Linux 下的信号量函数都是在通用的信号量数组上进行操作，而不是在一个单一的二值信号量上进行操作。

```c
#include <sys/sem.h>

// 创建或获取一个信号量组：若成功返回信号量集ID，失败返回-1
int semget(key_t key, int num_sems, int sem_flags);

// 对信号量组进行操作，改变信号量的值：成功返回0，失败返回-1
int semop(int semid, struct sembuf semoparray[], size_t numops);

// 控制信号量的相关信息
int semctl(int semid, int sem_num, int cmd, ...);
```

当 semget 创建新的信号量集合时，必须指定集合中信号量的个数（即num_sems），通常为1； 如果是引用一个现有的集合，则将num_sems指定为 0 。

在 semop 函数中，sembuf 结构的定义如下：

```c
struct sembuf
{
  short sem_num;  // 信号量组中对应的序号，0～sem_nums-1
  short sem_op;  // 信号量值在一次操作中的改变量
  short sem_flg;  // IPC_NOWAIT, SEM_UNDO
}
```

其中 sem_op 是一次操作中的信号量的改变量：

* 若sem_op > 0，表示进程释放相应的资源数，将 sem_op 的值加到信号量的值上。如果有进程正在休眠等待此信号量，则换行它们。

* 若sem_op < 0，请求 sem_op 的绝对值的资源。

* 若sem_op == 0，进程阻塞直到信号量的相应值为0

在 semctl 函数中的命令有多种，这里就说两个常用的：

* SETVAL：用于初始化信号量为一个已知的值。所需要的值作为联合semun的val成员来传递。在信号量第一次使用之前需要设置信号量。

* IPC_RMID：删除一个信号量集合。如果不删除信号量，它将继续在系统中存在，即使程序已经退出，它可能在你下次运行此程序时引发问题，而且信号量是一种有限的资源。

#### 例子

```c
#include<stdio.h>
#include<stdlib.h>
#include<sys/sem.h>

// 联合体，用于semctl初始化
union semun
{
  int val; // for SETVAL
  struct semid_ds *buf;
  unsigned short  *array;
};

// 初始化信号量
int init_sem(int sem_id, int value)
{
  union semun tmp;
  tmp.val = value;
  // int semctl(int semid, int sem_num, int cmd, ...);
  if(semctl(sem_id, 0, SETVAL, tmp) == -1)
  {
    perror("Init Semaphore Error");
    return -1;
  }
  return 0;
}

/*
 * P操作:
 * 若信号量值为1，获取资源并将信号量值减一
 * 若信号量值为0，进程挂起等待
 */
int sem_p(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  // 序号
  sbuf.sem_op = -1;  // P操作
  sbuf.sem_flg = SEM_UNDO;
  
  // int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("P operation Error");
    return -1;
  }
  return 0;
}

/*
 * V操作：
 * 释放资源并将信号量值加一
 * 如果有进程正在挂起等待，则唤醒它们
 */
int sem_v(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  // 序号
  sbuf.sem_op = 1;  // V操作
  sbuf.sem_flg = SEM_UNDO;
  
  // int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("V operation Error");
    return -1;
  }
  return 0;
}

// 删除信号量集
int del_sem(int sem_id)
{
  union semun tmp;
  if(semctl(sem_id, 0, IPC_RMID, tmp) == -1)
  {
    perror("Delete Semaphore Error");
    return -1;
  }
  return 0;
}

int main()
{
  int sem_id;  // 信号量集ID
  key_t key;
  pid_t pid;
  
  // 获取key值
  if((key = ftok(".", 'z')) < 0)
  {
    perror("ftok error");
    exit(1);
  }
  
  // int semget(key_t key, int num_sems, int sem_flags);
  // 创建信号量集，其中只有一个信号量
  if((sem_id = semget(key, 1, IPC_CREAT|0666)) == -1)
  {
    perror("semget error");
    exit(1);
  }
  
  // 初始化：初值设为0资源被占用
  init_sem(sem_id, 0);
  
  if((pid = fork()) == -1)
  {
    perror("Fork Error");
  }
  else if(pid == 0)  // 子进程
  {
    sleep(2);
    printf("Process child: pid=%d\n", getpid());
    sem_v(sem_id); // 释放资源，加一操作
  }
  else  // 父进程
  {
    sem_p(sem_id);  // 等待资源，减一操作
    printf("Process father: pid=%d\n", getpid());
    sem_v(sem_id);  // 释放资源，加一操作
    del_sem(sem_id);  // 删除信号量集
  }
  return 0;
}

```
上面的例子如果不加信号量，则父进程会先执行完毕。这里加了信号量让父进程等待子进程执行完以后再执行。


### 共享内存

共享内存（Shared Memory），指两个或多个进程共享一个给定的存储区。

#### 特点

* 共享内存是最快的一种 IPC，因为进程是直接对内存进行存取。

* 因为多个进程可以同时操作，所以需要进行同步。

* 信号量+共享内存通常结合在一起使用，信号量用来同步对共享内存的访问。

#### 原型

```c
#include <sys/shm.h>

// 创建或获取一个共享内存：成功返回共享内存ID，失败返回-1
int shmget(key_t key, size_t size, int flag);

// 连接共享内存到当前进程的地址空间：成功返回指向共享内存的指针，失败返回-1
void *shmat(int shm_id, const void *addr, int flag);

// 断开与共享内存的连接：成功返回0，失败返回-1
int shmdt(void *addr);

// 控制共享内存的相关信息：成功返回0，失败返回-1
int shmctl(int shm_id, int cmd, struct shmid_ds *buf);
```

当用 shmget 函数创建一段共享内存时，必须指定其 size；而如果引用一个已存在的共享内存，则将 size 指定为0 。

当一段共享内存被创建以后，它并不能被任何进程访问。必须使用 shmat 函数连接该共享内存到当前进程的地址空间，连接成功后把共享内存区对象映射到调用进程的地址空间，随后可像本地空间一样访问。

shmdt 函数是用来断开 shmat 建立的连接的。注意，这并不是从系统中删除该共享内存，只是当前进程不能再访问该共享内存而已。

shmctl 函数可以对共享内存执行多种操作，根据参数 cmd 执行相应的操作。常用的是IPC_RMID（从系统中删除该共享内存）。

#### 例子

下面这个例子，使用了**共享内存+信号量+消息队列**的组合来实现服务器进程与客户进程间的通信。

* 共享内存用来传递数据；
* 信号量用来同步；
* 消息队列用来在客户端修改了共享内存后通知服务器读取。

**Server.c**

```c
#include<stdio.h>
#include<stdlib.h>
#include<sys/shm.h>  //shared memory
#include<sys/sem.h>  //semaphore
#include<sys/msg.h>  //message queue
#include<string.h>  //memcpy

//消息队列结构
struct msg_form {
  long mtype;
  char mtext[256];
};

//联合体，用于semctl初始化
union semun
{
  int val;  //for SETVAL
  struct semid_ds *buf;
  unsigned short  *array;
};

//初始化信号量
int init_sem(int sem_id, int value)
{
  union semun tmp;
  tmp.val = value;
  //int semctl(int semid, int sem_num, int cmd, ...);
  if(semctl(sem_id, 0, SETVAL, tmp) == -1)
  {
    perror("Init Semaphore Error");
    return -1;
  }
  return 0;
}

/*
 * P操作:
 * 若信号量值为1，获取资源并将信号量值减一
 * 若信号量值为0，进程挂起等待
 */
int sem_p(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  //序号
  sbuf.sem_op = -1;  //P操作
  sbuf.sem_flg = SEM_UNDO;
  
  //int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("P operation Error");
    return -1;
  }
  return 0;
}

/*
 * V操作：
 * 释放资源并将信号量值加一
 * 如果有进程正在挂起等待，则唤醒它们
 */
int sem_v(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  //序号
  sbuf.sem_op = 1;  //V操作
  sbuf.sem_flg = SEM_UNDO;
  
  //int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("V operation Error");
    return -1;
  }
  return 0;
}

//删除信号量集
int del_sem(int sem_id)
{
  union semun tmp;
  if(semctl(sem_id, 0, IPC_RMID, tmp) == -1)
  {
    perror("Delete Semaphore Error");
    return -1;
  }
  return 0;
}

//创建一个信号量集
int creat_sem(key_t key)
{
  int sem_id;
  if((sem_id = semget(key, 1, IPC_CREAT|0666)) == -1)
  {
    perror("semget error");
    exit(-1);
  }
  init_sem(sem_id, 1);  //初值设为1资源未占用
  return sem_id;
}

int main()
{
  key_t key;
  int shmid;  //共享内存ID
  int semid;  //信号量ID
  int msqid;  //消息队列ID
  char *shm;  //共享内存地址
  char data[] = "this is server";
  struct shmid_ds buf1;  //用于删除共享内存
  struct msqid_ds buf2;  //用于删除消息队列
  struct msg_form msg;  //消息队列用于通知对方更新了共享内存
  
  //获取key值
  if((key = ftok(".", 'z')) < 0)
  {
    perror("ftok error");
    exit(1);
  }
  
  //int shmget(key_t key, size_t size, int flag);
  // 创建共享内存
  if((shmid = shmget(key, 1024, IPC_CREAT|0666)) == -1)
  {
    perror("Create Shared Memory Error");
    exit(1);
  }
  
  //void *shmat(int shm_id, const void *addr, int flag);
  // 连接共享内存
  shm = (char*)shmat(shmid, 0, 0);
  if((int)shm == -1)
  {
    perror("Attach Shared Memory Error");
    exit(1);
  }
  
  // 创建消息队列
  if ((msqid = msgget(key, IPC_CREAT|0777)) == -1)
  {
    perror("msgget error");
    exit(1);
  }
  
  // 创建信号量
  semid = creat_sem(key);
  
  // 读数据
  while(1)
  {
    msgrcv(msqid, &msg, 1, 888, 0);  //读取类型为888的消息
    if(msg.mtext == 'q')  //quit - 跳出循环
    {
      break;
    }
    
    if(msg.mtext == 'r') //共享内存已更新，可以读取共享内存
    {
      sem_p(semid);  //减一
      printf("%s\n",shm);  //读取共享内存
      sem_v(semid);  //加一
    }
  }
  
  // 断开连接
  shmdt(shm);
  
  // 删除共享内存、消息队列
  shmctl(shmid, IPC_RMID, &buf1);
  msgctl(msqid, IPC_RMID, &buf2);
  
  // 删除信号量
  del_sem(semid);
  
  return 0;
}

```

**Client.c**

```c
#include<stdio.h>
#include<stdlib.h>
#include<sys/shm.h>  //shared memory
#include<sys/sem.h>  //semaphore
#include<sys/msg.h>  //message queue
#include<string.h>   //memcpy

// 消息队列结构
struct msg_form {
  long mtype;
  char mtext;
};

// 联合体，用于semctl初始化
union semun
{
  int val;  //for SETVAL
  struct semid_ds *buf;
  unsigned short *array;
};

/*
 * P操作:
 * 若信号量值为1，获取资源并将信号量值减一
 * 若信号量值为0，进程挂起等待
 */
int sem_p(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  //序号
  sbuf.sem_op = -1;  //P操作
  sbuf.sem_flg = SEM_UNDO;
  
  //int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("P operation Error");
    return -1;
  }
  return 0;
}

/*
 * V操作：
 * 释放资源并将信号量值加一
 * 如果有进程正在挂起等待，则唤醒它们
 */
int sem_v(int sem_id)
{
  struct sembuf sbuf;
  sbuf.sem_num = 0;  //序号
  sbuf.sem_op = 1;  //V操作
  sbuf.sem_flg = SEM_UNDO;
  
  //int semop(int semid, struct sembuf semoparray[], size_t numops);
  if(semop(sem_id, &sbuf, 1) == -1)
  {
    perror("V operation Error");
    return -1;
  }
  return 0;
}

int main()
{
  key_t key;
  int shmid;  //共享内存ID
  int semid;  //信号量ID
  int msqid;  //消息队列ID
  char *shm;  //共享内存地址
  struct msg_form msg;  //消息队列用于通知对方更新了共享内存
  int flag = 1; //while循环条件
  
  //获取key值
  if((key = ftok(".", 'z')) < 0)
  {
    perror("ftok error");
    exit(1);
  }
  
  //获取共享内存
  if((shmid = shmget(key, 1024, 0)) == -1)
  {
    perror("shmget error");
    exit(1);
  }
  
  //连接共享内存
  shm = (char*)shmat(shmid, 0, 0);
  if((int)shm == -1)
  {
    perror("Attach Shared Memory Error");
    exit(1);
  }
  
  //创建消息队列
  if((msqid = msgget(key, 0)) == -1)
  {
    perror("msgget error");
    exit(1);
  }
  
  //获取信号量
  if((semid = semget(key, 0, 0)) == -1)
  {
    perror("semget error");
    exit(1);
  }
  
  // 写数据
  printf("***************************************\n");
  printf("*                 IPC                 *\n");
  printf("*    Input r to send data to server.  *\n");
  printf("*    Input q to quit.                 *\n");
  printf("***************************************\n");
  while(flag)
  {
    char c;
    printf("Please input command: ");
    scanf("%c", &c);
    switch(c)
    {
      case 'r':
        printf("Data to send: ");
        sem_p(semid);  //访问资源
        scanf("%s", shm);
        sem_v(semid);  //释放资源
        
        //清空标准输入缓冲区
        while((c=getchar())!='\n' && c!=EOF);
        msg.mtype = 888;
        msg.mtext = 'r';  //发送消息通知服务器读数据
        msgsnd(msqid, &msg, sizeof(msg.mtext), 0);
        break;
      case 'q':
        msg.mtype = 888;
        msg.mtext = 'q';
        msgsnd(msqid, &msg, sizeof(msg.mtext), 0);
        flag = 0;
        break;
      default:
        printf("Wrong input!\n");
        //清空标准输入缓冲区
        while((c=getchar())!='\n' && c!=EOF);
    }
  }
  
  //断开连接
  shmdt(shm);
  return 0;
}

```