## Redis 中的乐观锁和悲观锁

考虑一个业务场景，Redis 中存储了我们的账户余额，它是一个整数。现在有两个并发的客户端要对账户余额进行修改操作。这个修改操作不是简单的 incbry 指令，而是需要对余额乘以一个倍数。Redis 没有提供相关乘法的指令。我们需要先取出余额然后再内存里乘以倍数，再将结果写回 Redis。

这就会出现并发问题，因为有多个客户端会并发进行操作。我们可以通过 Redis 的分布式锁来避免冲突，这是一个很好的解决方案。**分布式锁是一种悲观锁。**

**Redis 提供了 watch 机制，它是一种乐观锁。**

```python
while True:
    do_watch()
    commands()
    multi()
    send_commands()
    try:
        exec()
        break
    except WatchError:
        continue
```
