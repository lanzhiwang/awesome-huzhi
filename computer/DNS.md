## DNS

### A 记录

```bash
# 查询 A 记录
$ dig -t a www.ksu.edu.tw
www.ksu.edu.tw.		536	IN	A	120.114.100.65
$ 

```

### NS 记录

如果你想要知道 www.ksu.edu.tw 的这笔记录是由哪部 DNS 服务器提供的，那就得要使用 `NS (NameServer)` 的 RR 类型标志来查询。

```bash
# 查询 NS 记录
$ dig -t ns ksu.edu.tw
ksu.edu.tw.		46	IN	NS	dns3.twaren.net.
ksu.edu.tw.		46	IN	NS	dns1.ksu.edu.tw.
ksu.edu.tw.		46	IN	NS	dns2.ksu.edu.tw.
 
# 查询 NS 服务器对应的的 A 记录
$ dig -t a dns3.twaren.net.
dns3.twaren.net.	1513	IN	A	211.79.61.47

$ dig -t a dns1.ksu.edu.tw.
dns1.ksu.edu.tw.	3600	IN	A	120.114.50.1

$ dig -t a dns2.ksu.edu.tw.
dns2.ksu.edu.tw.	3600	IN	A	120.114.150.1

```

### SOA记录

如果你有多部 DNS 服务器管理同一个领域名时，那么最好使用 master/slave 的方式来进行管理。既然要这样管理， 那就得要宣告被管理的 zone file 是如何进行传输的，此时就得要 `SOA (Start Of Authority)` 的标志了。

```bash
# 查询 SOA 记录
$ dig -t soa ksu.edu.tw
ksu.edu.tw.		3599	IN	SOA	dns1.ksu.edu.tw. abuse.mail.ksu.edu.tw. 2014123133 1800 900 604800 86400

# 输出参数的含义
dns1.ksu.edu.tw.
Master DNS 服务器主机名：这个领域主要是哪部 DNS 作为 master 的意思。

abuse.mail.ksu.edu.tw. 
管理员的 email：要注意的是， 由于 @ 在数据库档案中是有特别意义的，因此这里就将 abuse@mail.ksu.edu.tw 改写成 abuse.mail.ksu.edu.tw。

2014123133 
序号 (Serial)：这个序号代表的是这个数据库档案的新旧，序号越大代表越新。 当 slave 要判断是否主动下载新的数据库时，就以序号是否比 slave 上的还要新来判断，若是则下载，若不是则不下载。 所以当你修订了数据库内容时，记得要将这个数值放大才行！ 

1800 
更新频率 (Refresh)：那么啥时 slave 会去向 master 要求数据更新的判断？ 就是这个数值定义的。

900 
失败重新尝试时间 (Retry)：如果因为某些因素，导致 slave 无法对 master 达成联机， 那么在多久的时间内，slave 会尝试重新联机到 master。在设定中，900 秒会重新尝试一次。意思是说，每 1800 秒 slave 会主动向 master 联机，但如果该次联机没有成功，那接下来尝试联机的时间会变成 900 秒。若后来有成功，则又会恢复到 1800 秒才再一次联机。

604800 
失效时间 (Expire)：如果一直失败尝试时间，持续联机到达这个设定值时限， 那么 slave 将不再继续尝试联机，并且尝试删除这份下载的 zone file 信息。设定为 604800 秒。意思是说，当联机一直失败，每 900 秒尝试到达 604800 秒后slave 将不再更新，只能等待系统管理员的处理。

86400
快取时间 (Minumum TTL)：如果这个数据库 zone file 中，每笔 RR 记录都没有写到 TTL 快取时间的话，那么就以这个 SOA 的设定值为主。

```

### CNAME 记录

```bash
# CNAME 记录查询
$ dig -t a www.baidu.com
www.baidu.com.		1098	IN	CNAME	www.a.shifen.com.
www.a.shifen.com.	286	IN	A	58.217.200.37
www.a.shifen.com.	286	IN	A	58.217.200.39

```

## MX 记录

MX 是 Mail eXchanger (邮件交换) 的意思，通常你的整个领域会设定一个 MX ，代表，所有寄给这个领域的 email 应该要送到后头的 email server 主机名上头才是。

```bash
# 查询 MX 记录
$ dig -t mx 163.com
163.com.		9307	IN	MX	10 163mx02.mxmail.netease.com.
163.com.		9307	IN	MX	10 163mx03.mxmail.netease.com.
163.com.		9307	IN	MX	50 163mx00.mxmail.netease.com.
163.com.		9307	IN	MX	10 163mx01.mxmail.netease.com.

# 字段含义
163.com.		9307	IN	MX	10 163mx02.mxmail.netease.com.
10 代表优先级，数字越小，优先级越高

# 查询邮件服务器对应的 A 记录
$ dig -t a 163mx00.mxmail.netease.com.
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.139
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.159
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.149
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.141
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.145
163mx00.mxmail.netease.com. 138	IN	A	220.181.14.161

```

### 反解记录

```bash
# 查找一个可用IP
$ dig -t a www.ksu.edu.tw
www.ksu.edu.tw.		840	IN	A	120.114.100.65

# 通过 IP 找到对应的域名
$ dig -x 120.114.100.65
65.100.114.120.in-addr.arpa. 3599 IN	PTR	eng.www.ksu.edu.tw.
65.100.114.120.in-addr.arpa. 3599 IN	PTR	chs.www.ksu.edu.tw.
65.100.114.120.in-addr.arpa. 3599 IN	PTR	www.ksu.edu.tw.

###
$ dig -t a eng.www.ksu.edu.tw.
ksu.edu.tw.		1799	IN	SOA	dns1.ksu.edu.tw. abuse.mail.ksu.edu.tw. 2014123133 1800 900 604800 86400

$ dig -t a chs.www.ksu.edu.tw.
ksu.edu.tw.		1799	IN	SOA	dns1.ksu.edu.tw. abuse.mail.ksu.edu.tw. 2014123133 1800 900 604800 86400

```

[DNS 其他记录查询网站，例如 txt ](https://mxtoolbox.com/)