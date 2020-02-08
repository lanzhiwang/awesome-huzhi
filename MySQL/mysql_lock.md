## MySQL Lock

* [MySQL Innodb 中的锁](https://zhuanlan.zhihu.com/p/31875702)
* [MySQL 语句加锁分析](https://mp.weixin.qq.com/s?__biz=MzIxNTQ3NDMzMw==&mid=2247484169&idx=1&sn=f06eac890ea0f0810cedd6a2ca62fdd3&scene=19#wechat_redirect)

* 内部锁 - MySQL 在自身服务器内部执行的内部锁，管理多个会话对表内容的争用
  * 行级锁
  * 表级锁
* 外部锁 - MySQL 为客户会话提供选项来显式地获取`表锁`，以阻止其他会话访问表



#### 读锁

```bash
lock table tbl_name read;
flush table tbl_name;
...
unlock table;
```

#### 写锁

```bash
lock table tbl_name write;
flush table tbl_name;
...
flush table tbl_name;
unlock table;
```

#### 使用全局变量锁表
```bash
flush table with read lock;
set global read_only=on;
...
set global read_only=off;
unlock tables;
```
