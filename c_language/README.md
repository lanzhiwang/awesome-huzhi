## C 语言相关

### 内存分布

![](./memory.png)

通过这张图你可以看到，用户空间内存，从低到高分别是五种不同的内存段。

1. 只读段，包括代码和常量等。
2. 数据段，包括全局变量等。
3. 堆，包括动态分配的内存，从低地址开始向上增长。
4. 文件映射段，包括动态库、共享内存等，从高地址开始向下增长。
5. 栈，包括局部变量和函数调用的上下文等。栈的大小是固定的，一般是 8 MB。

在这五个内存段中，堆和文件映射段的内存是动态分配的。比如说，使用 C 标准库的 malloc() 或者 mmap() ，就可以分别在堆和文件映射段动态分配内存。



### C语言什么情况下需要用malloc来申请内存，为什么要申请内存？目的是什么？

malloc.h，是动态存储分配函数头文件，当对内存区进行操作时,调用相关函数。

数据量小使用**栈空间**，数据量大使用**堆空间**。也就是不用 malloc 的变量声明在栈，是编译器分配的空间，malloc 数据在堆区。

```c
#include "stdio.h"
#include "malloc.h"  // malloc() 函数被包含在 malloc.h 里面

int main(void)
{
   char*a=NULL;                          // 声明一个指向 a 的 char* 类型的指针
   a=(char*)malloc(100*sizeof(char));    // 使用 malloc 分配内存的首地址，然后赋值给 a
   if(!a)                                // 如果 malloc 失败，可以得到一些 log
   {
       perror("malloc");                 // 申请失败了，返回 -1 
       return -1;
   }
   sprintf(a,"%s","HelloWorld\n");       // 将 "HelloWorld\n" 写入 a 指向的地址
   printf("%s\n",a);                     // 输出用户输入的数据
   free(a);                              // 释放掉使用的内存地址
   return 0;
}
--------------------- 
作者：I_am_a_buger 
来源：CSDN 
原文：https://blog.csdn.net/i_am_a_buger/article/details/80980027 
版权声明：本文为博主原创文章，转载请附上博文链接！
```