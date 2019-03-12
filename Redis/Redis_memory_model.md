## Redis 内存模型

### Redis内存划分

Redis作为内存数据库，在内存中存储的内容主要是数据（键值对）；此外，除了数据以外，Redis的其他部分也会占用内存。

Redis的内存占用主要可以划分为以下几个部分：
* 数据

* 进程本身运行需要的内存

* 缓冲内存

* 内存碎片

##### 数据

作为数据库，数据是最主要的部分；这部分占用的内存会统计在 used_memory 中。

Redis 使用键值对存储数据，其中的值（对象）包括5种类型，即字符串、哈希、列表、集合、有序集合。这5种类型是Redis对外提供的，实际上，在Redis内部，每种类型可能有2种或更多的**内部编码**实现；此外，Redis在存储对象时，并不是直接将数据扔进内存，而是会对对象进行各种包装：如 redisObject、SDS 等**数据结构**。

##### 进程本身运行需要的内存

Redis 主进程本身运行肯定需要占用内存，如代码、常量池等等；这部分内存大约几兆，在大多数生产环境中与 Redis 数据占用的内存相比可以忽略。这部分内存不是由内存分配器分配，因此不会统计在 used_memory 中。

除了主进程外，Redis 创建的子进程运行也会占用内存，如 Redis 执行 AOF、RDB 重写时创建的子进程。当然，这部分内存不属于 Redis 主进程，也不会统计在 used_memory 和 used_memory_rss 中。

##### 缓冲内存

缓冲内存包括**客户端缓冲区**、**复制积压缓冲区**、**AOF 缓冲区**等；其中，客户端缓冲存储客户端连接的输入输出缓冲；复制积压缓冲用于部分复制功能；AOF 缓冲区用于在进行 AOF 重写时，保存最近的写入命令。这部分内存由内存分配器分配，因此会统计在 used_memory 中。

##### 内存碎片

内存碎片是 Redis 在分配、回收物理内存过程中产生的。例如，如果对数据的更改频繁，而且数据之间的大小相差很大，可能导致 redis 释放的空间在物理内存中并没有释放，但 redis 又无法有效利用，这就形成了内存碎片。内存碎片不会统计在 used_memory 中。

内存碎片的产生与对数据进行的操作、数据的特点等都有关；此外，与使用的内存分配器也有关系：如果内存分配器设计合理，可以尽可能的减少内存碎片的产生。

如果 Redis 服务器中的内存碎片已经很大，可以通过安全重启的方式减小内存碎片：因为重启之后，Redis 重新从备份文件中读取数据，在内存中进行重排，为每个数据重新选择合适的内存单元，减小内存碎片。

### Redis内存统计

```bash
127.0.0.1:6379> info memory
# Memory
used_memory:248897744  # Redis 分配器分配的内存总量（单位是字节），包括使用的虚拟内存（即swap），用于数据、缓冲内存
used_memory_human:237.37M  # used_memory_human只是显示更友好

used_memory_rss:257400832  # OS 看到的 Redis 使用的内存
used_memory_rss_human:245.48M

used_memory_peak:248958888
used_memory_peak_human:237.43M
used_memory_peak_perc:99.98%
used_memory_overhead:74343704
used_memory_startup:509680
used_memory_dataset:174554040
used_memory_dataset_perc:70.27%
allocator_allocated:248877560
allocator_active:249143296
allocator_resident:256606208
total_system_memory:1044770816
total_system_memory_human:996.37M
used_memory_lua:37888
used_memory_lua_human:37.00K
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
allocator_frag_ratio:1.00
allocator_frag_bytes:265736
allocator_rss_ratio:1.03
allocator_rss_bytes:7462912
rss_overhead_ratio:1.00
rss_overhead_bytes:794624
mem_fragmentation_ratio:1.03  # 内存碎片比率，该值是 used_memory_rss/ used_memory 的比值
mem_fragmentation_bytes:8586096
mem_allocator:jemalloc-4.0.3  # 内存分配器
active_defrag_running:0
lazyfree_pending_objects:0
127.0.0.1:6379> 

```

Here is the meaning of all fields in the memory section:

* used_memory: Total number of bytes allocated by Redis using its allocator (either standard libc, jemalloc, or an alternative allocator such as tcmalloc)  Redis使用其分配器（标准libc，jemalloc或替代分配器，如tcmalloc）分配的总字节数

* used_memory_human: Human readable representation of previous value

* used_memory_rss: Number of bytes that Redis allocated as seen by the operating system (a.k.a resident set size). This is the number reported by tools such as top(1) and ps(1)  操作系统看到的Redis分配的字节数（a.k.a常驻集大小）。 这是 top(1) 和 ps(1) 等工具报告的数字

* used_memory_rss_human: Human readable representation of previous value

* used_memory_peak: Peak memory consumed by Redis (in bytes)  Redis消耗的峰值内存（以字节为单位）

* used_memory_peak_human: Human readable representation of previous value

* used_memory_peak_perc: The percentage 百分比 of used_memory_peak out of used_memory

* used_memory_overhead: The sum in bytes of all overheads that the server allocated for managing its internal data structures  服务器为管理其内部数据结构而分配的所有开销的总和（以字节为单位）

* used_memory_startup: Initial amount of memory consumed by Redis at startup in bytes  Redis在启动时消耗的初始内存量（以字节为单位）

* used_memory_dataset: The size in bytes of the dataset (used_memory_overhead subtracted from used_memory)  used_memory 减去 used_memory_overhead

* used_memory_dataset_perc: The percentage of used_memory_dataset out of the net memory usage (used_memory minus used_memory_startup)

* total_system_memory: The total amount of memory that the Redis host has

* total_system_memory_human: Human readable representation of previous value

* used_memory_lua: Number of bytes used by the Lua engine

* used_memory_lua_human: Human readable representation of previous value

* maxmemory: The value of the maxmemory configuration directive

* maxmemory_human: Human readable representation of previous value

* maxmemory_policy: The value of the maxmemory-policy configuration directive

* mem_fragmentation_ratio: Ratio between used_memory_rss and used_memory

* mem_allocator: Memory allocator, chosen at compile time

* active_defrag_running: Flag indicating if active defragmentation is active

* lazyfree_pending_objects: The number of objects waiting to be freed (as a result of calling UNLINK, or FLUSHDB and FLUSHALL with the ASYNC option)

Ideally, the used_memory_rss value should be only slightly higher than used_memory. When rss >> used, a large difference means there is memory fragmentation (internal or external), which can be evaluated by checking mem_fragmentation_ratio. When used >> rss, it means part of Redis memory has been swapped off by the operating system: expect some significant latencies.  理想情况下，used_memory_rss 值应仅略高于 used_memory。 当 rss >>used 时，差异很大意味着存在内存碎片（内部或外部），可以通过检查 mem_fragmentation_ratio 来评估。 当使用 used >> rss 时，它意味着Redis内存的一部分已被操作系统交换：期望一些重要的延迟。

mem_fragmentation_ratio = used_memory_rss  / used_memory
mem_fragmentation_ratio 一般大于1，且该值越大，内存碎片比例越大。mem_fragmentation_ratio < 1，说明Redis使用了虚拟内存，由于虚拟内存的媒介是磁盘，比内存速度要慢很多，当这种情况出现时，应该及时排查，如果内存不足应该及时处理，如增加Redis节点、增加Redis服务器的内存、优化应用等。

Because Redis does not have control over how its allocations are mapped to memory pages, high used_memory_rss is often the result of a spike in memory usage.  由于 Redis 无法控制其分配如何映射到内存页面，因此高 used_memory_rss 通常是内存使用量激增的结果。

When Redis frees memory, the memory is given back to the allocator, and the allocator may or may not give the memory back to the system. There may be a discrepancy between the used_memory value and memory consumption as reported by the operating system. It may be due to the fact memory has been used and released by Redis, but not given back to the system. The used_memory_peak value is generally useful to check this point.  当 Redis 释放内存时，内存将返回给分配器，分配器可能会也可能不会将内存返回给系统。 use_memory 值与操作系统报告的内存消耗之间可能存在差异。 这可能是由于 Redis 已经使用和释放了内存，但没有返回给系统。 used_memory_peak 值通常用于检查此点。

Additional introspective information about the server's memory can be obtained by referring to the MEMORY STATS command and the MEMORY DOCTOR.  可以通过参考 MEMORY STATS 命令和 MEMORY DOCTOR 获得有关服务器内存的其他内省信息。



[参考](http://www.cnblogs.com/kismetv/p/8654978.html)