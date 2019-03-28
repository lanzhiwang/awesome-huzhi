## Linux 相关参数

### CPU 相关参数

* **user**: percent time spent in user space. User CPU time is the time spent on the processor running your program’s code (or code in libraries).  用户空间花费的时间百分比。 用户CPU时间是运行程序代码（或库中的代码）的处理器所花费的时间。

* **system**: percent time spent in kernel space. System CPU time is the time spent running code in the Operating System kernel.   内核空间花费的时间百分比。 系统CPU时间是在操作系统内核中运行代码所花费的时间。

* **idle**: percent of CPU used by any program. Every program or task that runs on a computer system occupies a certain amount of processing time on the CPU. If the CPU has completed all tasks it is idle.  任何程序使用的CPU百分比。 在计算机系统上运行的每个程序或任务在CPU上占用一定的处理时间。 如果CPU已完成所有任务，则它处于空闲状态。

* **nice** (*nix): percent time occupied by user level processes with a positive nice value. The time the CPU has spent running users’ processes that have been niced.  具有正的nice值的用户级进程占用的百分比时间。 CPU运行用户进程的时间。

* **irq** (Linux, *BSD): percent time spent servicing/handling hardware/software interrupts. Time servicing interrupts (hardware + software).  服务/处理硬件/软件中断所花费的时间百分比。 时间服务中断（硬件+软件）。

* **iowait** (Linux): percent time spent by the CPU waiting for I/O operations to complete.  CPU等待I / O操作完成所花费的时间百分比。

* **steal** (Linux): percentage of time a virtual CPU waits for a real CPU while the hypervisor is servicing another virtual processor.  虚拟机管理程序为另一个虚拟处理器提供服务时，虚拟CPU等待实际CPU的时间百分比。

* **ctx_sw**: number of context switches (voluntary + involuntary) per second. A context switch is a procedure that a computer’s CPU (central processing unit) follows to change from one task (or process) to another while ensuring that the tasks do not conflict.  每秒的上下文切换次数（自愿+非自愿）。 上下文切换是计算机的CPU（中央处理单元）遵循从一个任务（或进程）切换到另一个任务（或进程）同时确保任务不冲突的过程。

* **inter**: number of interrupts per second.  每秒中断次数。

* **sw_inter**: number of software interrupts per second. Always set to 0 on Windows and SunOS.  每秒软件中断次数。 始终在Windows和SunOS上设置为0。

* **syscal**: number of system calls per second. Do not displayed on Linux (always 0).  每秒系统调用次数。 不要在Linux上显示（始终为0）。

### Load

| **Load avg** | **Status** |
| ------------ | ---------- |
| \< 0.7*core | OK         |
| \> 0.7*core   | CAREFUL    |
| \> 1*core     | WARNING    |
| \> 5*core     | CRITICAL   |

### 内存相关参数

* [free 命令输出详解](https://github.com/lanzhiwang/awesome-huzhi/wiki/free-output-explanation)

### 网络性能测试

* [nc 命令示例](./linux/nc.md)


4. 磁盘I/O性能测试

